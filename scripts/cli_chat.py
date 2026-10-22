"""Interactive Command-Line Interface (CLI) for Ultron Sovereign Core.

Allows testing queries and receiving synthesized responses directly in the terminal.
Usage:
    python scripts/cli_chat.py
"""

from __future__ import annotations

import os
import sys
import asyncio
import time

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from backend.synthesis.omni_fusion_engine import omni_fusion_engine


def print_banner():
    print("=" * 72)
    print("⚡ ULTRON SOVEREIGN CORE — TERMINAL CLIENT")
    print("=" * 72)
    print("Type your inquiry and press Enter.")
    print("Type 'exit' or 'quit' (or Ctrl+C) to leave.")
    print("=" * 72)


async def main():
    print_banner()

    while True:
        try:
            query = input("\n[You] > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting terminal client.")
            break

        if not query:
            continue

        if query.lower() in ("exit", "quit", "/q"):
            print("Session terminated.")
            break

        print("\nProcessing across empirical databases and models...")
        t0 = time.perf_counter()
        try:
            result = await omni_fusion_engine.fuse_and_synthesize(query)
            elapsed = time.perf_counter() - t0

            answer = (
                result.get("antigravity_verdict")
                or result.get("logical_factual_answer")
                or "No answer generated."
            )
            citations = result.get("citations", [])
            apis = result.get("apis_consulted", [])

            print("-" * 72)
            print(f"⚡ Synthesis Complete ({elapsed:.2f}s) | Sources Consulted: {len(apis)}")
            print("-" * 72)
            print(answer)

            if citations:
                print("\n📚 Key Citations:")
                for i, c in enumerate(citations[:4], 1):
                    title = c.get("title", "Reference")
                    source = c.get("source_name") or c.get("source", "Source")
                    url = c.get("url", "")
                    print(f"  [{i}] {title} ({source}) {url}")

            print("-" * 72)

        except Exception as e:
            print(f"⚠️ Error during processing: {e}")


if __name__ == "__main__":
    asyncio.run(main())
