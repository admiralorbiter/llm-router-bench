#!/usr/bin/env python3
"""Zero-dependency TTFT and SSE latency benchmark for OpenAI-compatible gateways."""

import argparse
import json
import os
import sys
import time
import urllib.request


def probe_models(base_url: str, api_key: str, timeout: float = 10.0) -> tuple[float, int]:
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/models",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    count = len(data.get("data", [])) if isinstance(data, dict) else 0
    return elapsed_ms, count


def benchmark_completion(base_url: str, api_key: str, model: str, prompt: str, stream: bool) -> dict:
    payload = json.dumps({
        "model": model,
        "stream": stream,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    ttft_ms = None
    chunks = 0
    with urllib.request.urlopen(req, timeout=20.0) as resp:
        if stream:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                if ttft_ms is None:
                    ttft_ms = (time.perf_counter() - t0) * 1000.0
                if line == "data: [DONE]":
                    break
                chunks += 1
        else:
            _ = resp.read()
            ttft_ms = (time.perf_counter() - t0) * 1000.0
            chunks = 1
    total_ms = (time.perf_counter() - t0) * 1000.0
    return {
        "model": model,
        "stream": stream,
        "ttft_ms": round(ttft_ms or total_ms, 2),
        "total_ms": round(total_ms, 2),
        "chunks": chunks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark OpenAI/LiteLLM/vLLM gateway latency.")
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1"))
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY", ""))
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--prompt", default="In one short sentence, define consistent hashing.")
    parser.add_argument("--stream", action="store_true", help="Measure multi-chunk SSE TTFT")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: pass --api-key or set OPENAI_API_KEY", file=sys.stderr)
        return 1

    models_ms, model_count = probe_models(args.base_url, args.api_key)
    result = benchmark_completion(args.base_url, args.api_key, args.model, args.prompt, args.stream)
    result["models_probe_ms"] = round(models_ms, 2)
    result["catalog_models"] = model_count
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
