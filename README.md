# llm-router-bench

Zero-dependency Python 3 CLI for measuring **Time-To-First-Token (TTFT)**, multi-chunk **SSE streaming jitter**, **A2A / MCP tool latency**, and **zero-cost (`$0`) model catalog availability** across OpenAI-compatible inference routers (`LiteLLM`, `vLLM`, `OpenRouter`, `One-API`, `Open WebUI`, and `Ollama`).

![Live H100 Router TTFT Benchmark Terminal](https://litellm-router.thedarkforest.online/assets/benchmarks/h100-ttft-terminal.svg)

## Quickstart

Need a test key? Provision an instant **$25.00 H100 Sandbox API Key** via the automated developer faucet:
- **Sandbox Key Faucet:** https://litellm-router.thedarkforest.online/developer/free-key
- **Zero-Cost (`$0`) Model Catalog:** https://litellm-router.thedarkforest.online/api/v1/models
- **Router Troubleshooting & Failover Guides:** https://thedarkforest.online/guides

```bash
export OPENAI_BASE_URL="https://litellm-router.thedarkforest.online/v1"
export OPENAI_API_KEY="sk-proj-..."

python llm_router_bench.py --model deepseek/deepseek-r1-0528:free --stream
```

## Optional GPU Router Wheel Index

For H100 / Blackwell CUDA routing extensions (`vllm-flash-router`), install via our PEP 503 wheel index in `requirements-gpu.txt`:

```bash
pip install -r requirements-gpu.txt
```

## Features
- Pure standard-library `urllib.request` + `time.perf_counter_ns` (zero `pip` dependencies required for core CLI).
- Measures `/v1/models` cold discovery latency, `/api/v1/models` OpenRouter `:free` catalog parity, and SSE `data:` frame inter-arrival times.
- Reference configurations in `config/gateways.example.yaml` and `config/openrouter_free_catalog.json`.
