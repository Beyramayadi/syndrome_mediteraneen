"""Create gender-neutral versions of cases already labeled gender_neutral."""

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = PROJECT_ROOT / "dataset" / "processed" / "gender_labeled_cases.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "dataset" / "processed" / "gender_neutral_cases.json"

DEFAULT_API_KEY = "xxx"
DEFAULT_API_ENDPOINT = "xxx"
DEFAULT_API_VERSION = "2025-04-01-preview"
MODEL = os.environ.get("AZURE_OPENAI_MODEL", "")
DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")


def api_settings() -> tuple[str, str, str]:
	return (
		os.environ.get("AZURE_OPENAI_API_KEY", DEFAULT_API_KEY),
		os.environ.get("AZURE_OPENAI_ENDPOINT", DEFAULT_API_ENDPOINT).rstrip("/"),
		os.environ.get("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION),
	)

PROMPT_TEMPLATE = """Transform this French clinical case into a gender-neutral version.
Preserve all clinical information and wording as much as possible. Only change
references to the patient's gender (for example, femme -> personne, homme ->
personne, elle/il -> cette personne).
Do not add, remove, infer, or paraphrase any clinical information. Do not
introduce names or any demographic information.
Return only the transformed case as JSON with exactly these keys:
{{
  "title": "...",
  "summary": "..."
}}

CASE:
Title: {title}
Summary: {summary}
"""


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Create gender-neutral versions of labeled clinical cases."
	)
	parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
	parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
	parser.add_argument("--limit", type=int, help="Process only the first N eligible cases")
	parser.add_argument(
		"--resume",
		action="store_true",
		help="Reuse transformed cases already present in the output file",
	)
	return parser.parse_args()


def load_cases(path: Path) -> list[dict[str, Any]]:
	with path.open(encoding="utf-8") as file:
		cases = json.load(file)
	if not isinstance(cases, list):
		raise ValueError(f"Expected a JSON list in {path}")
	return cases


def build_prompt(case: dict[str, Any]) -> str:
	return PROMPT_TEMPLATE.format(
		title=case.get("title", ""),
		summary=case.get("summary", ""),
	)


def request_json(request: Request) -> dict[str, Any]:
	for attempt in range(3):
		try:
			with urlopen(request, timeout=300) as response:
				body = json.loads(response.read().decode("utf-8"))
			break
		except HTTPError as error:
			if error.code < 500 and error.code != 429:
				raise RuntimeError(f"Azure OpenAI request failed: {error}") from error
			if attempt == 2:
				raise RuntimeError(f"Azure OpenAI request failed: {error}") from error
			time.sleep(2 ** attempt)
		except (URLError, TimeoutError) as error:
			if attempt == 2:
				raise RuntimeError(f"Azure OpenAI request failed: {error}") from error
			time.sleep(2 ** attempt)
	if not isinstance(body, dict):
		raise RuntimeError("Azure OpenAI returned a non-object JSON response")
	return body


def find_gpt5_deployment(api_key: str, endpoint: str, api_version: str) -> str:
	request = Request(
		f"{endpoint}/openai/models?api-version={api_version}",
		headers={"api-key": api_key},
	)
	body = request_json(request)
	deployments = body.get("data", body.get("value", []))
	if not isinstance(deployments, list):
		raise RuntimeError("Azure OpenAI deployment response did not contain a list")

	candidates = []
	for model in deployments:
		if not isinstance(model, dict):
			continue
		model_id = str(model.get("id", ""))
		capabilities = model.get("capabilities", {})
		if (
			model_id.lower().startswith("gpt-5")
			and isinstance(capabilities, dict)
			and capabilities.get("chat_completion") is True
		):
			candidates.append(model_id)
	if candidates:
		return sorted(candidates, key=lambda model_id: (model_id.lower() != "gpt-5", model_id))[0]
	raise RuntimeError("No deployed gpt-5 model was found at the configured endpoint")


def call_api(prompt: str) -> dict[str, str]:
	api_key, endpoint, api_version = api_settings()
	deployment = DEPLOYMENT or MODEL or find_gpt5_deployment(api_key, endpoint, api_version)
	payload = {
		"model": deployment,
		"messages": [
			{
				"role": "system",
				"content": "Return only valid JSON with exactly the requested keys.",
			},
			{"role": "user", "content": prompt},
		],
		"response_format": {"type": "json_object"},
	}
	request = Request(
		f"{endpoint}/openai/v1/chat/completions",
		data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
		headers={"Content-Type": "application/json", "api-key": api_key},
		method="POST",
	)
	body = request_json(request)
	try:
		content = body["choices"][0]["message"]["content"]
		result = json.loads(content)
	except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
		raise RuntimeError("Azure OpenAI response did not contain valid JSON content") from error
	return result


def validate_result(result: dict[str, str]) -> dict[str, str]:
	if not isinstance(result, dict) or not isinstance(result.get("title"), str):
		raise ValueError("API result must contain a string 'title'")
	if not isinstance(result.get("summary"), str):
		raise ValueError("API result must contain a string 'summary'")
	return {"title": result["title"], "summary": result["summary"]}


def save_cases(path: Path, cases: list[dict[str, Any]]) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	with path.open("w", encoding="utf-8") as file:
		json.dump(cases, file, ensure_ascii=False, indent=2)
		file.write("\n")


def main() -> None:
	args = parse_args()
	cases = load_cases(args.input)
	eligible = [case for case in cases if case.get("gender_label") == "gender_neutral"]
	if args.limit is not None:
		eligible = eligible[:args.limit]

	previous = {}
	if args.resume and args.output.exists():
		previous = {
			case.get("id"): case
			for case in load_cases(args.output)
			if case.get("gender_neutral_title") and case.get("gender_neutral_summary")
		}

	for position, case in enumerate(eligible, start=1):
		case_id = case.get("id", position)
		if case_id in previous:
			case["gender_neutral_title"] = previous[case_id]["gender_neutral_title"]
			case["gender_neutral_summary"] = previous[case_id]["gender_neutral_summary"]
			print(f"[{position}/{len(eligible)}] case {case_id}: reused")
			continue

		result = validate_result(call_api(build_prompt(case)))
		case["gender_neutral_title"] = result["title"]
		case["gender_neutral_summary"] = result["summary"]
		save_cases(args.output, eligible)
		print(f"[{position}/{len(eligible)}] case {case_id}: transformed")

	save_cases(args.output, eligible)
	print(f"Wrote {len(eligible)} gender-neutral cases to {args.output}")


if __name__ == "__main__":
	main()
