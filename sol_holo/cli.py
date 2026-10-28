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
from .v3_brain_manifest import V3BrainReflectiveOrchestrator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sol-holo",
        description="SOL-Holo: Holographic Autopoietic Continuum & Sovereign Digital Organism (Frontiers A-Z + V3 Brain Manifest)",
    )
    sub = parser.add_subparsers(dest="command", required=False)

    p_man = sub.add_parser("manifest", help="Build and verify the 26-Frontier Holographic Master Manifest")
    p_man.add_argument("--output", type=Path, default=None, help="Optional JSON path to write manifest")

    p_syn = sub.add_parser("synthesize", help="Run full SOL-Holo synthesis across Continuum + Lumina + Frontiers O/P/Q/R/S/T/U/V/W/X/Y/Z + Ledger")
    p_syn.add_argument("--live", action="store_true", help="Use live gemini-4-argon API if GEMINI_API_KEY is set")
    p_syn.add_argument("--model", type=str, default="gemini-4-argon", help="Model identifier")
    p_syn.add_argument("--output-manifest", type=Path, default=None, help="Optional path to save master manifest")

    p_v3 = sub.add_parser(
        "v3-brain",
        aliases=["v3-brain-manifest", "build-v3-brain-manifest", "reflective-domain"],
        help="Run V3 Brain Manifest reflective synthesis across SOLHoloOrganism, sol-cortex, sol-hippocampus, and sol-rsi/self-train",
    )
    p_v3.add_argument("--live", action="store_true", help="Use live gemini-4-argon API if GEMINI_API_KEY is set")
    p_v3.add_argument("--model", type=str, default="gemini-4-argon", help="Model identifier (default: gemini-4-argon)")
    p_v3.add_argument("--thinking-level", type=str, default="high", choices=["minimal", "low", "medium", "high"])
    p_v3.add_argument(
        "--enable-substrate-tools",
        dest="enable_substrate_tools",
        action="store_true",
        default=True,
        help="Enable emergent substrate tool-calling loop in v3-brain (default: True)",
    )
    p_v3.add_argument(
        "--no-substrate-tools",
        dest="enable_substrate_tools",
        action="store_false",
        help="Disable live substrate tool-calling loop",
    )
    p_v3.add_argument(
        "--max-tool-rounds",
        type=int,
        default=2,
        help="Maximum multi-turn tool-calling rounds for Holo_Substrate_Synthesizer (default: 2)",
    )
    p_v3.add_argument("--study-name", type=str, default="V3_Brain_Manifest_Reflective_Agentic_Domain")
    p_v3.add_argument("--output-manifest", "--export-manifest", dest="output_manifest", type=Path, default=None, help="Optional JSON path to write V3BrainManifest")
    p_v3.add_argument("--export-packet", "--export-lens-packet", dest="export_packet", type=Path, default=None, help="Optional JSON path to write sol-lens v0.2 packet")
    p_v3.add_argument("--ledger-db", type=Path, default=None, help="Optional SQLite path for GovernanceCourtLedger")
    p_v3.add_argument("--observatory-db", type=Path, default=None, help="Optional SQLite path for sol-change Observatory")
    p_v3.add_argument("--export-observatory-bundle", type=Path, default=None, help="Optional directory to write observatory bundle")
    p_v3.add_argument("--trials", type=int, default=5, help="Number of repeat trials K >= 3 (default: 5)")

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

    if args.command in ("v3-brain", "v3-brain-manifest", "build-v3-brain-manifest", "reflective-domain"):
        orch = V3BrainReflectiveOrchestrator(
            model=args.model,
            thinking_level=args.thinking_level,
            live=args.live,
            enable_substrate_tools=bool(getattr(args, "enable_substrate_tools", True)),
            max_tool_rounds=max(1, int(getattr(args, "max_tool_rounds", 2))),
        )
        v3_report = orch.run_v3_brain_synthesis(
            study_name=args.study_name,
            ledger_db_path=args.ledger_db,
            observatory_db_path=args.observatory_db,
            export_packet_path=args.export_packet,
            export_manifest_path=args.output_manifest,
            export_observatory_dir=args.export_observatory_bundle,
            repeat_trial_count=args.trials,
        )
        print(json.dumps(v3_report.to_dict(), indent=2))
        return 0 if v3_report.manifest.v3_brain_manifest_verified else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

