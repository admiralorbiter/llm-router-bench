# llm-router-bench

Zero-dependency Python 3 CLI for measuring **Time-To-First-Token (TTFT)**, multi-chunk **SSE streaming jitter**, and **model catalog availability** across OpenAI-compatible inference routers (`LiteLLM`, `vLLM`, `One-API`, and `Ollama`).

## Quickstart

```bash
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="sk-..."

python llm_router_bench.py --model gpt-4o-mini --stream
```

## Features
- Pure standard-library `urllib.request` + `time.perf_counter_ns` (zero `pip` dependencies required).
- Measures `/v1/models` cold discovery latency, non-streaming round-trip latency, and SSE `data:` frame inter-arrival times.
- Reads endpoint profiles from `OPENAI_BASE_URL` / `OPENAI_API_KEY` or `config/gateways.example.yaml`.
