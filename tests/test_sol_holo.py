"""
Test suite for `SOL-Holo` (`c:\\sol-systems\\sol-holo`).

Verifies:
1. All 14 Frontiers (`Frontier_A` through `Frontier_N`) in `SOLHoloMasterManifest`
   validate cleanly with a deterministic SHA-256 `holographic_merkle_root` and
   intact sacred core graph SHA-256 (`d0a80462d2b9389160502b097aca1932bb014941adf6e4b77799997283e4a1bc`).
2. `SOLHoloOrganism.run_holographic_synthesis()` executes the full Continuum Discovery
   (Frontiers I + K + M + N) and Lumina Sovereign 8-Ranger (Frontiers J + L + M + N)
   pipelines, chains them into `GovernanceCourtLedger`, and verifies `sol-change`
   observatory drift and `sol_edge.runtime.replay` parity.
3. `sol_holo.cli` (`manifest` and `synthesize` subcommands) exits with code 0.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

_THIS_FILE = Path(__file__).resolve()
_SOL_HOLO_ROOT = _THIS_FILE.parents[1]
_SOL_SYSTEMS_ROOT = _SOL_HOLO_ROOT.parent

for _p in (
    _SOL_HOLO_ROOT,
    _SOL_SYSTEMS_ROOT,
    _SOL_SYSTEMS_ROOT / "sol-continuum",
    _SOL_SYSTEMS_ROOT / "sol-change",
    _SOL_SYSTEMS_ROOT / "sol-decide",
    _SOL_SYSTEMS_ROOT / "sol-edge" / "src",
):
    _ps = str(_p)
    if _p.exists() and _ps not in sys.path:
        sys.path.insert(0, _ps)

from sol_holo import (
    FRONTIER_CATALOG,
    SOLHoloOrganism,
    compute_holographic_merkle_root,
)
from sol_holo.cli import main as sol_holo_cli_main


def test_sol_holo_14_frontier_master_manifest() -> None:
    organism = SOLHoloOrganism()
    manifest = organism.build_master_manifest()

    assert manifest.schema == "techman.sol-holo.master-manifest/v1.0"
    assert manifest.total_frontiers == 14
    assert len(FRONTIER_CATALOG) == 14
    assert manifest.all_frontiers_verified is True
    assert manifest.holographic_merkle_root.startswith("sha256:")
    assert manifest.sacred_core_immutability_verified is True
    assert (
        manifest.sacred_core_graph_sha256
        == "d0a80462d2b9389160502b097aca1932bb014941adf6e4b77799997283e4a1bc"
    )

    frontier_ids = [f["frontier_id"] for f in manifest.frontiers]
    expected_ids = [f"Frontier_{chr(ord('A') + i)}" for i in range(14)]
    assert frontier_ids == expected_ids
    for f in manifest.frontiers:
        assert f["verified"] is True
        assert f["verdict"] == "PROMOTE"
        assert f["packet_digest"].startswith("sha256:")

    # Verify Merkle root determinism
    recomputed_root = compute_holographic_merkle_root(
        [f["packet_digest"] for f in manifest.frontiers]
    )
    assert recomputed_root == manifest.holographic_merkle_root


def test_sol_holo_end_to_end_synthesis(tmp_path: Path) -> None:
    organism = SOLHoloOrganism()
    report = organism.run_holographic_synthesis(work_dir=tmp_path / "holo_work")

    assert report.all_verified is True
    assert report.manifest.all_frontiers_verified is True

    # Continuum branch (Frontiers I + K + M + N)
    cont = report.continuum_episode_summary
    assert cont["conjecture_status"] == "PROVED_THEOREM"
    assert cont["cycle0_status"] == "QUARANTINE"
    assert cont["cycle1_status"] == "ELIGIBLE"
    assert cont["frontier_k_verified"] is True
    assert cont["frontier_n_verified"] is True
    assert cont["causal_emergence_delta_ei"] > 0.0

    # Lumina branch (Frontiers J + L + M + N)
    lum = report.lumina_episode_summary
    assert lum["wideword_32_r7_hex"] == "0x7D5D7757"
    assert lum["wideword_64_r7_hex"] == "0x0078005655775757"
    assert lum["fault_cases_passed"] == 68
    assert lum["atomic_commit_status"] == "commit"
    assert lum["sovereign_runtime_mode"] == "shadow"
    assert lum["allow_production_execution"] is False
    assert lum["cycle0_status"] == "QUARANTINE"
    assert lum["cycle1_status"] == "ELIGIBLE"
    assert lum["frontier_l_verified"] is True
    assert lum["frontier_n_verified"] is True

    # Cross-run GovernanceCourtLedger & sol-change replay
    led = report.ledger_verification
    assert led["is_valid"] is True
    assert led["total_runs_verified"] == 2
    assert led["total_events_verified"] == 16
    assert led["cross_run_chained"] is True

    obs = report.observatory_assessments
    assert obs["continuum"]["comparability"] == "compatible"
    assert obs["continuum"]["outcome"] == "improved"
    assert obs["continuum"]["runtime_replay_verified"] is True
    assert obs["lumina"]["comparability"] == "compatible"
    assert obs["lumina"]["outcome"] == "improved"
    assert obs["lumina"]["runtime_replay_verified"] is True


def test_sol_holo_cli_manifest_and_synthesize(tmp_path: Path) -> None:
    manifest_out = tmp_path / "cli_manifest.json"
    rc_man = sol_holo_cli_main(["manifest", "--output", str(manifest_out)])
    assert rc_man == 0
    assert manifest_out.is_file()
    doc = json.loads(manifest_out.read_text(encoding="utf-8"))
    assert doc["total_frontiers"] == 14
    assert doc["all_frontiers_verified"] is True
