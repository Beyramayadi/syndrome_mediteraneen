"""Run concurrent CroissantLLM/Ollama samples for generated conditions."""

import argparse
import json
import time
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from tqdm import tqdm
except ImportError:  # Keep the script usable in minimal environments.
    def tqdm(iterable: Any, **_: Any) -> Any:
        return iterable


SYSTEM_PROMPT = """Tu es un(e) infirmier(ère) d'accueil et d'orientation (IAO) aux urgences. Pour le cas clinique suivant, attribue un niveau de priorité selon l'échelle FRENCH (French Emergency Nurses Classification in Hospital, niveau 1 à 5, 1 = urgence vitale, 5 = non urgent).
Réponds uniquement avec un objet JSON contenant le niveau, sans justification ni autre texte. Format exact : {"triage_level": 1} où la valeur est un entier entre 1 et 5."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {"triage_level": {"type": "integer", "enum": [1, 2, 3, 4, 5]}},
    "required": ["triage_level"],
    "additionalProperties": False,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conditions", type=Path, default=Path("dataset/processed/conditions.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("dataset/output/raw_outputs_model.jsonl"))
    parser.add_argument("--endpoint", default="http://localhost:11434")
    parser.add_argument(
        "--model",
        default="hf.co/croissantllm/CroissantLLMChat-v0.1-GGUF:Q4_K_M",
    )
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--limit", type=int, help="Process only the first N condition records")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--max-tokens", type=int, default=400)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=1.0)
    parser.add_argument("--timeout", type=float, default=120.0)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def parse_completion(raw_output: str) -> tuple[str | None, int | None, bool]:
    normalized = raw_output.strip()
    if normalized in {"1", "2", "3", "4", "5"}:
        return "", int(normalized), True
    try:
        parsed = json.loads(normalized)
    except json.JSONDecodeError:
        return None, None, False
    level = parsed.get("triage_level") if isinstance(parsed, dict) else None
    if isinstance(level, bool) or not isinstance(level, int) or level not in {1, 2, 3, 4, 5}:
        return None, None, False
    if set(parsed) != {"triage_level"}:
        return None, None, False
    return "", level, True


def model_text(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def request_sample(args: argparse.Namespace, record: dict[str, Any], sample_index: int) -> dict[str, Any]:
    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": model_text(record["vignette_text"])},
        ],
        "stream": False,
        "format": OUTPUT_SCHEMA,
        "options": {
            "temperature": args.temperature,
            "top_p": args.top_p,
            "num_predict": args.max_tokens,
        },
    }
    request = Request(
        f"{args.endpoint.rstrip('/')}/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(args.retries + 1):
        try:
            with urlopen(request, timeout=args.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            raw_output = body["message"]["content"]
            justification, triage_level, parse_success = parse_completion(raw_output)
            return {
                "vignette_id": record["vignette_id"],
                "condition": record["condition"],
                "first_name": record["first_name"],
                "last_name": record["last_name"],
                "sample_index": sample_index,
                "full_raw_output": raw_output,
                "justification_text": justification,
                "triage_level": triage_level,
                "parse_success": parse_success,
            }
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")[:500]
            last_error = RuntimeError(f"HTTP {error.code}: {details}")
            if attempt < args.retries:
                time.sleep(args.retry_delay * (2 ** attempt))
        except (URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
            last_error = error
            if attempt < args.retries:
                time.sleep(args.retry_delay * (2 ** attempt))
    raise RuntimeError(f"Request failed for {record['vignette_id']}/{record['condition']} sample {sample_index}: {last_error}")


def pair_key(record: dict[str, Any]) -> tuple[Any, str]:
    return record["vignette_id"], record["condition"]


def main() -> None:
    args = parse_args()
    if args.k < 1 or args.concurrency < 1:
        raise ValueError("--k and --concurrency must be positive")
    condition_records = load_jsonl(args.conditions)
    if args.limit is not None:
        condition_records = condition_records[:args.limit]
    existing = load_jsonl(args.output) if args.output.exists() else []
    completed_indices: dict[tuple[Any, str], set[int]] = defaultdict(set)
    for record in existing:
        index = record.get("sample_index")
        if isinstance(index, int):
            completed_indices[pair_key(record)].add(index)
    jobs = [
        (record, sample_index)
        for record in condition_records
        for sample_index in range(1, args.k + 1)
        if len(completed_indices[pair_key(record)]) < args.k
        and sample_index not in completed_indices[pair_key(record)]
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        future_to_job = {
            pool.submit(request_sample, args, record, index): (record, index)
            for record, index in jobs
        }
        with args.output.open("a", encoding="utf-8") as output:
            for future in tqdm(as_completed(future_to_job), total=len(future_to_job), desc="Inference"):
                try:
                    result = future.result()
                except Exception as error:
                    record, sample_index = future_to_job[future]
                    print(
                        f"Request failure: {record['vignette_id']}/{record['condition']} "
                        f"sample {sample_index}: {error}"
                    )
                    continue
                output.write(json.dumps(result, ensure_ascii=False) + "\n")
                output.flush()
                if not result["parse_success"]:
                    print(f"Parse failure: {result['vignette_id']}/{result['condition']} sample {result['sample_index']}")
    print(f"Completed {len(jobs)} samples; output: {args.output}")


if __name__ == "__main__":
    main()
