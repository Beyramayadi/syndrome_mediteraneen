"""Compute triage consistency and entropy from raw inference JSONL."""

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("dataset/output/raw_outputs_model.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("dataset/output/metrics_model.csv"))
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def entropy(values: list[int]) -> float:
    counts = Counter(values)
    total = len(values)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def main() -> None:
    args = parse_args()
    groups: dict[tuple[Any, str], list[int]] = {}
    parse_failures: Counter[tuple[Any, str]] = Counter()
    for record in load_jsonl(args.input):
        key = (record.get("vignette_id"), record.get("condition", ""))
        level = record.get("triage_level")
        if record.get("parse_success") and isinstance(level, int) and 1 <= level <= 5:
            groups.setdefault(key, []).append(level)
        else:
            parse_failures[key] += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "vignette_id", "condition", "n_parsed", "n_parse_failures", "triage_distribution",
        "modal_triage_level", "self_consistency_rate", "shannon_entropy",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for (vignette_id, condition), values in sorted(groups.items(), key=lambda item: (str(item[0][0]), item[0][1])):
            counts = Counter(values)
            mode_count = max(counts.values()) if counts else 0
            modes = sorted(level for level, count in counts.items() if count == mode_count)
            writer.writerow({
                "vignette_id": vignette_id,
                "condition": condition,
                "n_parsed": len(values),
                "n_parse_failures": parse_failures[(vignette_id, condition)],
                "triage_distribution": json.dumps(dict(sorted(counts.items()))),
                "modal_triage_level": modes[0] if modes else "",
                "self_consistency_rate": mode_count / len(values) if values else "",
                "shannon_entropy": entropy(values) if values else "",
            })
    print(f"Wrote {len(groups)} metric rows to {args.output}")


if __name__ == "__main__":
    main()
