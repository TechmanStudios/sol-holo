"""
CLI Entrypoint for `SOL-Holo` (`sol_holo.cli`)
==============================================

Usage:
  python -m sol_holo.cli manifest
  python -m sol_holo.cli synthesize [--live] [--output-manifest packets/sol_holo_master_manifest.json]
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from .holo_engine import SOLHoloOrganism


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sol-holo",
        description="SOL-Holo: Holographic Autopoietic Continuum & Sovereign Digital Organism (Frontiers A-T)",
    )
    sub = parser.add_subparsers(dest="command", required=False)

    p_man = sub.add_parser("manifest", help="Build and verify the 20-Frontier Holographic Master Manifest")
    p_man.add_argument("--output", type=Path, default=None, help="Optional JSON path to write manifest")

    p_syn = sub.add_parser("synthesize", help="Run full SOL-Holo synthesis across Continuum + Lumina + Frontiers O/P/Q/R/S/T + Ledger")
    p_syn.add_argument("--live", action="store_true", help="Use live gemini-4-argon API if GEMINI_API_KEY is set")
    p_syn.add_argument("--model", type=str, default="gemini-4-argon", help="Model identifier")
    p_syn.add_argument("--output-manifest", type=Path, default=None, help="Optional path to save master manifest")

    args = parser.parse_args(argv)
    organism = SOLHoloOrganism()

    if args.command in (None, "manifest"):
        manifest = organism.build_master_manifest()
        out_path = getattr(args, "output", None)
        if out_path is not None:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(manifest.to_dict(), indent=2) + "\n", encoding="utf-8")
        print(json.dumps(manifest.to_dict(), indent=2))
        return 0 if manifest.all_frontiers_verified else 1

    if args.command == "synthesize":
        client = None
        if args.live:
            try:
                from google import genai
                from sol_decide.agentic.live_llm_elicitation import _load_env_safely

                _load_env_safely()
                api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
                if api_key:
                    client = genai.Client(api_key=api_key)
            except Exception as exc:
                print(f"[sol-holo] Warning: falling back to deterministic synthesis ({exc})", file=sys.stderr)
        report = organism.run_holographic_synthesis(gemini_client=client, model=args.model)
        if args.output_manifest is not None:
            args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
            args.output_manifest.write_text(
                json.dumps(report.manifest.to_dict(), indent=2) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(report.to_dict(), indent=2))
        return 0 if report.all_verified else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
