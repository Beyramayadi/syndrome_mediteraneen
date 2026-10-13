"""Run the FRENCH triage experiment through the configured Azure OpenAI endpoint."""

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from gender_neurtral import api_settings
from run_inference import OUTPUT_SCHEMA, SYSTEM_PROMPT, load_jsonl, model_text, parse_completion

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable: Any, **_: Any) -> Any:
        return iterable


DEFAULT_DEPLOYMENT = "gpt-4o"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conditions", type=Path, default=Path("dataset/processed/conditions.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("dataset/output/raw_outputs_gpt4o.jsonl"))
    parser.add_argument("--deployment", default=os.environ.get("AZURE_OPENAI_DEPLOYMENT", DEFAULT_DEPLOYMENT))
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--limit", type=int, help="Process only the first N condition records")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--max-tokens", type=int, default=400)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=1.0)
    parser.add_argument("--timeout", type=float, default=120.0)
    return parser.parse_args()


def request_sample(args: argparse.Namespace, record: dict[str, Any], sample_index: int) -> dict[str, Any]:
    api_key, endpoint, api_version = api_settings()
    payload = {
        "model": args.deployment,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": model_text(record["vignette_text"])},
        ],
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "french_triage_level",
                "strict": True,
                "schema": OUTPUT_SCHEMA,
            },
        },
    }
    request = Request(
        f"{endpoint}/openai/v1/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "api-key": api_key},
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(args.retries + 1):
        try:
            with urlopen(request, timeout=args.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            raw_output = body["choices"][0]["message"]["content"]
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
    raise RuntimeError(
        f"Request failed for {record['vignette_id']}/{record['condition']} "
        f"sample {sample_index}: {last_error}"
    )


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
            for future in tqdm(as_completed(future_to_job), total=len(future_to_job), desc="Azure GPT-4o"):
                try:
                    result = future.result()
                except Exception as error:
                    record, sample_index = future_to_job[future]
                    print(f"Request failure: {record['vignette_id']}/{record['condition']} sample {sample_index}: {error}")
                    continue
                output.write(json.dumps(result, ensure_ascii=False) + "\n")
                output.flush()
                if not result["parse_success"]:
                    print(f"Parse failure: {result['vignette_id']}/{result['condition']} sample {result['sample_index']}")
    print(f"Completed {len(jobs)} samples; output: {args.output}")


if __name__ == "__main__":
    main()
