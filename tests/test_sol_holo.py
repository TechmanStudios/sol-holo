"""
Test suite for `SOL-Holo` (`c:\\sol-systems\\sol-holo`).

Verifies:
1. All 26 Frontiers (`Frontier_A` through `Frontier_Z`) in `SOLHoloMasterManifest`
   validate cleanly with a deterministic SHA-256 `holographic_merkle_root` and
   intact sacred core graph SHA-256 (`d0a80462d2b9389160502b097aca1932bb014941adf6e4b77799997283e4a1bc`).
2. `SOLHoloOrganism.run_holographic_synthesis()` executes all 14 synthesis branches
   (Continuum, Lumina, WGSL Prover, Swarm Cohomology, UMOK Edge, Mitotic Foliation,
   STWM Wavefront, RSI Compiler Governance, HCAM Shard Consensus, Waveguide SIMD Pipeline,
   Burn-In Attestation, Entangled Cadence Wavefront, Waveguide Channel Staging, and
   Sovereign Court Lockdown), chains them into `GovernanceCourtLedger`
   (14 runs, 112 `sol-edge` events), and verifies `sol-change` observatory drift and
   `sol_edge.runtime.replay` parity.
3. `sol_holo.cli` (`manifest` and `synthesize` subcommands) exits with code 0.
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
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


def test_sol_holo_20_frontier_master_manifest() -> None:
    organism = SOLHoloOrganism()
    manifest = organism.build_master_manifest()

    assert manifest.schema == "techman.sol-holo.master-manifest/v1.0"
    assert manifest.total_frontiers == 26
    assert len(FRONTIER_CATALOG) == 26
    assert manifest.all_frontiers_verified is True
    assert manifest.holographic_merkle_root.startswith("sha256:")
    assert manifest.sacred_core_immutability_verified is True
    assert (
        manifest.sacred_core_graph_sha256
        == "d0a80462d2b9389160502b097aca1932bb014941adf6e4b77799997283e4a1bc"
    )

    frontier_ids = [f["frontier_id"] for f in manifest.frontiers]
    expected_ids = [f"Frontier_{chr(ord('A') + i)}" for i in range(26)]
    assert frontier_ids == expected_ids
    for f in manifest.frontiers:
        assert f["verified"] is True
        assert f["verdict"] == "PROMOTE"
        assert f["packet_digest"].startswith("sha256:")
        assert str(f["interaction_id"]).startswith("v1_")
        assert len(f["thought_signature_digests"]) >= 1
        assert str(f["thought_signature_digests"][0]).startswith("sha256:")

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
    assert report.manifest.total_frontiers == 26

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

    # WGSL Decision Prover branch (Frontier O)
    wgsl = report.wgsl_prover_episode_summary
    assert wgsl["total_grid_cells"] == 4096
    assert wgsl["speedup_factor"] > 1.0
    assert wgsl["cycle0_status"] == "QUARANTINE"
    assert wgsl["cycle1_status"] == "ELIGIBLE"
    assert wgsl["frontier_o_verified"] is True

    # Multi-Robot Swarm Cohomology branch (Frontier P)
    swarm = report.swarm_cohomology_episode_summary
    assert swarm["payload_mass_kg"] >= 25.0
    assert swarm["num_robots"] == 2
    assert swarm["total_dof"] == 12
    assert swarm["cycle0_squeeze_wrench_n"] > 15.0
    assert swarm["cycle1_squeeze_wrench_n"] <= 15.0
    assert swarm["cycle0_rotational_defect_deg"] > 3.0
    assert swarm["cycle1_rotational_defect_deg"] <= 3.0
    assert swarm["estop_latency_us"] <= 200.0
    assert swarm["gps_or_mocap_required"] is False
    assert swarm["cycle0_status"] == "QUARANTINE"
    assert swarm["cycle1_status"] == "ELIGIBLE"
    assert swarm["frontier_p_verified"] is True

    # UMOK Edge Kernel branch (Frontier Q)
    umok = report.umok_edge_episode_summary
    assert umok["cycle0_mean_step_latency_us"] > 1.0
    assert umok["cycle1_mean_step_latency_us"] <= 1.0
    assert umok["zero_copy_verified"] is True
    assert umok["cycle0_safe_state_action"] == "HOLD_SAFE_POSITION"
    assert umok["cycle1_safe_state_action"] == "NONE"
    assert umok["cycle0_staged_frames_count"] == 0
    assert umok["cycle1_staged_frames_count"] == 4
    assert umok["release_gate_status"] == "ELIGIBLE_AWAITING_RELEASE_AUTHORITY"
    assert umok["authorized_claimed"] is False
    assert umok["cycle0_status"] == "QUARANTINE"
    assert umok["cycle1_status"] == "ELIGIBLE"
    assert umok["frontier_q_verified"] is True

    # Mitotic Foliation branch (Frontier R)
    mitotic = report.mitotic_foliation_episode_summary
    assert abs(float(mitotic["cycle1_alpha"]) - 0.50) <= 1e-4
    assert mitotic["toroidal_genus_g"] == 1
    assert mitotic["euler_characteristic_chi"] == 0
    assert mitotic["cycle1_mass_conservation_residual"] <= 1e-9
    assert mitotic["sacred_core_immutable"] is True
    assert mitotic["cycle0_status"] == "QUARANTINE"
    assert mitotic["cycle1_status"] == "ELIGIBLE"
    assert mitotic["frontier_r_verified"] is True

    # STWM Wavefront branch (Frontier S)
    stwm = report.stwm_wavefront_episode_summary
    assert stwm["pdm_8bit_passed_cases"] == 6
    assert stwm["prefix_carry_passed_cases"] == 8
    assert stwm["hierarchical_32b_passed"] == 5
    assert stwm["hierarchical_64b_passed"] == 5
    assert stwm["quantum_calibration_passed_regimes"] == 12
    assert stwm["cycle1_interlane_crosstalk_db"] <= -30.0
    assert stwm["cycle0_status"] == "QUARANTINE"
    assert stwm["cycle1_status"] == "ELIGIBLE"
    assert stwm["frontier_s_verified"] is True

    # RSI Compiler Governance branch (Frontier T)
    rsi = report.rsi_compiler_episode_summary
    assert rsi["rc_id"] == "SOL-WAVEGUIDE-RC2"
    assert rsi["replay_verified_count"] >= 2
    assert rsi["replay_failed_count"] == 0
    assert rsi["production_mutation_allowed"] is False
    assert rsi["cycle0_status"] == "QUARANTINE"
    assert rsi["cycle1_status"] == "ELIGIBLE"
    assert rsi["frontier_t_verified"] is True

    # HCAM Shard Consensus branch (Frontier U)
    hcam = report.hcam_shard_episode_summary
    assert hcam["banks_32b"] == 4
    assert hcam["banks_64b"] == 8
    assert hcam["shard_count"] == 4
    assert hcam["cycle1_local_quorum_shards"] >= 3
    assert hcam["orphan_nodes_reclaimed"] >= 1
    assert hcam["live_root_reclaimed"] is False
    assert hcam["cycle0_status"] == "QUARANTINE"
    assert hcam["cycle1_status"] == "ELIGIBLE"
    assert hcam["frontier_u_verified"] is True

    # Waveguide SIMD Pipeline branch (Frontier V)
    wsimd = report.waveguide_simd_episode_summary
    assert wsimd["predicated_diamonds_converted"] >= 1
    assert wsimd["flags_externally_visible"] is False
    assert wsimd["assembled_core_count"] == 4
    assert wsimd["simd_lane_width"] in (4, 64)
    assert wsimd["fault_matrix_passed_cases"] >= 5
    assert wsimd["cycle0_status"] == "QUARANTINE"
    assert wsimd["cycle1_status"] == "ELIGIBLE"
    assert wsimd["frontier_v_verified"] is True

    # Burn-In Attestation branch (Frontier W)
    burnin = report.burnin_attestation_episode_summary
    assert burnin["cycles_executed"] >= 6
    assert burnin["ready_verification_steps"] >= 5
    assert burnin["real_signature_claimed"] is False
    assert burnin["network_access_used"] is False
    assert burnin["cycle0_status"] == "QUARANTINE"
    assert burnin["cycle1_status"] == "ELIGIBLE"
    assert burnin["frontier_w_verified"] is True

    # Entangled Cadence Wavefront branch (Frontier X)
    ecw = report.entangled_cadence_episode_summary
    assert ecw["manifold_count"] == 4
    assert ecw["group_coherence"] >= 0.99
    assert ecw["post_sync_max_skew"] <= 0.05
    assert ecw["autonomy_bounded"] is True
    assert ecw["alignment_score"] >= 0.99
    assert ecw["cycle0_status"] == "QUARANTINE"
    assert ecw["cycle1_status"] == "ELIGIBLE"
    assert ecw["frontier_x_verified"] is True

    # Waveguide Channel Staging branch (Frontier Y)
    wcs = report.waveguide_channel_staging_episode_summary
    assert wcs["recognized_kernels_count"] == 5
    assert wcs["raw_hazard_detected_on_conflict"] is True
    assert wcs["crosstalk_reduction"] > 0.0
    assert wcs["noop_dry_run_events_count"] == 182
    assert wcs["local_staging_copied_files"] == 28
    assert wcs["physical_execution_permitted_by_gate"] is False
    assert wcs["cycle0_status"] == "QUARANTINE"
    assert wcs["cycle1_status"] == "ELIGIBLE"
    assert wcs["frontier_y_verified"] is True

    # Sovereign Court Lockdown branch (Frontier Z)
    scl = report.sovereign_court_lockdown_episode_summary
    assert scl["registered_gates_count"] == 11
    assert scl["passed_gates_count"] == 11
    assert scl["finalization_evidence_items_count"] == 10
    assert scl["freeze_invariant_count"] == 10
    assert scl["lockdown_setting_count"] == 12
    assert scl["allow_production_execution"] is False
    assert scl["authorized_claimed"] is False
    assert scl["cycle0_status"] == "QUARANTINE"
    assert scl["cycle1_status"] == "ELIGIBLE"
    assert scl["frontier_z_verified"] is True

    # Cross-run GovernanceCourtLedger & sol-change replay (14 runs, 112 events)
    led = report.ledger_verification
    assert led["is_valid"] is True
    assert led["total_runs_verified"] == 14
    assert led["total_events_verified"] == 112
    assert led["cross_run_chained"] is True

    obs = report.observatory_assessments
    for key in (
        "continuum",
        "lumina",
        "wgsl_prover",
        "swarm_cohomology",
        "umok_edge",
        "mitotic_foliation",
        "stwm_wavefront",
        "rsi_compiler",
        "hcam_shard",
        "waveguide_simd",
        "burnin_attestation",
        "entangled_cadence",
        "waveguide_channel_staging",
        "sovereign_court_lockdown",
    ):
        assert obs[key]["comparability"] == "compatible"
        assert obs[key]["outcome"] == "improved"
        assert obs[key]["runtime_replay_verified"] is True


def test_sol_holo_cli_manifest_and_synthesize(tmp_path: Path) -> None:
    manifest_out = tmp_path / "cli_manifest.json"
    rc_man = sol_holo_cli_main(["manifest", "--output", str(manifest_out)])
    assert rc_man == 0
    assert manifest_out.is_file()
    doc = json.loads(manifest_out.read_text(encoding="utf-8"))
    assert doc["total_frontiers"] == 26
    assert doc["all_frontiers_verified"] is True

    syn_manifest_out = tmp_path / "cli_syn_manifest.json"
    rc_syn = sol_holo_cli_main(["synthesize", "--output-manifest", str(syn_manifest_out)])
    assert rc_syn == 0
    assert syn_manifest_out.is_file()
    syn_doc = json.loads(syn_manifest_out.read_text(encoding="utf-8"))
    assert syn_doc["total_frontiers"] == 26
    assert syn_doc["all_frontiers_verified"] is True


def test_sol_holo_standalone_packet_synthesis(tmp_path: Path) -> None:
    organism = SOLHoloOrganism()
    report = organism._run_standalone_packet_synthesis()
    assert report.all_verified is True
    assert report.manifest.all_frontiers_verified is True
    assert report.manifest.total_frontiers == 26
    assert report.continuum_episode_summary["conjecture_status"] == "PROVED_THEOREM"
    assert report.continuum_episode_summary["interaction_id"].startswith("v1_")
    assert report.lumina_episode_summary["wideword_32_r7_hex"] == "0x7D5D7757"
    assert report.lumina_episode_summary["wideword_64_r7_hex"] == "0x0078005655775757"
    assert report.lumina_episode_summary["fault_cases_passed"] == 68
    assert report.lumina_episode_summary["interaction_id"].startswith("v1_")
    assert report.wgsl_prover_episode_summary["frontier_o_verified"] is True
    assert report.wgsl_prover_episode_summary["interaction_id"].startswith("v1_")
    assert report.swarm_cohomology_episode_summary["frontier_p_verified"] is True
    assert report.swarm_cohomology_episode_summary["interaction_id"].startswith("v1_")
    assert report.umok_edge_episode_summary["frontier_q_verified"] is True
    assert report.umok_edge_episode_summary["interaction_id"].startswith("v1_")
    assert report.umok_edge_episode_summary["authorized_claimed"] is False
    assert report.mitotic_foliation_episode_summary["frontier_r_verified"] is True
    assert report.mitotic_foliation_episode_summary["interaction_id"].startswith("v1_")
    assert report.stwm_wavefront_episode_summary["frontier_s_verified"] is True
    assert report.stwm_wavefront_episode_summary["interaction_id"].startswith("v1_")
    assert report.rsi_compiler_episode_summary["frontier_t_verified"] is True
    assert report.rsi_compiler_episode_summary["interaction_id"].startswith("v1_")
    assert report.rsi_compiler_episode_summary["production_mutation_allowed"] is False
    assert report.hcam_shard_episode_summary["frontier_u_verified"] is True
    assert report.hcam_shard_episode_summary["interaction_id"].startswith("v1_")
    assert report.hcam_shard_episode_summary["orphan_nodes_reclaimed"] == 2
    assert report.waveguide_simd_episode_summary["frontier_v_verified"] is True
    assert report.waveguide_simd_episode_summary["interaction_id"].startswith("v1_")
    assert report.waveguide_simd_episode_summary["simd_lane_width"] == 64
    assert report.waveguide_simd_episode_summary["fault_matrix_passed_cases"] == 33
    assert report.burnin_attestation_episode_summary["frontier_w_verified"] is True
    assert report.burnin_attestation_episode_summary["interaction_id"].startswith("v1_")
    assert report.burnin_attestation_episode_summary["ready_verification_steps"] == 7
    assert report.burnin_attestation_episode_summary["real_signature_claimed"] is False
    assert report.burnin_attestation_episode_summary["network_access_used"] is False
    assert report.entangled_cadence_episode_summary["frontier_x_verified"] is True
    assert report.entangled_cadence_episode_summary["interaction_id"].startswith("v1_")
    assert report.waveguide_channel_staging_episode_summary["frontier_y_verified"] is True
    assert report.waveguide_channel_staging_episode_summary["interaction_id"].startswith("v1_")
    assert report.sovereign_court_lockdown_episode_summary["frontier_z_verified"] is True
    assert report.sovereign_court_lockdown_episode_summary["interaction_id"].startswith("v1_")
    assert report.sovereign_court_lockdown_episode_summary["allow_production_execution"] is False
    assert report.sovereign_court_lockdown_episode_summary["authorized_claimed"] is False
    assert report.ledger_verification["total_runs_verified"] == 14
    assert report.ledger_verification["total_events_verified"] == 112
    assert report.ledger_verification["cross_run_chained"] is True

    # Negative check: tampering with package_archive_digest_attestation.real_signature_claimed
    # in standalone packets directory must be surfaced in burnin_attestation_episode_summary
    # and fail manifest verification.
    tampered_dir = tmp_path / "tampered_packets"
    shutil.copytree(organism.packets_dir, tampered_dir)
    burnin_file = tampered_dir / "live_gemini4_burnin_attestation_packet.json"
    burnin_data = json.loads(burnin_file.read_text(encoding="utf-8"))
    burnin_data["frontier_w_verification"]["package_archive_digest_attestation"]["real_signature_claimed"] = True
    burnin_file.write_text(json.dumps(burnin_data, indent=2), encoding="utf-8")

    tampered_org = SOLHoloOrganism(packets_dir=tampered_dir)
    tampered_rep = tampered_org._run_standalone_packet_synthesis()
    assert tampered_rep.burnin_attestation_episode_summary["real_signature_claimed"] is True
    assert tampered_rep.all_verified is False
    assert tampered_rep.manifest.all_frontiers_verified is False
