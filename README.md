# syndrome-mediteraneen

Experiment outputs are stored under `dataset/output`: one model-specific
`raw_outputs_*.jsonl` file per Ollama model, with statistical reports and plots
under `dataset/output/analysis`.

## CroissantLLM bias-audit pipeline

Run these commands from the repository root. The first step creates an
auditable JSONL file and makes no model calls.

```bash
python scripts/generate_conditions.py \
	--vignettes dataset/processed/gender_neutral_cases.json \
	--names dataset/processed/names.json \
	--output dataset/processed/conditions.jsonl \
	--seed 20260910
```

Start CroissantLLM with vLLM, then pass the served model name to inference:

```bash
python scripts/run_inference.py \
	--conditions dataset/processed/conditions.jsonl \
	--output dataset/output/raw_outputs_model.jsonl \
	--endpoint http://localhost:8000/v1 \
	--model YOUR_VLLM_MODEL_NAME \
	--k 10 --temperature 0.7 --top-p 0.9 \
	--max-tokens 400 --concurrency 8
```

Inference appends results as they complete and can be rerun safely. It skips
condition pairs that already have all requested sample indices. Parse failures
remain in the JSONL with `parse_success: false`.

Compute one summary row per vignette and condition:

```bash
python scripts/compute_metrics.py \
	--input dataset/output/raw_outputs_model.jsonl \
	--output dataset/output/metrics_model.csv
```

The metrics include the triage distribution, modal level, self-consistency,
Shannon entropy, parsed-sample count, and parse-failure count.

## Synthetic dataset inference with Ollama

`scripts/run_inference_v2.py` runs the same triage experiment design directly on
`dataset/processed/synthetic/synthetic.json` and uses Ollama via
`http://localhost:11434/api/chat`.

Choose the model at runtime with `--model`:

```bash

python scripts/run_inference_v2.py \
	--model hf.co/croissantllm/CroissantLLMChat-v0.1-GGUF:Q4_K_M \
	--endpoint http://localhost:11434 \
	--k 10 \
	--output dataset/output/raw_outputs_synthetic_croissantllm.jsonl

python scripts/run_inference_v2.py \
	--model m/biomistral:latest \
	--endpoint http://localhost:11434 \
	--k 10 \
	--output dataset/output/raw_outputs_synthetic_biomistral.jsonl

python scripts/run_inference_v2.py \
	--model llama3.1:latest \
	--endpoint http://localhost:11434 \
	--k 10 \
	--output dataset/output/raw_outputs_synthetic_llama31.jsonl

python scripts/run_inference_v2.py \
	--model mistral-nemo:latest \
	--endpoint http://localhost:11434 \
	--k 10 \
	--output dataset/output/raw_outputs_synthetic_mistral_nemo.jsonl

python scripts/run_inference_v2.py \
	--model qwen2.5:14b \
	--endpoint http://localhost:11434 \
	--k 10 \
	--output dataset/output/raw_outputs_synthetic_qwen25_14b.jsonl
```

If `--model` is omitted, the script falls back to its default model value.