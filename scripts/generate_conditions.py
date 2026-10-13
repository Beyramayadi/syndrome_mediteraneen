"""Generate auditable name-insertion conditions from gender-neutral cases."""

import argparse
import json
import random
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = (
    "european_male",
    "european_female",
    "maghrebi_male",
    "maghrebi_female",
    "control",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vignettes",
        type=Path,
        default=PROJECT_ROOT / "dataset/processed/gender_neutral_cases.json",
    )
    parser.add_argument(
        "--names",
        type=Path,
        default=PROJECT_ROOT / "dataset/processed/names.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "dataset/processed/conditions.jsonl",
    )
    parser.add_argument("--seed", type=int, default=20260910)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def build_vignette(case: dict[str, Any], full_name: str | None) -> str:
    title = str(case.get("gender_neutral_title", "")).strip()
    summary = str(case.get("gender_neutral_summary", "")).strip()
    if full_name is not None:
        summary = f"{full_name}, {summary}"
    return f"{title}\n\n{summary}".strip()


def sample_name(condition: str, names: dict[str, Any], rng: random.Random) -> tuple[str | None, str | None]:
    if condition == "control":
        return None, None
    first_name_group = names.get("first_names", {}).get(condition, [])
    last_name_group = names.get("last_names", {}).get(
        "maghrebi" if condition.startswith("maghrebi") else "european", []
    )
    if not first_name_group or not last_name_group:
        raise ValueError(f"Missing names for condition {condition}")
    return rng.choice(first_name_group), rng.choice(last_name_group)


def main() -> None:
    args = parse_args()
    cases = load_json(args.vignettes)
    names = load_json(args.names)
    if not isinstance(cases, list):
        raise ValueError(f"Expected a JSON list in {args.vignettes}")

    rng = random.Random(args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as output:
        for case in cases:
            for condition in CONDITIONS:
                first_name, last_name = sample_name(condition, names, rng)
                full_name = (
                    f"{first_name} {last_name}"
                    if first_name is not None and last_name is not None
                    else None
                )
                record = {
                    "vignette_id": case.get("id"),
                    "condition": condition,
                    "first_name": first_name,
                    "last_name": last_name,
                    "source_title": case.get("gender_neutral_title", ""),
                    "source_summary": case.get("gender_neutral_summary", ""),
                    "vignette_text": build_vignette(case, full_name),
                }
                output.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Wrote {len(cases) * len(CONDITIONS)} condition records to {args.output}")


if __name__ == "__main__":
    main()
