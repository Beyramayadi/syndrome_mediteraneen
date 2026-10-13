"""Classify clinical cases by whether their gender can be counterfactually changed.

The classifier asks a local Ollama model whether replacing the patient's gender
with the other gender would make the case medically incoherent. It does not
infer the label from gendered words alone: a male or female patient with a
gender-neutral condition can still receive ``gender_neutral``.
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "dataset" / "processed" / "parsed_cases.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "dataset" / "processed" / "gender_labeled_cases.json"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:14b"

SYSTEM_PROMPT = """Tu es un annotateur médical chargé de classer des cas cliniques.
La question porte uniquement sur le sexe/genre du patient principal.

gender_specific signifie que remplacer le patient par une personne de l'autre
sexe rendrait le cas médicalement incohérent, parce que le diagnostic, l'organe,
la grossesse, une structure anatomique ou une autre caractéristique essentielle
est liée au sexe. Un cas n'est PAS spécifique seulement parce que le patient est
décrit comme un homme ou une femme, ni parce que des comportements sociaux sont
mentionnés.

gender_neutral signifie que le texte resterait médicalement cohérent après ce
remplacement, même si certains détails comme l'âge ou les pronoms devaient être
adaptés. En cas de doute, choisis gender_neutral.

Réponds exclusivement avec un objet JSON valide, sans markdown, exactement avec
les clés suivantes:
{
  "label": "gender_specific" ou "gender_neutral",
	"confidence": un entier entre 0 et 10
}"""


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Classify parsed clinical cases with a local Ollama model."
	)
	parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
	parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
	parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL))
	parser.add_argument(
		"--ollama-url",
		default=os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL),
		help="Ollama server URL, without /api/chat",
	)
	parser.add_argument("--limit", type=int, help="Process only the first N cases")
	parser.add_argument(
		"--resume",
		action="store_true",
		help="Reuse labels already present in the output file",
	)
	return parser.parse_args()


def case_text(case: dict[str, Any]) -> str:
	return f"Titre : {case.get('title', '')}\nRésumé : {case.get('summary', '')}".strip()


def call_ollama(base_url: str, model: str, case: dict[str, Any]) -> dict[str, Any]:
	payload = {
		"model": model,
		"stream": False,
		"format": "json",
		"options": {"temperature": 0},
		"messages": [
			{"role": "system", "content": SYSTEM_PROMPT},
			{"role": "user", "content": case_text(case)},
		],
	}
	request = Request(
		f"{base_url.rstrip('/')}/api/chat",
		data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
		headers={"Content-Type": "application/json"},
		method="POST",
	)
	try:
		with urlopen(request, timeout=300) as response:
			body = json.loads(response.read().decode("utf-8"))
	except (HTTPError, URLError, TimeoutError) as error:
		raise RuntimeError(f"Ollama request failed: {error}") from error

	content = body.get("message", {}).get("content")
	if not isinstance(content, str):
		raise RuntimeError("Ollama response did not contain message.content")
	try:
		result = json.loads(content)
	except json.JSONDecodeError as error:
		raise RuntimeError(f"Ollama returned invalid JSON: {content!r}") from error

	if result.get("label") not in {"gender_specific", "gender_neutral"}:
		raise RuntimeError(f"Unexpected label from Ollama: {result.get('label')!r}")
	confidence = result.get("confidence")
	if isinstance(confidence, bool) or not isinstance(confidence, int) or not 0 <= confidence <= 10:
		raise RuntimeError(f"Invalid confidence from Ollama: {confidence!r}")
	return {"label": result["label"], "confidence": confidence}


def load_cases(path: Path) -> list[dict[str, Any]]:
	with path.open(encoding="utf-8") as file:
		cases = json.load(file)
	if not isinstance(cases, list):
		raise ValueError(f"Expected a JSON list in {path}")
	return cases


def main() -> None:
	args = parse_args()
	cases = load_cases(args.input)
	previous = {}
	if args.resume and args.output.exists():
		previous = {case.get("id"): case for case in load_cases(args.output)}
	if args.limit is not None:
		cases = cases[:args.limit]

	for position, case in enumerate(cases, start=1):
		case_id = case.get("id", position)
		if case_id in previous and previous[case_id].get("gender_label"):
			case.update({key: previous[case_id][key] for key in (
				"gender_label", "gender_confidence"
			) if key in previous[case_id]})
			print(f"[{position}/{len(cases)}] case {case_id}: reused")
			continue

		result = call_ollama(args.ollama_url, args.model, case)
		case["gender_label"] = result["label"]
		case["gender_confidence"] = result["confidence"]
		print(f"[{position}/{len(cases)}] case {case_id}: {result['label']}")

	args.output.parent.mkdir(parents=True, exist_ok=True)
	with args.output.open("w", encoding="utf-8") as file:
		json.dump(cases, file, ensure_ascii=False, indent=2)
		file.write("\n")
	print(f"Wrote {len(cases)} labeled cases to {args.output}")


if __name__ == "__main__":
	main()
