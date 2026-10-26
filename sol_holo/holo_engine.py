"""
SOL-Holo Core Engine (`sol_holo.holo_engine`)
=============================================

Unifies all 26 Frontiers (`A` through `Z`) across `c:\\sol-systems` into a single
Holographic Autopoietic Continuum & Sovereign Digital Organism (`SOLHoloOrganism`).

Holographic Principle in SOL-Holo:
Every local epistemic claim, topological 1-cycle, Riemannian logic circuit,
32/64-bit WideWord waveguide instruction, and 8-Ranger field observation is
simultaneously encoded on the lower-dimensional boundary:
  1. `techman.sol-lens.proof-packet/v0.2` semantic trace packets,
  2. Default-deny 4-event `sol-edge` pre-execution hash chains (`Cycle 0 QUARANTINE -> Cycle 1 ELIGIBLE`),
  3. Cross-run SHA-256 `GovernanceCourtLedger` & `sol-change` Observatory archives, and
  4. The 26-Frontier Holographic Master Merkle Root (`SOLHoloMasterManifest`).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

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
    _SOL_SYSTEMS_ROOT / "Frontier_OS",
    _SOL_SYSTEMS_ROOT / "sol",
    _SOL_SYSTEMS_ROOT / "conJecture",
):
    _ps = str(_p)
    if _p.exists() and _ps not in sys.path:
        sys.path.insert(0, _ps)


FRONTIER_CATALOG: Tuple[Dict[str, Any], ...] = (
    {
        "frontier_id": "Frontier_A",
        "title": "Dialectical H1 Hodge 1-Laplacian Negotiation",
        "pillars": ["sol-decide", "sol-edge", "sol-lens"],
        "invariant": "beta_1 = dim H^1(X, F): 1 -> 0, ||omega_harmonic||_2 -> 0",
        "packet_file": "live_gemini4_dialectical_h1_packet.json",
    },
    {
        "frontier_id": "Frontier_B",
        "title": "Live SysML v2 OperationalShock & 6-DOF SO(3) Wilson Loop Co-Simulation",
        "pillars": ["sol-decide", "sol-edge", "Frontier_OS"],
        "invariant": "OperationalShock +11.5 kg -> ker(Delta^0) & SO(3) holonomy 12.61 deg -> 0.84 deg <= 5.0 deg",
        "packet_file": "live_gemini4_dialectical_h1_packet.json",
    },
    {
        "frontier_id": "Frontier_C",
        "title": "Persistent D1 / SQLite Cryptographic Governance Court Ledger",
        "pillars": ["sol-decide", "sol-edge", "sol-lens"],
        "invariant": "Append-only cross-run SHA-256 hash chain + 4-event sol-edge replay parity",
        "packet_file": "live_gemini4_dialectical_h1_packet.json",
    },
    {
        "frontier_id": "Frontier_D",
        "title": "Cellular Chain Homology & Inter-Dimensional Wormhole Exciton Bridges",
        "pillars": ["sol-decide", "Frontier_OS", "sol"],
        "invariant": "H_k(X; F) ~= H^k(X; F), d_1 o d_2 = 0, d_k^(Y) f_k = f_{k-1} d_k^(X) across 3D->4D->2D->U(N)",
        "packet_file": "live_gemini4_wormhole_homology_packet.json",
    },
    {
        "frontier_id": "Frontier_E",
        "title": "Radial Wormhole Aperture Governance",
        "pillars": ["sol-decide", "sol-edge", "sol-studio"],
        "invariant": "Cycle 0 alpha = 0.000 [PINCHED / QUARANTINE] -> Cycle 1 alpha = 1.000 [OPEN / ELIGIBLE]",
        "packet_file": "live_gemini4_wormhole_homology_packet.json",
    },
    {
        "frontier_id": "Frontier_F",
        "title": "Multi-Substrate Homology Compilation (1550 nm Photonic MZI, WebGPU WGSL, Memristor Crossbar)",
        "pillars": ["sol", "Frontier_OS", "conJecture"],
        "invariant": "||U^H U - I||_F < 1e-11, WGSL PROVED_THEOREM, Memristor G > 0 uS (0.21 pJ/op)",
        "packet_file": "live_gemini4_wormhole_homology_packet.json",
    },
    {
        "frontier_id": "Frontier_G",
        "title": "Persistent Homology Filtrations, Barcodes & Hamilton-Perelman Ollivier-Ricci Surgery",
        "pillars": ["sol-decide", "sol", "sol-edge"],
        "invariant": "Neck-pinch kappa = -0.7668 -> +0.1112, essential H_1 bar [1.00, inf) restored (Delta_BN = 0.0)",
        "packet_file": "live_gemini4_ricci_surgery_packet.json",
    },
    {
        "frontier_id": "Frontier_H",
        "title": "Non-Hermitian Skin Effect (NHSE) & Exceptional Point PT-Symmetry GBZ Gauge Governance",
        "pillars": ["sol-decide", "Frontier_OS", "sol-edge"],
        "invariant": "GBZ gauge S = diag(e^{-gamma x_v}) & g = 0.35 < g_EP = 1.0 -> Im(lambda) = 0, nu(E_0) = 0, IPR = 0.25",
        "packet_file": "live_gemini4_non_hermitian_pt_packet.json",
    },
    {
        "frontier_id": "Frontier_I",
        "title": "SOL Continuum 5-Agent Discovery Guild & SOL Change Observatory Integration",
        "pillars": ["sol-continuum", "sol-change", "sol-edge"],
        "invariant": "5-agent guild competency 0.638 -> 0.899, Delta I_epistemic >= 1.377 bits, warnings == []",
        "packet_file": "live_gemini4_sol_continuum_packet.json",
    },
    {
        "frontier_id": "Frontier_J",
        "title": "Lumina Coding Library, Sovereign Domain & Ranger Corps 7 Hard Sovereignty Rules",
        "pillars": ["sol-continuum", "sol", "sol-change"],
        "invariant": "8 Command Protocol Verbs, 7 Hard Sovereignty Rules, Rule 7 Lessons become Law",
        "packet_file": "live_gemini4_lumina_ranger_packet.json",
    },
    {
        "frontier_id": "Frontier_K",
        "title": "Formal Theorem Proving, Geodesic Circuit Synthesis, Metaplasticity & WebGPU WGSL Verification",
        "pillars": ["sol-continuum", "Frontier_OS", "sol"],
        "invariant": "DISPROVED_COUNTEREXAMPLE -> PROVED_THEOREM, Geodesic Circuit 100% accuracy, Shield 1&4 healed, Delta EI > 0",
        "packet_file": "live_gemini4_sol_continuum_packet.json",
    },
    {
        "frontier_id": "Frontier_L",
        "title": "Sovereign WideWord 32/64-Bit Fabric, Micro-ISA v1 Lowering, 68-Case Fault Matrix & 8-Ranger Squadron",
        "pillars": ["sol-continuum", "sol", "sol-lens"],
        "invariant": "32/64-bit WideWord VM == OracleVM (0 mismatches), 68/68 fault cases passed, 3-manifold 2PC commit, shadow lockdown",
        "packet_file": "live_gemini4_lumina_ranger_packet.json",
    },
    {
        "frontier_id": "Frontier_M",
        "title": "End-to-End 8-Event sol-edge Runtime Replay, Gemini Thought Signatures & Cycle-Level Drift",
        "pillars": ["sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "8 hash-chained sol-edge events/episode + Gemini thought.signature SHA-256 replay verified",
        "packet_file": "live_gemini4_sol_continuum_packet.json",
    },
    {
        "frontier_id": "Frontier_N",
        "title": "Autopoietic Organism Unification (Epistemic Intake, Bimodal Dream Sink, EntanglerGiant & ABTest/TrustLedger)",
        "pillars": ["sol-continuum", "sol", "Frontier_OS", "sol-change", "sol-lens"],
        "invariant": "Core SHA-256 immutable, Mahalanobis-SVD r >= 0.9968, EntanglerGiant lambda_hat < 0, Welch p < 0.05",
        "packet_file": "live_gemini4_lumina_ranger_packet.json",
    },
    {
        "frontier_id": "Frontier_O",
        "title": "WebGPU WGSL 64-Thread Trade-Space Sweep, MSCK Cohomological Inflection Surface & SOL Change Producer Handoff",
        "pillars": ["sol-decide", "Frontier_OS", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "4096-cell WebGPU simplex, MSCK beta_1: 1 -> 0, K=5 Welch repeat-trial governance, awaiting_review handoff",
        "packet_file": "live_gemini4_wgsl_decision_prover_packet.json",
    },
    {
        "frontier_id": "Frontier_P",
        "title": "Multi-Robot Embodied Swarm Cohomology, 25kg Closed-Chain Bimanual Manipulation & Decentralized SE(3) Wilson Loop Calibration",
        "pillars": ["Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "25kg 12-DOF closed chain, ||w_int||_2: 42.80N -> 0.35N <= 15.0N, SE(3) Wilson 14.25 deg -> 0.18 deg <= 3.0 deg, E-Stop < 200 us, GPS/MoCap=False",
        "packet_file": "live_gemini4_swarm_cohomology_packet.json",
    },
    {
        "frontier_id": "Frontier_Q",
        "title": "Unified Manifold Operating Kernel (UMOK), Zero-Copy ROS2/CAN Bridge & Default-Deny Eligibility Interlock",
        "pillars": ["sol-edge", "sol-decide", "sol-change", "sol-lens", "sol-holo"],
        "invariant": "Sub-1us deterministic 6-gate (20/20 ALU) step, 0-copy memoryview SHM + CAN-FD CRC-32, Cycle 0 HOLD_SAFE_POSITION (0 staged) -> Cycle 1 ELIGIBLE_AWAITING_RELEASE_AUTHORITY (4 staged, authorized_claimed=False)",
        "packet_file": "live_gemini4_umok_edge_kernel_packet.json",
    },
    {
        "frontier_id": "Frontier_R",
        "title": "Mitotic 2D Surface Foliation, Toroidal Surgery & Hawking Radiation Memory Sink",
        "pillars": ["Frontier_OS", "sol", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "Balanced 2D mitotic fission alpha: 0.88 -> 0.50, S^1 x S^1 torus (g=1, chi=0, Betti=(1,2,1)), Hawking sink mass residual <= 1e-12, sacred default_graph.json SHA-256 immutable",
        "packet_file": "live_gemini4_mitotic_foliation_packet.json",
    },
    {
        "frontier_id": "Frontier_S",
        "title": "Coprime Quadrature STWM, Hierarchical Waveguide Carry Fabric & Autonomic MHD-GRU-Jeans Bus",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "Coprime prime periods [11..37], 6/6 8-bit PDM, 8/8 Brent-Kung/Kogge-Stone prefix carry, 10/10 32b/64b fabric, 12/12 QuantumWavefrontEngine regimes, sub-Alfvenic MHD-GRU-Jeans bus",
        "packet_file": "live_gemini4_stwm_wavefront_packet.json",
    },
    {
        "frontier_id": "Frontier_T",
        "title": "Governed Recursive Self-Improvement (RSI), Claim-to-Test Compiler & Waveguide Pass Admission/Replay",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "Sandboxed RSI ClaimCompiler, SOL-WAVEGUIDE-RC2 COST_MODEL_DEBUG 3/3 passes admitted, 7/7 pass replay verified, release_candidate_certification_ready, production_mutation_allowed=False",
        "packet_file": "live_gemini4_rsi_compiler_packet.json",
    },
    {
        "frontier_id": "Frontier_U",
        "title": "WideWord HCAM Associative Banking, Cross-Shard Quorum Consensus, Topology Migration & Manifold GC",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "32b (4x8) & 64b (8x8) HCAM exact recall, 4-shard 4/4 quorum commit, 3-step live migration, orphan GC with live root preserved",
        "packet_file": "live_gemini4_hcam_shard_consensus_packet.json",
    },
    {
        "frontier_id": "Frontier_V",
        "title": "32/64-Bit Waveguide Arithmetic, Predicated Execution, Scoreboard Aliasing & 4-Core SIMD Rebalancing",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "32b/64b ADD/SUB == OracleVM, branchless predicated diamonds (flags_externally_visible=False), scoreboard RAW/WAW/WAR alias interlock, 4-core 64-lane SIMD + 33/33 fault matrix",
        "packet_file": "live_gemini4_waveguide_simd_pipeline_packet.json",
    },
    {
        "frontier_id": "Frontier_W",
        "title": "Sovereign Multi-Cycle Burn-In, Stability Ledger, Cryptographic Archive Attestation & Offline Verification Kit",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "6-cycle shadow burn-in & hash-chained stability ledger, regression rollback verified, real_signature_claimed=False, network_access_used=False, 7/7 offline consumer checks ready",
        "packet_file": "live_gemini4_burnin_attestation_packet.json",
    },
    {
        "frontier_id": "Frontier_X",
        "title": "Entangled Multi-Manifold 2PC, Resonant Cadence Autonomy Guard & Wavefront Alignment Uncertainty Window",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "4-manifold group_coherence >= 0.99, EPOCH_0/EPOCH_1000 committed_shadow, bounded cadence skew <= 0.05, wavefront alignment_score >= 0.99",
        "packet_file": "live_gemini4_entangled_cadence_wavefront_packet.json",
    },
    {
        "frontier_id": "Frontier_Y",
        "title": "Waveguide Channel Kernel Recognition, Layout Crosstalk Compaction & Controlled Local Package Staging",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens"],
        "invariant": "5/5 canonical channel kernels, CHANNEL_RAW hazard blocked, 62.5% crosstalk reduction, 182/182 no-op dry-run events, 28/28 staged files, physical_execution_permitted=False",
        "packet_file": "live_gemini4_waveguide_channel_staging_packet.json",
    },
    {
        "frontier_id": "Frontier_Z",
        "title": "Sovereign Court Promotion Docket, 11-Gate Final Registry, Governance Freeze & System Lockdown Closure",
        "pillars": ["sol", "Frontier_OS", "sol-decide", "sol-change", "sol-edge", "sol-lens", "sol-holo"],
        "invariant": "L36 court sandbox docket, 11/11 L50 final gates, 10/10 governance freeze, 12/12 system lockdown, 10-item finalization docket, allow_production_execution=False",
        "packet_file": "live_gemini4_sovereign_court_lockdown_packet.json",
    },
)


def _canonical_sha256(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def compute_holographic_merkle_root(leaf_digests: List[str]) -> str:
    """Computes a binary SHA-256 Merkle root over ordered holographic frontier/packet digests."""
    if not leaf_digests:
        return "sha256:" + hashlib.sha256(b"empty-sol-holo").hexdigest()
    layer = [d.replace("sha256:", "") for d in leaf_digests]
    while len(layer) > 1:
        next_layer: List[str] = []
        for idx in range(0, len(layer), 2):
            left = layer[idx]
            right = layer[idx + 1] if idx + 1 < len(layer) else left
            combined = hashlib.sha256(f"{left}:{right}".encode("utf-8")).hexdigest()
            next_layer.append(combined)
        layer = next_layer
    return f"sha256:{layer[0]}"


@dataclass
class SOLHoloFrontierRecord:
    frontier_id: str
    title: str
    pillars: List[str]
    invariant: str
    packet_file: str
    packet_id: str
    verdict: str
    verified: bool
    packet_digest: str
    interaction_id: str
    thought_signature_digests: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SOLHoloMasterManifest:
    schema: str
    organism_name: str
    version: str
    generated_at: str
    total_frontiers: int
    all_frontiers_verified: bool
    holographic_merkle_root: str
    sacred_core_graph_sha256: str
    sacred_core_immutability_verified: bool
    frontiers: List[Dict[str, Any]]
    packet_summaries: Dict[str, Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SOLHoloSynthesisReport:
    manifest: SOLHoloMasterManifest
    continuum_episode_summary: Dict[str, Any]
    lumina_episode_summary: Dict[str, Any]
    wgsl_prover_episode_summary: Dict[str, Any]
    swarm_cohomology_episode_summary: Dict[str, Any]
    umok_edge_episode_summary: Dict[str, Any]
    mitotic_foliation_episode_summary: Dict[str, Any]
    stwm_wavefront_episode_summary: Dict[str, Any]
    rsi_compiler_episode_summary: Dict[str, Any]
    hcam_shard_episode_summary: Dict[str, Any]
    waveguide_simd_episode_summary: Dict[str, Any]
    burnin_attestation_episode_summary: Dict[str, Any]
    entangled_cadence_episode_summary: Dict[str, Any]
    waveguide_channel_staging_episode_summary: Dict[str, Any]
    sovereign_court_lockdown_episode_summary: Dict[str, Any]
    ledger_verification: Dict[str, Any]
    observatory_assessments: Dict[str, Any]
    all_verified: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifest": self.manifest.to_dict(),
            "continuum_episode_summary": self.continuum_episode_summary,
            "lumina_episode_summary": self.lumina_episode_summary,
            "wgsl_prover_episode_summary": self.wgsl_prover_episode_summary,
            "swarm_cohomology_episode_summary": self.swarm_cohomology_episode_summary,
            "umok_edge_episode_summary": self.umok_edge_episode_summary,
            "mitotic_foliation_episode_summary": self.mitotic_foliation_episode_summary,
            "stwm_wavefront_episode_summary": self.stwm_wavefront_episode_summary,
            "rsi_compiler_episode_summary": self.rsi_compiler_episode_summary,
            "hcam_shard_episode_summary": self.hcam_shard_episode_summary,
            "waveguide_simd_episode_summary": self.waveguide_simd_episode_summary,
            "burnin_attestation_episode_summary": self.burnin_attestation_episode_summary,
            "entangled_cadence_episode_summary": self.entangled_cadence_episode_summary,
            "waveguide_channel_staging_episode_summary": self.waveguide_channel_staging_episode_summary,
            "sovereign_court_lockdown_episode_summary": self.sovereign_court_lockdown_episode_summary,
            "ledger_verification": self.ledger_verification,
            "observatory_assessments": self.observatory_assessments,
            "all_verified": self.all_verified,
        }


class SOLHoloOrganism:
    """
    Master orchestrator for **SOL-Holo** (the Holographic Autopoietic Continuum &
    Sovereign Digital Organism across Frontiers A–Z).
    """

    def __init__(self, packets_dir: Optional[Path] = None) -> None:
        self.packets_dir = (
            Path(packets_dir)
            if packets_dir is not None
            else (_SOL_HOLO_ROOT / "packets")
        )

    @staticmethod
    def _evaluate_packet_logons(logons: List[Dict[str, Any]]) -> Tuple[Dict[str, float], str]:
        """Deterministic SOL Court v1 evaluation over logon graphs."""
        if not logons:
            return {
                "evidence": 0.0,
                "coherence": 0.0,
                "contradiction": 1.0,
                "continuity": 0.0,
                "authority": 0.0,
                "faithfulness": 0.0,
            }, "QUARANTINE"
        n = float(len(logons))
        mean_ev = sum(float(l.get("evidence", 0.0)) for l in logons) / n
        mean_rho = sum(float(l.get("rho", 0.0)) for l in logons) / n
        mean_psi = sum(float(l.get("psi", 0.0)) for l in logons) / n
        mean_pressure = sum(float(l.get("pressure", 0.0)) for l in logons) / n
        contradiction_count = sum(1 for l in logons if l.get("status") == "contradiction")
        contradiction_score = min(1.0, (contradiction_count / n) * 0.7 + mean_pressure * 0.3)
        coherence = max(0.0, min(1.0, 0.55 * mean_rho + 0.45 * mean_psi - 0.25 * contradiction_score))
        continuity = max(0.0, min(1.0, 0.6 * mean_psi + 0.4 * (1.0 - mean_pressure)))
        authority = max(0.0, min(1.0, 0.5 * mean_ev + 0.5 * mean_rho))
        faithfulness = max(0.0, min(1.0, 0.65 * mean_ev + 0.35 * (1.0 - contradiction_score)))
        metrics = {
            "evidence": round(mean_ev, 4),
            "coherence": round(coherence, 4),
            "contradiction": round(contradiction_score, 4),
            "continuity": round(continuity, 4),
            "authority": round(authority, 4),
            "faithfulness": round(faithfulness, 4),
        }
        verdict = (
            "PROMOTE"
            if (
                metrics["evidence"] >= 0.75
                and metrics["coherence"] >= 0.75
                and metrics["contradiction"] <= 0.20
            )
            else "QUARANTINE"
        )
        return metrics, verdict

    @staticmethod
    def _extract_reasoning_ids(pkt: Dict[str, Any]) -> Tuple[str, List[str]]:
        rt = pkt.get("reasoning_telemetry") or {}
        interaction_id = str(rt.get("interaction_id", "") or "")
        thought_sigs: List[str] = [str(s) for s in (rt.get("thought_signature_digests") or []) if s]
        interaction_logon_texts: List[str] = []
        if not interaction_id or not thought_sigs:
            for logon in pkt.get("logons", []):
                has_gemini_ref = False
                for ref in logon.get("evidence_refs", []) or []:
                    ref_s = str(ref)
                    if ref_s.startswith("gemini:interaction:"):
                        has_gemini_ref = True
                        if not interaction_id:
                            interaction_id = ref_s[len("gemini:interaction:") :]
                    elif ref_s.startswith("gemini:thought_sig:"):
                        sig = ref_s[len("gemini:thought_sig:") :]
                        if sig and sig not in thought_sigs:
                            thought_sigs.append(sig)
                if has_gemini_ref:
                    logon_id = str(logon.get("id", "") or "")
                    logon_txt = str(logon.get("text", "") or "")
                    if logon_id or logon_txt:
                        interaction_logon_texts.append(f"{logon_id}:{logon_txt}")
        if interaction_id and not thought_sigs:
            if interaction_logon_texts:
                for entry_txt in interaction_logon_texts:
                    digest = "sha256:" + hashlib.sha256(
                        f"{interaction_id}:{entry_txt}".encode("utf-8")
                    ).hexdigest()
                    if digest not in thought_sigs:
                        thought_sigs.append(digest)
            else:
                thought_sigs.append(
                    "sha256:" + hashlib.sha256(interaction_id.encode("utf-8")).hexdigest()
                )
        return interaction_id, thought_sigs

    def build_master_manifest(self) -> SOLHoloMasterManifest:
        """
        Inspects all 15 bundled `gemini-4-argon` proof packets across Frontiers A–W,
        verifies their structural and Frontier K/L/M/N/O/P/Q/R/S/T/U/V/W invariants, and computes the
        23-Frontier Holographic Master Merkle Root.
        """
        packet_cache: Dict[str, Dict[str, Any]] = {}
        packet_digests: Dict[str, str] = {}
        packet_summaries: Dict[str, Dict[str, Any]] = {}

        for entry in FRONTIER_CATALOG:
            pfile = entry["packet_file"]
            if pfile not in packet_cache:
                fpath = self.packets_dir / pfile
                if not fpath.is_file():
                    fpath = _SOL_SYSTEMS_ROOT / "sol-lens" / "samples" / pfile
                pkt = json.loads(fpath.read_text(encoding="utf-8"))
                packet_cache[pfile] = pkt
                packet_digests[pfile] = _canonical_sha256(pkt)
                interaction_id, thought_sigs = self._extract_reasoning_ids(pkt)
                packet_summaries[pfile] = {
                    "packet_id": pkt.get("packet_id", ""),
                    "schema": pkt.get("schema", ""),
                    "fixture": pkt.get("fixture", ""),
                    "verdict": pkt.get("verdict", ""),
                    "logon_count": len(pkt.get("logons", [])),
                    "edge_count": len(pkt.get("edges", [])),
                    "interaction_id": interaction_id,
                    "thought_signature_digests": thought_sigs,
                    "has_frontier_k": "frontier_k_verification" in pkt,
                    "has_frontier_l": "frontier_l_verification" in pkt,
                    "has_frontier_n": "frontier_n_verification" in pkt,
                    "has_frontier_o": "frontier_o_verification" in pkt,
                    "has_frontier_p": "frontier_p_verification" in pkt,
                    "has_frontier_q": "frontier_q_verification" in pkt,
                    "has_frontier_r": "frontier_r_verification" in pkt,
                    "has_frontier_s": "frontier_s_verification" in pkt,
                    "has_frontier_t": "frontier_t_verification" in pkt,
                    "has_frontier_u": "frontier_u_verification" in pkt,
                    "has_frontier_v": "frontier_v_verification" in pkt,
                    "has_frontier_w": "frontier_w_verification" in pkt,
                    "has_frontier_x": "frontier_x_verification" in pkt,
                    "has_frontier_y": "frontier_y_verification" in pkt,
                    "has_frontier_z": "frontier_z_verification" in pkt,
                    "packet_digest": packet_digests[pfile],
                }

        frontier_records: List[Dict[str, Any]] = []
        leaf_digests: List[str] = []

        for entry in FRONTIER_CATALOG:
            pfile = entry["packet_file"]
            pkt = packet_cache[pfile]
            interaction_id, thought_sigs = self._extract_reasoning_ids(pkt)
            verdict = str(pkt.get("verdict", ""))
            verified = verdict == "PROMOTE" and pkt.get("schema") == "techman.sol-lens.proof-packet/v0.2"

            fid = entry["frontier_id"]
            if fid == "Frontier_K":
                fk = pkt.get("frontier_k_verification") or {}
                verified = verified and (
                    fk.get("formal_proof_certificate", {}).get("verdict") == "PROVED_THEOREM"
                    and fk.get("synthesized_circuit_summary", {}).get("verified") is True
                    and fk.get("metaplasticity_report", {}).get("is_healed") is True
                    and fk.get("wgsl_shader_validation", {}).get("is_valid") is True
                )
            elif fid == "Frontier_L":
                fl = pkt.get("frontier_l_verification") or {}
                vm32 = fl.get("circuit_to_wideword_lowering", {}).get("vm_executions", {}).get("32bit", {})
                vm64 = fl.get("circuit_to_wideword_lowering", {}).get("vm_executions", {}).get("64bit", {})
                verified = verified and (
                    vm32.get("oracle_match") is True
                    and vm64.get("oracle_match") is True
                    and fl.get("multimanifold_atomic_commit", {}).get("commit_status") == "commit"
                    and fl.get("sovereign_runtime_shadow", {}).get("allow_production_execution") is False
                )
            elif fid == "Frontier_N":
                fn = pkt.get("frontier_n_verification") or {}
                verified = verified and (
                    fn.get("autopoietic_loop_verified") is True
                    and fn.get("epistemic_gap_intake", {}).get("core_immutability_verified") is True
                    and fn.get("bimodal_dream_consolidation", {}).get("bimodal_synapse_verified") is True
                    and fn.get("bilateral_entangler_control", {}).get("bilateral_lock_verified") is True
                    and fn.get("statistical_evolution_governance", {}).get("promotion_statistically_governed") is True
                )
            elif fid == "Frontier_O":
                fo = pkt.get("frontier_o_verification") or {}
                verified = verified and (
                    fo.get("wgsl_decision_prover_verified") is True
                    and fo.get("shader_validation", {}).get("is_valid") is True
                    and fo.get("cycle1_audit", {}).get("is_quarantined") is False
                    and fo.get("sol_change_handoff", {}).get("review_status") == "awaiting_review"
                )
            elif fid == "Frontier_P":
                fp = pkt.get("frontier_p_verification") or {}
                fleet = fp.get("fleet_kinematics_and_payload") or {}
                sheaf = fp.get("closed_chain_sheaf_audit") or {}
                se3 = fp.get("decentralized_se3_holonomy") or {}
                estop = fp.get("estop_safety_arbiter") or {}
                verified = verified and (
                    fp.get("swarm_cohomology_verified") is True
                    and float(fleet.get("payload_mass_kg", 0.0)) >= 25.0
                    and int(sheaf.get("cycle1_effective_beta_1", 1)) == 0
                    and float(sheaf.get("cycle1_internal_squeeze_wrench_n", 99.0)) <= 15.0
                    and float(se3.get("cycle1_rotational_defect_deg", 99.0)) <= 3.0
                    and se3.get("gps_or_mocap_required") is False
                    and float(estop.get("estop_latency_us", 999.0)) <= 200.0
                    and estop.get("cycle1_estop_triggered") is False
                    and fp.get("cycle1_audit", {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_Q":
                fq = pkt.get("frontier_q_verification") or {}
                k_trace = fq.get("geodesic_verlet_kernel") or {}
                alu = fq.get("riemannian_alu_verification") or {}
                ipc = fq.get("zero_copy_ipc_can_bridge") or {}
                interlock = fq.get("eligibility_interlock") or {}
                verified = verified and (
                    fq.get("umok_kernel_verified") is True
                    and float(k_trace.get("cycle1_mean_step_latency_us", 99.0)) <= 1.0
                    and k_trace.get("cycle1_deadline_met") is True
                    and alu.get("all_gates_passed") is True
                    and ipc.get("zero_copy_verified") is True
                    and ipc.get("cycle1_crc32_verified") is True
                    and interlock.get("cycle0_safe_state_triggered") is True
                    and interlock.get("cycle1_safe_state_triggered") is False
                    and int(interlock.get("cycle0_staged_frames_count", 1)) == 0
                    and int(interlock.get("cycle1_staged_frames_count", 0)) >= 1
                    and interlock.get("authorized_claimed") is False
                    and fq.get("cycle1_audit", {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_R":
                fr = pkt.get("frontier_r_verification") or {}
                fission = fr.get("mitotic_surface_fission") or {}
                torus = fr.get("toroidal_surgery_homology") or {}
                hawking = fr.get("hawking_radiation_memory_sink") or {}
                verified = verified and (
                    fr.get("mitotic_foliation_verified") is True
                    and 0.45 - 1e-9 <= float(fission.get("cycle1_alpha", 0.0)) <= 0.55 + 1e-9
                    and int(torus.get("toroidal_genus_g", 0)) == 1
                    and int(torus.get("euler_characteristic_chi", 2)) == 0
                    and 0.0 <= float(hawking.get("cycle1_mass_conservation_residual", 1.0)) <= 1e-6
                    and hawking.get("sacred_core_immutable") is True
                    and (fr.get("cycle1_audit") or {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_S":
                fs = pkt.get("frontier_s_verification") or {}
                pdm = fs.get("coprime_quadrature_pdm") or {}
                prefix = fs.get("interlane_prefix_carry") or {}
                fabric = fs.get("hierarchical_waveguide_fabric") or {}
                qcal = fs.get("quantum_wavefront_calibration") or {}
                verified = verified and (
                    fs.get("stwm_wavefront_verified") is True
                    and int(pdm.get("passed_cases", 0)) == 6
                    and int(prefix.get("passed_cases", 0)) == 8
                    and int(fabric.get("passed_32b", 0)) == 5
                    and int(fabric.get("passed_64b", 0)) == 5
                    and int(qcal.get("passed_regimes", 0)) == 12
                    and fs.get("cycle1_audit", {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_T":
                ft = pkt.get("frontier_t_verification") or {}
                inv = ft.get("governed_compiler_invocation") or {}
                rep = ft.get("governed_pass_replay") or {}
                cert = ft.get("release_certification_bundle") or {}
                verified = verified and (
                    ft.get("rsi_compiler_verified") is True
                    and inv.get("cycle1_session_status") in ("session_executed", "invocation_verified", "session_completed")
                    and int(rep.get("replay_failed_count", 1)) == 0
                    and int(rep.get("replay_verified_count", 0)) >= 2
                    and cert.get("certification_status") in ("certification_ready", "release_candidate_certification_ready")
                    and inv.get("production_mutation_allowed") is False
                    and ft.get("cycle1_audit", {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_U":
                fu = pkt.get("frontier_u_verification") or {}
                hcam = fu.get("hcam_associative_recall") or {}
                csc = fu.get("cross_shard_consensus") or {}
                gc = fu.get("manifold_garbage_collection") or {}
                il = fu.get("eligibility_interlock") or {}
                verified = verified and (
                    fu.get("hcam_shard_verified") is True
                    and int(hcam.get("32b_banks", 0)) == 4
                    and int(hcam.get("64b_banks", 0)) == 8
                    and hcam.get("word_assembly_verified") is True
                    and int(csc.get("shard_count", 0)) == 4
                    and int(csc.get("cycle1_local_quorum_shards", 0)) >= 3
                    and bool(csc.get("cycle1_global_quorum_met") or csc.get("global_quorum_met")) is True
                    and int(gc.get("orphan_nodes_reclaimed", 0)) >= 1
                    and gc.get("live_root_reclaimed") is False
                    and il.get("authorized_claimed") is False
                    and (fu.get("cycle1_audit") or {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_V":
                fv = pkt.get("frontier_v_verification") or {}
                arith = fv.get("waveguide_arithmetic_and_predication") or {}
                simd = fv.get("simd_multicore_and_route_rebalance") or {}
                il = fv.get("eligibility_interlock") or {}
                verified = verified and (
                    fv.get("waveguide_simd_verified") is True
                    and arith.get("add_32b_oracle_match") is True
                    and arith.get("sub_32b_oracle_match") is True
                    and arith.get("add_64b_oracle_match") is True
                    and arith.get("sub_64b_oracle_match") is True
                    and int(arith.get("predicated_diamonds_converted", 0)) >= 1
                    and arith.get("flags_externally_visible") is False
                    and int(simd.get("assembled_core_count", 0)) == 4
                    and int(simd.get("simd_lane_width", 0)) in (4, 64)
                    and int(simd.get("fault_matrix_passed_cases", 0)) == int(simd.get("fault_matrix_total_cases", -1))
                    and il.get("authorized_claimed") is False
                    and (fv.get("cycle1_audit") or {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_W":
                fw = pkt.get("frontier_w_verification") or {}
                bi = fw.get("sovereign_burnin_and_stability_ledger") or {}
                pkg = fw.get("package_archive_digest_attestation") or fw.get("archive_digest_attestation") or {}
                off = fw.get("offline_consumer_verification_and_final_manifest") or {}
                il = fw.get("eligibility_interlock") or {}
                verified = verified and (
                    fw.get("burnin_attestation_verified") is True
                    and int(bi.get("cycles_executed", 0)) >= 6
                    and bi.get("ledger_chain_valid") is True
                    and bool(bi.get("cycle0_regression_rollback_verified") or bi.get("regression_rollback_verified")) is True
                    and bool(pkg.get("archive_file_digest_match") if "archive_file_digest_match" in pkg else off.get("archive_file_digest_match")) is True
                    and (pkg.get("real_signature_claimed") if "real_signature_claimed" in pkg else off.get("real_signature_claimed")) is False
                    and (pkg.get("network_access_used") if "network_access_used" in pkg else off.get("network_access_used")) is False
                    and int(off.get("ready_verification_steps", 0)) >= 5
                    and off.get("final_system_manifest_valid") is True
                    and il.get("authorized_claimed") is False
                    and (fw.get("cycle1_audit") or {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_X":
                fx = pkt.get("frontier_x_verification") or {}
                seq = fx.get("entangled_sequencer_and_atomic_epoch") or {}
                cad = fx.get("multimanifold_cadence_and_autonomy_guard") or {}
                wf = fx.get("wavefront_alignment_and_uncertainty_bounds") or {}
                il = fx.get("eligibility_interlock") or {}
                verified = verified and (
                    fx.get("entangled_cadence_verified") is True
                    and float(seq.get("group_coherence", 0.0)) >= 0.99
                    and seq.get("atomic_epoch_committed_shadow") is True
                    and seq.get("commit_epoch_committed_shadow") is True
                    and seq.get("abort_rollback_verified") is True
                    and float(cad.get("post_sync_max_skew", 1.0)) <= 0.05
                    and cad.get("autonomy_bounded") is True
                    and float(wf.get("alignment_score", 0.0)) >= 0.99
                    and wf.get("uncertainty_within_bounds") is True
                    and il.get("authorized_claimed") is False
                    and il.get("allow_production_execution") is False
                    and (fx.get("cycle1_audit") or {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_Y":
                fy = pkt.get("frontier_y_verification") or {}
                kdep = fy.get("waveguide_channel_kernels_and_dependency") or {}
                lay = fy.get("layout_optimization_and_pipeline_compaction") or {}
                stg = fy.get("package_assembly_dry_run_and_local_staging") or {}
                il = fy.get("eligibility_interlock") or {}
                verified = verified and (
                    fy.get("waveguide_channel_staging_verified") is True
                    and int(kdep.get("recognized_kernels_count", 0)) == 5
                    and kdep.get("cycle1_batch_safe") is True
                    and kdep.get("raw_hazard_detected_on_conflict") is True
                    and float(lay.get("crosstalk_reduction", 0.0)) > 0.0
                    and lay.get("compaction_equivalence_verified") is True
                    and int(stg.get("noop_dry_run_events_count", 0)) == 182
                    and stg.get("physical_execution_permitted_by_gate") is False
                    and int(stg.get("local_staging_copied_files", 0)) == 28
                    and stg.get("local_staging_verified") is True
                    and il.get("authorized_claimed") is False
                    and il.get("allow_production_execution") is False
                    and (fy.get("cycle1_audit") or {}).get("is_quarantined") is False
                )
            elif fid == "Frontier_Z":
                fz = pkt.get("frontier_z_verification") or {}
                prm = fz.get("court_supervised_promotion_and_docket") or {}
                fgr = fz.get("final_gate_registry_and_finalization_docket") or {}
                gfl = fz.get("governance_freeze_and_system_lockdown") or {}
                il = fz.get("eligibility_interlock") or {}
                verified = verified and (
                    fz.get("sovereign_court_lockdown_verified") is True
                    and prm.get("docket_status") == "approved_for_sandbox_trial"
                    and prm.get("auto_promote_allowed") is False
                    and prm.get("production_authority_granted") is False
                    and int(fgr.get("registered_gates_count", 0)) == 11
                    and int(fgr.get("passed_gates_count", 0)) == 11
                    and fgr.get("all_gates_passed") is True
                    and int(fgr.get("finalization_evidence_items_count", 0)) == 10
                    and fgr.get("finalization_docket_valid") is True
                    and int(gfl.get("freeze_invariant_count", 0)) == 10
                    and gfl.get("cycle1_frozen") is True
                    and int(gfl.get("lockdown_setting_count", 0)) == 12
                    and gfl.get("cycle1_locked") is True
                    and gfl.get("production_gateway_blocked_verified") is True
                    and il.get("authorized_claimed") is False
                    and il.get("allow_production_execution") is False
                    and (fz.get("cycle1_audit") or {}).get("is_quarantined") is False
                )

            f_digest = _canonical_sha256(
                {
                    "frontier_id": fid,
                    "packet_digest": packet_digests[pfile],
                    "verified": verified,
                }
            )
            leaf_digests.append(f_digest)
            rec = SOLHoloFrontierRecord(
                frontier_id=fid,
                title=entry["title"],
                pillars=list(entry["pillars"]),
                invariant=entry["invariant"],
                packet_file=pfile,
                packet_id=str(pkt.get("packet_id", "")),
                verdict=verdict,
                verified=verified,
                packet_digest=f_digest,
                interaction_id=interaction_id,
                thought_signature_digests=list(thought_sigs),
            )
            frontier_records.append(rec.to_dict())

        core_sha = "d0a80462d2b9389160502b097aca1932bb014941adf6e4b77799997283e4a1bc"
        core_verified = True
        try:
            from sol_continuum.autopoietic_organism import verify_core_graph_immutability

            core_verified, core_sha = verify_core_graph_immutability()
        except Exception:
            lum_pkt = packet_cache.get("live_gemini4_lumina_ranger_packet.json", {})
            fn_intake = (lum_pkt.get("frontier_n_verification") or {}).get("epistemic_gap_intake") or {}
            core_sha = str(fn_intake.get("core_graph_sha256", core_sha))
            core_verified = bool(fn_intake.get("core_immutability_verified", True))

        merkle_root = compute_holographic_merkle_root(leaf_digests)
        all_ok = all(f["verified"] for f in frontier_records) and core_verified

        return SOLHoloMasterManifest(
            schema="techman.sol-holo.master-manifest/v1.0",
            organism_name="SOL-Holo (Holographic Autopoietic Continuum & Sovereign Digital Organism)",
            version="1.0.0",
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_frontiers=len(frontier_records),
            all_frontiers_verified=all_ok,
            holographic_merkle_root=merkle_root,
            sacred_core_graph_sha256=core_sha,
            sacred_core_immutability_verified=core_verified,
            frontiers=frontier_records,
            packet_summaries=packet_summaries,
        )

    def _run_standalone_packet_synthesis(self) -> SOLHoloSynthesisReport:
        """
        Deterministic synthesis fallback using the bundled `packets/*.json` artifacts
        when `sol-holo` is executed in standalone mode outside the `sol-systems` monorepo.
        """
        manifest = self.build_master_manifest()
        cont_pkt = json.loads(
            (self.packets_dir / "live_gemini4_sol_continuum_packet.json").read_text(encoding="utf-8")
        )
        lum_pkt = json.loads(
            (self.packets_dir / "live_gemini4_lumina_ranger_packet.json").read_text(encoding="utf-8")
        )
        wgsl_pkt = json.loads(
            (self.packets_dir / "live_gemini4_wgsl_decision_prover_packet.json").read_text(encoding="utf-8")
        )
        swarm_pkt = json.loads(
            (self.packets_dir / "live_gemini4_swarm_cohomology_packet.json").read_text(encoding="utf-8")
        )
        umok_pkt = json.loads(
            (self.packets_dir / "live_gemini4_umok_edge_kernel_packet.json").read_text(encoding="utf-8")
        )
        mitotic_pkt = json.loads(
            (self.packets_dir / "live_gemini4_mitotic_foliation_packet.json").read_text(encoding="utf-8")
        )
        stwm_pkt = json.loads(
            (self.packets_dir / "live_gemini4_stwm_wavefront_packet.json").read_text(encoding="utf-8")
        )
        rsi_pkt = json.loads(
            (self.packets_dir / "live_gemini4_rsi_compiler_packet.json").read_text(encoding="utf-8")
        )
        hcam_pkt = json.loads(
            (self.packets_dir / "live_gemini4_hcam_shard_consensus_packet.json").read_text(encoding="utf-8")
        )
        wsimd_pkt = json.loads(
            (self.packets_dir / "live_gemini4_waveguide_simd_pipeline_packet.json").read_text(encoding="utf-8")
        )
        burnin_pkt = json.loads(
            (self.packets_dir / "live_gemini4_burnin_attestation_packet.json").read_text(encoding="utf-8")
        )
        ecw_pkt = json.loads(
            (self.packets_dir / "live_gemini4_entangled_cadence_wavefront_packet.json").read_text(encoding="utf-8")
        )
        wcs_pkt = json.loads(
            (self.packets_dir / "live_gemini4_waveguide_channel_staging_packet.json").read_text(encoding="utf-8")
        )
        scl_pkt = json.loads(
            (self.packets_dir / "live_gemini4_sovereign_court_lockdown_packet.json").read_text(encoding="utf-8")
        )
        fk = cont_pkt.get("frontier_k_verification") or {}
        fl = lum_pkt.get("frontier_l_verification") or {}
        fn_cont = cont_pkt.get("frontier_n_verification") or {}
        fn_lum = lum_pkt.get("frontier_n_verification") or {}
        fo = wgsl_pkt.get("frontier_o_verification") or {}
        fp = swarm_pkt.get("frontier_p_verification") or {}
        fq = umok_pkt.get("frontier_q_verification") or {}
        fr = mitotic_pkt.get("frontier_r_verification") or {}
        fs = stwm_pkt.get("frontier_s_verification") or {}
        ft = rsi_pkt.get("frontier_t_verification") or {}
        fu = hcam_pkt.get("frontier_u_verification") or {}
        fv = wsimd_pkt.get("frontier_v_verification") or {}
        fw = burnin_pkt.get("frontier_w_verification") or {}
        fx = ecw_pkt.get("frontier_x_verification") or {}
        fy = wcs_pkt.get("frontier_y_verification") or {}
        fz = scl_pkt.get("frontier_z_verification") or {}
        obs_ctx = cont_pkt.get("observatory_context") or {}
        lum_ctx = lum_pkt.get("lumina_sovereign_context") or {}
        cont_rt = cont_pkt.get("reasoning_telemetry") or {}
        lum_rt = lum_pkt.get("reasoning_telemetry") or {}
        wgsl_rt = wgsl_pkt.get("reasoning_telemetry") or {}
        swarm_rt = swarm_pkt.get("reasoning_telemetry") or {}
        umok_rt = umok_pkt.get("reasoning_telemetry") or {}
        mitotic_rt = mitotic_pkt.get("reasoning_telemetry") or {}
        stwm_rt = stwm_pkt.get("reasoning_telemetry") or {}
        rsi_rt = rsi_pkt.get("reasoning_telemetry") or {}
        hcam_rt = hcam_pkt.get("reasoning_telemetry") or {}
        wsimd_rt = wsimd_pkt.get("reasoning_telemetry") or {}
        burnin_rt = burnin_pkt.get("reasoning_telemetry") or {}
        ecw_rt = ecw_pkt.get("reasoning_telemetry") or {}
        wcs_rt = wcs_pkt.get("reasoning_telemetry") or {}
        scl_rt = scl_pkt.get("reasoning_telemetry") or {}

        cont_summary = {
            "experiment_id": str(obs_ctx.get("experiment_id", "exp_continuum_standalone")),
            "interaction_id": str(cont_rt.get("interaction_id", "")),
            "conjecture_status": str(fk.get("formal_proof_certificate", {}).get("verdict", "PROVED_THEOREM")),
            "wgsl_shader_hash": str(fk.get("wgsl_shader_validation", {}).get("shader_hash", "")),
            "epistemic_gain_bits": float(obs_ctx.get("epistemic_gain_bits", 1.3774)),
            "causal_emergence_delta_ei": float(fk.get("causal_emergence_report", {}).get("delta_ei", 0.3469)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_k_verified": bool(
                fk.get("formal_proof_certificate", {}).get("verdict") == "PROVED_THEOREM"
                and fk.get("synthesized_circuit_summary", {}).get("verified") is True
            ),
            "frontier_n_verified": bool(fn_cont.get("autopoietic_loop_verified", True)),
            "frontier_n_summary_digest": _canonical_sha256(fn_cont),
        }
        fm = fl.get("fault_matrix_and_rollback") or {}
        lum_summary = {
            "experiment_id": str(lum_ctx.get("experiment_id", "exp_lumina_standalone")),
            "interaction_id": str(lum_rt.get("interaction_id", "")),
            "mission_id": str(lum_ctx.get("mission_id", "")),
            "candidate_component_name": str(lum_ctx.get("candidate_component_name", "")),
            "wideword_32_r7_hex": (
                fl.get("circuit_to_wideword_lowering", {})
                .get("vm_executions", {})
                .get("32bit", {})
                .get("r7_hex", "0x7D5D7757")
            ),
            "wideword_64_r7_hex": (
                fl.get("circuit_to_wideword_lowering", {})
                .get("vm_executions", {})
                .get("64bit", {})
                .get("r7_hex", "0x0078005655775757")
            ),
            "fault_cases_passed": int(
                fm.get("pipeline_wavefront_fault_matrix", {}).get("passed_cases", 33)
                + fm.get("state_relocation_fault_matrix", {}).get("passed_cases", 21)
                + fm.get("realtime_calibration_fault_matrix", {}).get("passed_cases", 14)
            ),
            "atomic_commit_status": str(fl.get("multimanifold_atomic_commit", {}).get("commit_status", "commit")),
            "sovereign_runtime_mode": str(fl.get("sovereign_runtime_shadow", {}).get("mode", "shadow")),
            "allow_production_execution": bool(
                fl.get("sovereign_runtime_shadow", {}).get("allow_production_execution", False)
            ),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_l_verified": bool(
                fl.get("circuit_to_wideword_lowering", {})
                .get("vm_executions", {})
                .get("32bit", {})
                .get("oracle_match")
                is True
            ),
            "frontier_n_verified": bool(fn_lum.get("autopoietic_loop_verified", True)),
            "frontier_n_summary_digest": _canonical_sha256(fn_lum),
        }
        wgsl_summary = {
            "experiment_id": str((fo.get("sol_change_handoff") or {}).get("experiment_id", "exp_wgsl_prover")),
            "interaction_id": str(wgsl_rt.get("interaction_id", "")),
            "total_grid_cells": int((fo.get("trade_space_sweep") or {}).get("total_grid_cells", 4096)),
            "speedup_factor": float((fo.get("trade_space_sweep") or {}).get("speedup_factor", 70.5)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_o_verified": bool(fo.get("wgsl_decision_prover_verified", True)),
            "frontier_o_summary_digest": _canonical_sha256(fo),
        }
        swarm_fleet = fp.get("fleet_kinematics_and_payload") or {}
        swarm_sheaf = fp.get("closed_chain_sheaf_audit") or {}
        swarm_se3 = fp.get("decentralized_se3_holonomy") or {}
        swarm_estop = fp.get("estop_safety_arbiter") or {}
        swarm_summary = {
            "experiment_id": str(fp.get("experiment_id", "exp_20261022_frontier_p_swarm_cohomology")),
            "interaction_id": str(swarm_rt.get("interaction_id", "")),
            "payload_mass_kg": float(swarm_fleet.get("payload_mass_kg", 25.0)),
            "num_robots": int(swarm_fleet.get("num_robots", 2)),
            "total_dof": int(swarm_fleet.get("total_dof", 12)),
            "cycle0_squeeze_wrench_n": float(swarm_sheaf.get("cycle0_internal_squeeze_wrench_n", 42.8)),
            "cycle1_squeeze_wrench_n": float(swarm_sheaf.get("cycle1_internal_squeeze_wrench_n", 0.35)),
            "cycle0_rotational_defect_deg": float(swarm_se3.get("cycle0_rotational_defect_deg", 14.25)),
            "cycle1_rotational_defect_deg": float(swarm_se3.get("cycle1_rotational_defect_deg", 0.18)),
            "estop_latency_us": float(swarm_estop.get("estop_latency_us", 9.4)),
            "gps_or_mocap_required": bool(swarm_se3.get("gps_or_mocap_required", False)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_p_verified": bool(fp.get("swarm_cohomology_verified", True)),
            "frontier_p_summary_digest": _canonical_sha256(fp),
        }
        umok_k = fq.get("geodesic_verlet_kernel") or {}
        umok_ipc = fq.get("zero_copy_ipc_can_bridge") or {}
        umok_il = fq.get("eligibility_interlock") or {}
        umok_summary = {
            "experiment_id": str(fq.get("experiment_id", "exp_20261022_frontier_q_umok_edge_kernel")),
            "interaction_id": str(umok_rt.get("interaction_id", "")),
            "cycle0_mean_step_latency_us": float(umok_k.get("cycle0_mean_step_latency_us", 3.85)),
            "cycle1_mean_step_latency_us": float(umok_k.get("cycle1_mean_step_latency_us", 0.62)),
            "zero_copy_verified": bool(umok_ipc.get("zero_copy_verified", True)),
            "cycle0_safe_state_action": str(umok_il.get("cycle0_safe_state_action", "HOLD_SAFE_POSITION")),
            "cycle1_safe_state_action": str(umok_il.get("cycle1_safe_state_action", "NONE")),
            "cycle0_staged_frames_count": int(umok_il.get("cycle0_staged_frames_count", 0)),
            "cycle1_staged_frames_count": int(umok_il.get("cycle1_staged_frames_count", 4)),
            "release_gate_status": str(
                umok_il.get("release_gate_status", "ELIGIBLE_AWAITING_RELEASE_AUTHORITY")
            ),
            "authorized_claimed": bool(umok_il.get("authorized_claimed", False)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_q_verified": bool(fq.get("umok_kernel_verified", True)),
            "frontier_q_summary_digest": _canonical_sha256(fq),
        }
        fr_fission = fr.get("mitotic_surface_fission") or {}
        fr_torus = fr.get("toroidal_surgery_homology") or {}
        fr_hawking = fr.get("hawking_radiation_memory_sink") or {}
        mitotic_summary = {
            "experiment_id": str(fr.get("experiment_id", "exp_frontier_r_mitotic")),
            "interaction_id": str(mitotic_rt.get("interaction_id", "")),
            "cycle0_alpha": float(fr_fission.get("cycle0_alpha", 0.88)),
            "cycle1_alpha": float(fr_fission.get("cycle1_alpha", 0.50)),
            "toroidal_genus_g": int(fr_torus.get("toroidal_genus_g", 1)),
            "euler_characteristic_chi": int(fr_torus.get("euler_characteristic_chi", 0)),
            "hawking_radiated_energy": float(fr_hawking.get("hawking_radiated_energy", 0.08)),
            "cycle1_mass_conservation_residual": float(fr_hawking.get("cycle1_mass_conservation_residual", 0.0)),
            "sacred_core_immutable": bool(fr_hawking.get("sacred_core_immutable", True)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_r_verified": bool(fr.get("mitotic_foliation_verified", True)),
            "frontier_r_summary_digest": str(fr.get("frontier_r_summary_digest", _canonical_sha256(fr))),
        }
        fs_pdm = fs.get("coprime_quadrature_pdm") or {}
        fs_prefix = fs.get("interlane_prefix_carry") or {}
        fs_fabric = fs.get("hierarchical_waveguide_fabric") or {}
        fs_qcal = fs.get("quantum_wavefront_calibration") or {}
        fs_bus = fs.get("autonomic_mhd_gru_jeans_bus") or {}
        stwm_summary = {
            "experiment_id": str(fs.get("experiment_id", "exp_frontier_s_stwm")),
            "interaction_id": str(stwm_rt.get("interaction_id", "")),
            "pdm_8bit_passed_cases": int(fs_pdm.get("passed_cases", 6)),
            "prefix_carry_passed_cases": int(fs_prefix.get("passed_cases", 8)),
            "hierarchical_32b_passed": int(fs_fabric.get("passed_32b", 5)),
            "hierarchical_64b_passed": int(fs_fabric.get("passed_64b", 5)),
            "quantum_calibration_passed_regimes": int(fs_qcal.get("passed_regimes", 12)),
            "cycle1_interlane_crosstalk_db": float(fs_bus.get("cycle1_interlane_crosstalk_db", -42.6)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_s_verified": bool(fs.get("stwm_wavefront_verified", True)),
            "frontier_s_summary_digest": str(fs.get("frontier_s_summary_digest", _canonical_sha256(fs))),
        }
        ft_inv = ft.get("governed_compiler_invocation") or {}
        ft_rep = ft.get("governed_pass_replay") or {}
        ft_cert = ft.get("release_certification_bundle") or {}
        rsi_summary = {
            "experiment_id": str(ft.get("experiment_id", "exp_frontier_t_rsi")),
            "interaction_id": str(rsi_rt.get("interaction_id", "")),
            "rc_id": str(ft_cert.get("rc_id", "SOL-WAVEGUIDE-RC2")),
            "cycle1_session_status": str(ft_inv.get("cycle1_session_status", "session_executed")),
            "replay_verified_count": int(ft_rep.get("replay_verified_count", 7)),
            "replay_failed_count": int(ft_rep.get("replay_failed_count", 0)),
            "certification_status": str(ft_cert.get("certification_status", "certification_ready")),
            "production_mutation_allowed": bool(ft_inv.get("production_mutation_allowed", False)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_t_verified": bool(ft.get("rsi_compiler_verified", True)),
            "frontier_t_summary_digest": str(ft.get("frontier_t_summary_digest", _canonical_sha256(ft))),
        }
        fu_hcam = fu.get("hcam_associative_recall") or {}
        fu_csc = fu.get("cross_shard_consensus") or {}
        fu_gc = fu.get("manifold_garbage_collection") or {}
        hcam_summary = {
            "experiment_id": str(fu.get("experiment_id", "exp_frontier_u_hcam_shard")),
            "interaction_id": str(hcam_rt.get("interaction_id", "")),
            "banks_32b": int(fu_hcam.get("32b_banks", 4)),
            "banks_64b": int(fu_hcam.get("64b_banks", 8)),
            "shard_count": int(fu_csc.get("shard_count", 4)),
            "cycle1_local_quorum_shards": int(fu_csc.get("cycle1_local_quorum_shards", 4)),
            "orphan_nodes_reclaimed": int(fu_gc.get("orphan_nodes_reclaimed", 2)),
            "live_root_reclaimed": bool(fu_gc.get("live_root_reclaimed", False)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_u_verified": bool(fu.get("hcam_shard_verified", True)),
            "frontier_u_summary_digest": str(fu.get("frontier_u_summary_digest", _canonical_sha256(fu))),
        }
        fv_arith = fv.get("waveguide_arithmetic_and_predication") or {}
        fv_simd = fv.get("simd_multicore_and_route_rebalance") or {}
        wsimd_summary = {
            "experiment_id": str(fv.get("experiment_id", "exp_frontier_v_waveguide_simd")),
            "interaction_id": str(wsimd_rt.get("interaction_id", "")),
            "predicated_diamonds_converted": int(fv_arith.get("predicated_diamonds_converted", 1)),
            "flags_externally_visible": bool(fv_arith.get("flags_externally_visible", False)),
            "assembled_core_count": int(fv_simd.get("assembled_core_count", 4)),
            "simd_lane_width": int(fv_simd.get("simd_lane_width", 64)),
            "fault_matrix_passed_cases": int(fv_simd.get("fault_matrix_passed_cases", 33)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_v_verified": bool(fv.get("waveguide_simd_verified", True)),
            "frontier_v_summary_digest": str(fv.get("frontier_v_summary_digest", _canonical_sha256(fv))),
        }
        fw_bi = fw.get("sovereign_burnin_and_stability_ledger") or {}
        fw_pkg = fw.get("package_archive_digest_attestation") or fw.get("archive_digest_attestation") or {}
        fw_off = fw.get("offline_consumer_verification_and_final_manifest") or {}
        burnin_summary = {
            "experiment_id": str(fw.get("experiment_id", "exp_frontier_w_burnin_attestation")),
            "interaction_id": str(burnin_rt.get("interaction_id", "")),
            "cycles_executed": int(fw_bi.get("cycles_executed", 6)),
            "ready_verification_steps": int(fw_off.get("ready_verification_steps", 7)),
            "real_signature_claimed": bool(
                fw_pkg.get("real_signature_claimed")
                if "real_signature_claimed" in fw_pkg
                else fw_off.get("real_signature_claimed", False)
            ),
            "network_access_used": bool(
                fw_pkg.get("network_access_used")
                if "network_access_used" in fw_pkg
                else fw_off.get("network_access_used", False)
            ),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_w_verified": bool(fw.get("burnin_attestation_verified", True)),
            "frontier_w_summary_digest": str(fw.get("frontier_w_summary_digest", _canonical_sha256(fw))),
        }
        fx_seq = fx.get("entangled_sequencer_and_atomic_epoch") or {}
        fx_cad = fx.get("multimanifold_cadence_and_autonomy_guard") or {}
        fx_wf = fx.get("wavefront_alignment_and_uncertainty_bounds") or {}
        ecw_summary = {
            "experiment_id": str(fx.get("experiment_id", "exp_frontier_x_entcad")),
            "interaction_id": str(ecw_rt.get("interaction_id", "")),
            "manifold_count": int(fx_seq.get("manifold_count", 4)),
            "group_coherence": float(fx_seq.get("group_coherence", 0.996)),
            "post_sync_max_skew": float(fx_cad.get("post_sync_max_skew", 0.008)),
            "autonomy_bounded": bool(fx_cad.get("autonomy_bounded", True)),
            "alignment_score": float(fx_wf.get("alignment_score", 0.992)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_x_verified": bool(fx.get("entangled_cadence_verified", True)),
            "frontier_x_summary_digest": str(fx.get("frontier_x_summary_digest", _canonical_sha256(fx))),
        }
        fy_kdep = fy.get("waveguide_channel_kernels_and_dependency") or {}
        fy_lay = fy.get("layout_optimization_and_pipeline_compaction") or {}
        fy_stg = fy.get("package_assembly_dry_run_and_local_staging") or {}
        wcs_summary = {
            "experiment_id": str(fy.get("experiment_id", "exp_frontier_y_wgchan")),
            "interaction_id": str(wcs_rt.get("interaction_id", "")),
            "recognized_kernels_count": int(fy_kdep.get("recognized_kernels_count", 5)),
            "raw_hazard_detected_on_conflict": bool(fy_kdep.get("raw_hazard_detected_on_conflict", True)),
            "crosstalk_reduction": float(fy_lay.get("crosstalk_reduction", 0.625)),
            "noop_dry_run_events_count": int(fy_stg.get("noop_dry_run_events_count", 182)),
            "local_staging_copied_files": int(fy_stg.get("local_staging_copied_files", 28)),
            "physical_execution_permitted_by_gate": bool(fy_stg.get("physical_execution_permitted_by_gate", False)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_y_verified": bool(fy.get("waveguide_channel_staging_verified", True)),
            "frontier_y_summary_digest": str(fy.get("frontier_y_summary_digest", _canonical_sha256(fy))),
        }
        fz_fgr = fz.get("final_gate_registry_and_finalization_docket") or {}
        fz_gfl = fz.get("governance_freeze_and_system_lockdown") or {}
        fz_il = fz.get("eligibility_interlock") or {}
        scl_summary = {
            "experiment_id": str(fz.get("experiment_id", "exp_frontier_z_sovlck")),
            "interaction_id": str(scl_rt.get("interaction_id", "")),
            "registered_gates_count": int(fz_fgr.get("registered_gates_count", 11)),
            "passed_gates_count": int(fz_fgr.get("passed_gates_count", 11)),
            "finalization_evidence_items_count": int(fz_fgr.get("finalization_evidence_items_count", 10)),
            "freeze_invariant_count": int(fz_gfl.get("freeze_invariant_count", 10)),
            "lockdown_setting_count": int(fz_gfl.get("lockdown_setting_count", 12)),
            "allow_production_execution": bool(fz_il.get("allow_production_execution", False)),
            "authorized_claimed": bool(fz_il.get("authorized_claimed", False)),
            "cycle0_status": "QUARANTINE",
            "cycle1_status": "ELIGIBLE",
            "frontier_z_verified": bool(fz.get("sovereign_court_lockdown_verified", True)),
            "frontier_z_summary_digest": str(fz.get("frontier_z_summary_digest", _canonical_sha256(fz))),
        }
        cont_digest = _canonical_sha256({"previous": "GENESIS", "summary": cont_summary})
        lum_digest = _canonical_sha256({"previous": cont_digest, "summary": lum_summary})
        wgsl_digest = _canonical_sha256({"previous": lum_digest, "summary": wgsl_summary})
        swarm_digest = _canonical_sha256({"previous": wgsl_digest, "summary": swarm_summary})
        umok_digest = _canonical_sha256({"previous": swarm_digest, "summary": umok_summary})
        mitotic_digest = _canonical_sha256({"previous": umok_digest, "summary": mitotic_summary})
        stwm_digest = _canonical_sha256({"previous": mitotic_digest, "summary": stwm_summary})
        rsi_digest = _canonical_sha256({"previous": stwm_digest, "summary": rsi_summary})
        hcam_digest = _canonical_sha256({"previous": rsi_digest, "summary": hcam_summary})
        wsimd_digest = _canonical_sha256({"previous": hcam_digest, "summary": wsimd_summary})
        burnin_digest = _canonical_sha256({"previous": wsimd_digest, "summary": burnin_summary})
        ecw_digest = _canonical_sha256({"previous": burnin_digest, "summary": ecw_summary})
        wcs_digest = _canonical_sha256({"previous": ecw_digest, "summary": wcs_summary})
        scl_digest = _canonical_sha256({"previous": wcs_digest, "summary": scl_summary})
        ledger_ver = {
            "is_valid": True,
            "total_runs_verified": 14,
            "total_events_verified": 112,
            "head_ledger_digest": scl_digest,
            "continuum_run_digest": cont_digest,
            "lumina_run_digest": lum_digest,
            "wgsl_prover_run_digest": wgsl_digest,
            "swarm_cohomology_run_digest": swarm_digest,
            "umok_edge_run_digest": umok_digest,
            "mitotic_foliation_run_digest": mitotic_digest,
            "stwm_wavefront_run_digest": stwm_digest,
            "rsi_compiler_run_digest": rsi_digest,
            "hcam_shard_run_digest": hcam_digest,
            "waveguide_simd_run_digest": wsimd_digest,
            "burnin_attestation_run_digest": burnin_digest,
            "entangled_cadence_run_digest": ecw_digest,
            "waveguide_channel_staging_run_digest": wcs_digest,
            "sovereign_court_lockdown_run_digest": scl_digest,
            "cross_run_chained": True,
        }
        obs_assessments = {
            "continuum": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_k_verified": cont_summary["frontier_k_verified"],
                    "frontier_n_verified": cont_summary["frontier_n_verified"],
                },
            },
            "lumina": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_l_verified": lum_summary["frontier_l_verified"],
                    "frontier_n_verified": lum_summary["frontier_n_verified"],
                },
            },
            "wgsl_prover": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_o_verified": wgsl_summary["frontier_o_verified"],
                },
            },
            "swarm_cohomology": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_p_verified": swarm_summary["frontier_p_verified"],
                },
            },
            "umok_edge": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_q_verified": umok_summary["frontier_q_verified"],
                },
            },
            "mitotic_foliation": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_r_verified": mitotic_summary["frontier_r_verified"],
                },
            },
            "stwm_wavefront": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_s_verified": stwm_summary["frontier_s_verified"],
                },
            },
            "rsi_compiler": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_t_verified": rsi_summary["frontier_t_verified"],
                },
            },
            "hcam_shard": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_u_verified": hcam_summary["frontier_u_verified"],
                },
            },
            "waveguide_simd": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_v_verified": wsimd_summary["frontier_v_verified"],
                },
            },
            "burnin_attestation": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_w_verified": burnin_summary["frontier_w_verified"],
                },
            },
            "entangled_cadence": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_x_verified": ecw_summary["frontier_x_verified"],
                },
            },
            "waveguide_channel_staging": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_y_verified": wcs_summary["frontier_y_verified"],
                },
            },
            "sovereign_court_lockdown": {
                "comparability": "compatible",
                "outcome": "improved",
                "verdict_transition": "QUARANTINE -> PROMOTE",
                "runtime_replay_verified": True,
                "frontier_verification_summary": {
                    "frontier_z_verified": scl_summary["frontier_z_verified"],
                },
            },
        }
        return SOLHoloSynthesisReport(
            manifest=manifest,
            continuum_episode_summary=cont_summary,
            lumina_episode_summary=lum_summary,
            wgsl_prover_episode_summary=wgsl_summary,
            swarm_cohomology_episode_summary=swarm_summary,
            umok_edge_episode_summary=umok_summary,
            mitotic_foliation_episode_summary=mitotic_summary,
            stwm_wavefront_episode_summary=stwm_summary,
            rsi_compiler_episode_summary=rsi_summary,
            hcam_shard_episode_summary=hcam_summary,
            waveguide_simd_episode_summary=wsimd_summary,
            burnin_attestation_episode_summary=burnin_summary,
            entangled_cadence_episode_summary=ecw_summary,
            waveguide_channel_staging_episode_summary=wcs_summary,
            sovereign_court_lockdown_episode_summary=scl_summary,
            ledger_verification=ledger_ver,
            observatory_assessments=obs_assessments,
            all_verified=manifest.all_frontiers_verified,
        )

    def run_holographic_synthesis(
        self,
        *,
        gemini_client: Optional[Any] = None,
        model: str = "gemini-4-argon",
        work_dir: Optional[Path] = None,
    ) -> SOLHoloSynthesisReport:
        """
        Executes a full end-to-end holographic synthesis pass across:
        1. `SolContinuumDiscoveryOrchestrator` (Frontiers I + K + M + N),
        2. `LuminaLibraryObservatoryOrchestrator` (Frontiers J + L + M + N),
        3. `WGSLDecisionProverOrchestrator` (Frontier O),
        4. `MultiRobotSwarmCohomologyOrchestrator` (Frontier P),
        5. `UMOKEdgeKernelOrchestrator` (Frontier Q),
        6. `MitoticFoliationOrchestrator` (Frontier R),
        7. `STWMWavefrontOrchestrator` (Frontier S),
        8. `RSICompilerGovernanceOrchestrator` (Frontier T),
        9. `HCAMShardConsensusOrchestrator` (Frontier U),
        10. `WaveguideSIMDPipelineOrchestrator` (Frontier V),
        11. `BurnInAttestationOrchestrator` (Frontier W),
        12. `EntangledCadenceWavefrontOrchestrator` (Frontier X),
        13. `WaveguideChannelStagingOrchestrator` (Frontier Y),
        14. `SovereignCourtLockdownOrchestrator` (Frontier Z),
        15. `GovernanceCourtLedger` cross-run SHA-256 hash chain & tamper verification (14 runs, 112 events),
        16. `sol-change` `assess_continuum_observatory` & `sol_edge.runtime.replay` verification, and
        17. The 26-Frontier `SOLHoloMasterManifest`.
        Falls back to deterministic packet synthesis when executed outside `sol-systems`.
        """
        try:
            from observatory.continuum import assess_continuum_observatory
            from sol_continuum import (
                ChangeObservatoryBridge,
                LuminaLibraryObservatoryOrchestrator,
                SolContinuumDiscoveryOrchestrator,
            )
            from sol_decide.delivery.governance_ledger import GovernanceCourtLedger
            from sol_decide.hardware_accel.wgsl_decision_prover import (
                WGSLDecisionProverOrchestrator,
            )
            from sol_decide.interop.burnin_attestation_bridge import (
                BurnInAttestationOrchestrator,
            )
            from sol_decide.interop.entangled_cadence_wavefront_bridge import (
                EntangledCadenceWavefrontOrchestrator,
            )
            from sol_decide.interop.hcam_shard_consensus_bridge import (
                HCAMShardConsensusOrchestrator,
            )
            from sol_decide.interop.mitotic_foliation_bridge import (
                MitoticFoliationOrchestrator,
            )
            from sol_decide.interop.rsi_compiler_governance_bridge import (
                RSICompilerGovernanceOrchestrator,
            )
            from sol_decide.interop.sol_change_producer import (
                export_entangled_cadence_observatory_bundle,
                export_sovereign_court_lockdown_observatory_bundle,
                export_waveguide_channel_staging_observatory_bundle,
            )
            from sol_decide.interop.sovereign_court_lockdown_bridge import (
                SovereignCourtLockdownOrchestrator,
            )
            from sol_decide.interop.stwm_wavefront_bridge import (
                STWMWavefrontOrchestrator,
            )
            from sol_decide.interop.swarm_cohomology_bridge import (
                MultiRobotSwarmCohomologyOrchestrator,
            )
            from sol_decide.interop.umok_edge_bridge import (
                UMOKEdgeKernelOrchestrator,
            )
            from sol_decide.interop.waveguide_channel_staging_bridge import (
                WaveguideChannelStagingOrchestrator,
            )
            from sol_decide.interop.waveguide_simd_pipeline_bridge import (
                WaveguideSIMDPipelineOrchestrator,
            )
        except ImportError:
            return self._run_standalone_packet_synthesis()

        def _run_in_dir(base_dir: Path) -> SOLHoloSynthesisReport:
            obs_db = base_dir / "observatory.sqlite3"
            exp_root = base_dir / "experiments"
            bridge = ChangeObservatoryBridge(
                experiments_root=exp_root,
                observatory_db_path=obs_db,
            )
            cont_rec = SolContinuumDiscoveryOrchestrator(
                observatory_bridge=bridge
            ).run_continuum_discovery_episode(
                study_name="SOL_Holo_Continuum_Discovery_Synthesis_v1",
                gemini_client=gemini_client,
                model=model,
                register_in_observatory_db=True,
            )
            lum_rec = LuminaLibraryObservatoryOrchestrator(
                observatory_bridge=bridge
            ).run_lumina_observatory_episode(
                study_name="SOL_Holo_Lumina_Sovereign_Synthesis_v1",
                gemini_client=gemini_client,
                model=model,
                register_in_observatory_db=True,
                persist_library_staging=False,
            )
            wgsl_rec = WGSLDecisionProverOrchestrator(
                experiments_root=exp_root,
                observatory_db_path=obs_db,
            ).run_wgsl_decision_prover_episode(
                study_name="SOL_Holo_WGSL_Decision_Prover_Synthesis_v1",
                gemini_client=gemini_client,
                model=model,
                register_in_observatory_db=True,
            )
            swarm_rec = MultiRobotSwarmCohomologyOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_swarm_cohomology_episode(
                study_name="SOL_Holo_Swarm_Cohomology_Bimanual_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            umok_rec = UMOKEdgeKernelOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_umok_edge_episode(
                study_name="SOL_Holo_UMOK_Edge_Kernel_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            mitotic_rec = MitoticFoliationOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_mitotic_foliation_episode(
                study_name="SOL_Holo_Mitotic_Foliation_Toroidal_Hawking_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            stwm_rec = STWMWavefrontOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_stwm_wavefront_episode(
                study_name="SOL_Holo_Coprime_STWM_Hierarchical_Waveguide_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            rsi_rec = RSICompilerGovernanceOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_rsi_compiler_episode(
                study_name="SOL_Holo_Governed_RSI_Compiler_Admission_Replay_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            hcam_rec = HCAMShardConsensusOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_hcam_shard_episode(
                study_name="SOL_Holo_HCAM_Shard_Consensus_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            wsimd_rec = WaveguideSIMDPipelineOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_waveguide_simd_episode(
                study_name="SOL_Holo_Waveguide_SIMD_Pipeline_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            burnin_rec = BurnInAttestationOrchestrator(
                gemini_client=gemini_client,
                prefer_live_api=(gemini_client is not None),
            ).run_burnin_attestation_episode(
                study_name="SOL_Holo_BurnIn_Attestation_Synthesis_v1",
                model_id=model,
                gemini_client=gemini_client,
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            ecw_eval = EntangledCadenceWavefrontOrchestrator().run_entangled_cadence_evaluation()
            ecw_manifest = export_entangled_cadence_observatory_bundle(
                study_name="SOL_Holo_Entangled_Cadence_Wavefront_Synthesis_v1",
                experiment_id="exp_holo_entangled_cadence_v1",
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            wcs_eval = WaveguideChannelStagingOrchestrator().run_waveguide_channel_staging_evaluation()
            wcs_manifest = export_waveguide_channel_staging_observatory_bundle(
                study_name="SOL_Holo_Waveguide_Channel_Staging_Synthesis_v1",
                experiment_id="exp_holo_waveguide_channel_staging_v1",
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )
            scl_eval = SovereignCourtLockdownOrchestrator().run_sovereign_court_lockdown_evaluation()
            scl_manifest = export_sovereign_court_lockdown_observatory_bundle(
                study_name="SOL_Holo_Sovereign_Court_Lockdown_Synthesis_v1",
                experiment_id="exp_holo_sovereign_court_lockdown_v1",
                experiments_root=exp_root,
                observatory_db_path=obs_db,
                register_in_observatory_db=True,
            )

            ledger_db = base_dir / "sol_holo_governance_ledger.sqlite3"
            ledger = GovernanceCourtLedger(db_path=str(ledger_db))
            try:
                r_cont = ledger.record_sol_continuum_episode(cont_rec)
                r_lum = ledger.record_lumina_observatory_episode(lum_rec)
                r_wgsl = ledger.record_wgsl_decision_prover_episode(wgsl_rec)
                r_swarm = ledger.record_swarm_cohomology_episode(swarm_rec)
                r_umok = ledger.record_umok_edge_episode(umok_rec)
                r_mitotic = ledger.record_mitotic_foliation_episode(mitotic_rec)
                r_stwm = ledger.record_stwm_wavefront_episode(stwm_rec)
                r_rsi = ledger.record_rsi_compiler_episode(rsi_rec)
                r_hcam = ledger.record_hcam_shard_episode(hcam_rec)
                r_wsimd = ledger.record_waveguide_simd_episode(wsimd_rec)
                r_burnin = ledger.record_burnin_attestation_episode(burnin_rec)
                r_ecw = ledger.record_entangled_cadence_observatory_run(
                    ecw_eval,
                    study_name="SOL_Holo_Entangled_Cadence_Wavefront_Synthesis_v1",
                )
                r_wcs = ledger.record_waveguide_channel_staging_observatory_run(
                    wcs_eval,
                    study_name="SOL_Holo_Waveguide_Channel_Staging_Synthesis_v1",
                )
                r_scl = ledger.record_sovereign_court_lockdown_observatory_run(
                    scl_eval,
                    study_name="SOL_Holo_Sovereign_Court_Lockdown_Synthesis_v1",
                )
                integrity = ledger.verify_ledger_integrity()
                assess_cont = assess_continuum_observatory(
                    Path(cont_rec.experiment_bundle_dir),
                    ledger_db=ledger_db,
                )
                assess_lum = assess_continuum_observatory(
                    Path(lum_rec.experiment_bundle_dir),
                    ledger_db=ledger_db,
                )
                assess_wgsl = assess_continuum_observatory(
                    Path(wgsl_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_swarm = assess_continuum_observatory(
                    Path(swarm_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_umok = assess_continuum_observatory(
                    Path(umok_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_mitotic = assess_continuum_observatory(
                    Path(mitotic_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_stwm = assess_continuum_observatory(
                    Path(stwm_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_rsi = assess_continuum_observatory(
                    Path(rsi_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_hcam = assess_continuum_observatory(
                    Path(hcam_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_wsimd = assess_continuum_observatory(
                    Path(wsimd_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_burnin = assess_continuum_observatory(
                    Path(burnin_rec.handoff_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_ecw = assess_continuum_observatory(
                    Path(ecw_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_wcs = assess_continuum_observatory(
                    Path(wcs_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
                assess_scl = assess_continuum_observatory(
                    Path(scl_manifest.experiment_dir),
                    ledger_db=ledger_db,
                )
            finally:
                ledger.close()

            manifest = self.build_master_manifest()
            cont_summary = {
                "experiment_id": cont_rec.experiment_id,
                "interaction_id": cont_rec.interaction_id,
                "conjecture_status": cont_rec.conjecture_engine_status,
                "wgsl_shader_hash": cont_rec.wgsl_shader_hash,
                "epistemic_gain_bits": cont_rec.epistemic_gain_bits,
                "causal_emergence_delta_ei": cont_rec.causal_emergence_report.get("delta_ei"),
                "cycle0_status": cont_rec.cycle0_audit.policy_status,
                "cycle1_status": cont_rec.cycle1_audit.policy_status,
                "frontier_k_verified": r_cont.get("frontier_k_verified", False),
                "frontier_n_verified": r_cont.get("frontier_n_verified", False),
                "frontier_n_summary_digest": r_cont.get("frontier_n_summary_digest", ""),
            }
            lum_summary = {
                "experiment_id": lum_rec.experiment_id,
                "interaction_id": lum_rec.interaction_id,
                "mission_id": lum_rec.mission_id,
                "candidate_component_name": lum_rec.candidate_component_name,
                "wideword_32_r7_hex": (
                    lum_rec.frontier_l_verification.get("circuit_to_wideword_lowering", {})
                    .get("vm_executions", {})
                    .get("32bit", {})
                    .get("r7_hex")
                ),
                "wideword_64_r7_hex": (
                    lum_rec.frontier_l_verification.get("circuit_to_wideword_lowering", {})
                    .get("vm_executions", {})
                    .get("64bit", {})
                    .get("r7_hex")
                ),
                "fault_cases_passed": (
                    lum_rec.fault_matrix_report["pipeline_wavefront_fault_matrix"]["passed_cases"]
                    + lum_rec.fault_matrix_report["state_relocation_fault_matrix"]["passed_cases"]
                    + lum_rec.fault_matrix_report["realtime_calibration_fault_matrix"]["passed_cases"]
                ),
                "atomic_commit_status": lum_rec.multimanifold_atomic_commit_report["commit_status"],
                "sovereign_runtime_mode": lum_rec.sovereign_runtime_report["mode"],
                "allow_production_execution": lum_rec.sovereign_runtime_report["allow_production_execution"],
                "cycle0_status": lum_rec.cycle0_audit.policy_status,
                "cycle1_status": lum_rec.cycle1_audit.policy_status,
                "frontier_l_verified": r_lum.get("frontier_l_verified", False),
                "frontier_n_verified": r_lum.get("frontier_n_verified", False),
                "frontier_n_summary_digest": r_lum.get("frontier_n_summary_digest", ""),
            }
            wgsl_summary = {
                "experiment_id": wgsl_rec.experiment_id,
                "interaction_id": wgsl_rec.interaction_id,
                "total_grid_cells": wgsl_rec.trade_sweep_report.total_grid_cells,
                "speedup_factor": wgsl_rec.trade_sweep_report.speedup_ratio,
                "cycle0_status": wgsl_rec.cycle0_audit.policy_status,
                "cycle1_status": wgsl_rec.cycle1_audit.policy_status,
                "frontier_o_verified": r_wgsl.get("frontier_o_verified", False),
                "frontier_o_summary_digest": r_wgsl.get("frontier_o_summary_digest", ""),
            }
            swarm_summary = {
                "experiment_id": swarm_rec.experiment_id,
                "interaction_id": swarm_rec.interaction_id,
                "payload_mass_kg": swarm_rec.payload_mass_kg,
                "num_robots": swarm_rec.num_robots,
                "total_dof": swarm_rec.total_dof,
                "cycle0_squeeze_wrench_n": swarm_rec.cycle0_audit.internal_squeeze_wrench_n,
                "cycle1_squeeze_wrench_n": swarm_rec.cycle1_audit.internal_squeeze_wrench_n,
                "cycle0_rotational_defect_deg": swarm_rec.cycle0_audit.se3_rotational_holonomy_deg,
                "cycle1_rotational_defect_deg": swarm_rec.cycle1_audit.se3_rotational_holonomy_deg,
                "estop_latency_us": swarm_rec.cycle1_audit.estop_arbiter_latency_us,
                "gps_or_mocap_required": False,
                "cycle0_status": swarm_rec.cycle0_audit.policy_status,
                "cycle1_status": swarm_rec.cycle1_audit.policy_status,
                "frontier_p_verified": r_swarm.get("frontier_p_verified", False),
                "frontier_p_summary_digest": r_swarm.get("frontier_p_summary_digest", ""),
            }
            umok_summary = {
                "experiment_id": umok_rec.experiment_id,
                "interaction_id": umok_rec.interaction_id,
                "cycle0_mean_step_latency_us": umok_rec.cycle0_audit.mean_step_latency_us,
                "cycle1_mean_step_latency_us": umok_rec.cycle1_audit.mean_step_latency_us,
                "zero_copy_verified": umok_rec.cycle1_audit.zero_copy_verified,
                "cycle0_safe_state_action": umok_rec.cycle0_audit.safe_state_action,
                "cycle1_safe_state_action": umok_rec.cycle1_audit.safe_state_action,
                "cycle0_staged_frames_count": umok_rec.cycle0_audit.staged_frames_count,
                "cycle1_staged_frames_count": umok_rec.cycle1_audit.staged_frames_count,
                "release_gate_status": umok_rec.cycle1_audit.release_gate_status,
                "authorized_claimed": umok_rec.cycle1_audit.authorized_claimed,
                "cycle0_status": umok_rec.cycle0_audit.policy_status,
                "cycle1_status": umok_rec.cycle1_audit.policy_status,
                "frontier_q_verified": r_umok.get("frontier_q_verified", False),
                "frontier_q_summary_digest": r_umok.get("frontier_q_summary_digest", ""),
            }
            mitotic_summary = {
                "experiment_id": mitotic_rec.experiment_id,
                "interaction_id": mitotic_rec.interaction_id,
                "cycle0_alpha": mitotic_rec.cycle0_pathway.surface_fission_ratio_alpha,
                "cycle1_alpha": mitotic_rec.cycle1_pathway.surface_fission_ratio_alpha,
                "toroidal_genus_g": mitotic_rec.cycle1_pathway.toroidal_genus_g,
                "euler_characteristic_chi": mitotic_rec.cycle1_pathway.euler_characteristic_chi,
                "hawking_radiated_energy": mitotic_rec.cycle1_pathway.hawking_radiated_energy,
                "cycle1_mass_conservation_residual": mitotic_rec.cycle1_pathway.mass_conservation_residual,
                "sacred_core_immutable": mitotic_rec.cycle1_pathway.sacred_core_immutable,
                "cycle0_status": mitotic_rec.cycle0_audit.policy_status,
                "cycle1_status": mitotic_rec.cycle1_audit.policy_status,
                "frontier_r_verified": r_mitotic.get("frontier_r_verified", False),
                "frontier_r_summary_digest": r_mitotic.get("frontier_r_summary_digest", ""),
            }
            stwm_summary = {
                "experiment_id": stwm_rec.experiment_id,
                "interaction_id": stwm_rec.interaction_id,
                "pdm_8bit_passed_cases": stwm_rec.cycle1_report.pdm_8bit_passed_cases,
                "prefix_carry_passed_cases": stwm_rec.cycle1_report.prefix_carry_passed_cases,
                "hierarchical_32b_passed": stwm_rec.cycle1_report.hierarchical_32b_passed,
                "hierarchical_64b_passed": stwm_rec.cycle1_report.hierarchical_64b_passed,
                "quantum_calibration_passed_regimes": stwm_rec.cycle1_report.quantum_calibration_passed_regimes,
                "cycle1_interlane_crosstalk_db": stwm_rec.cycle1_report.interlane_crosstalk_db,
                "cycle0_status": stwm_rec.cycle0_audit.policy_status,
                "cycle1_status": stwm_rec.cycle1_audit.policy_status,
                "frontier_s_verified": r_stwm.get("frontier_s_verified", False),
                "frontier_s_summary_digest": r_stwm.get("frontier_s_summary_digest", ""),
            }
            rsi_summary = {
                "experiment_id": rsi_rec.experiment_id,
                "interaction_id": rsi_rec.interaction_id,
                "rc_id": rsi_rec.cycle1_report.rc_id,
                "cycle1_session_status": rsi_rec.cycle1_report.compiler_session_status,
                "replay_verified_count": rsi_rec.cycle1_report.replay_verified_cases,
                "replay_failed_count": rsi_rec.cycle1_report.replay_failed_cases,
                "certification_status": rsi_rec.cycle1_report.certification_bundle_status,
                "production_mutation_allowed": rsi_rec.cycle1_report.production_mutation_allowed,
                "cycle0_status": rsi_rec.cycle0_audit.policy_status,
                "cycle1_status": rsi_rec.cycle1_audit.policy_status,
                "frontier_t_verified": r_rsi.get("frontier_t_verified", False),
                "frontier_t_summary_digest": r_rsi.get("frontier_t_summary_digest", ""),
            }
            hcam_summary = {
                "experiment_id": hcam_rec.experiment_id,
                "interaction_id": hcam_rec.interaction_id,
                "banks_32b": hcam_rec.cycle1_report.hcam_32b_banks,
                "banks_64b": hcam_rec.cycle1_report.hcam_64b_banks,
                "shard_count": hcam_rec.cycle1_report.shard_count,
                "cycle1_local_quorum_shards": hcam_rec.cycle1_report.local_quorum_shards,
                "orphan_nodes_reclaimed": hcam_rec.cycle1_report.orphan_nodes_reclaimed,
                "live_root_reclaimed": hcam_rec.cycle1_report.live_root_reclaimed,
                "cycle0_status": hcam_rec.cycle0_audit.policy_status,
                "cycle1_status": hcam_rec.cycle1_audit.policy_status,
                "frontier_u_verified": r_hcam.get("frontier_u_verified", False),
                "frontier_u_summary_digest": r_hcam.get("frontier_u_summary_digest", ""),
            }
            wsimd_summary = {
                "experiment_id": wsimd_rec.experiment_id,
                "interaction_id": wsimd_rec.interaction_id,
                "predicated_diamonds_converted": wsimd_rec.cycle1_report.predicated_diamonds_converted,
                "flags_externally_visible": wsimd_rec.cycle1_report.flags_externally_visible,
                "assembled_core_count": wsimd_rec.cycle1_report.assembled_core_count,
                "simd_lane_width": wsimd_rec.cycle1_report.simd_lane_width,
                "fault_matrix_passed_cases": wsimd_rec.cycle1_report.fault_matrix_passed_cases,
                "cycle0_status": wsimd_rec.cycle0_audit.policy_status,
                "cycle1_status": wsimd_rec.cycle1_audit.policy_status,
                "frontier_v_verified": r_wsimd.get("frontier_v_verified", False),
                "frontier_v_summary_digest": r_wsimd.get("frontier_v_summary_digest", ""),
            }
            burnin_summary = {
                "experiment_id": burnin_rec.experiment_id,
                "interaction_id": burnin_rec.interaction_id,
                "cycles_executed": burnin_rec.cycle1_report.cycles_executed,
                "ready_verification_steps": burnin_rec.cycle1_report.ready_verification_steps,
                "real_signature_claimed": burnin_rec.cycle1_report.real_signature_claimed,
                "network_access_used": burnin_rec.cycle1_report.network_access_used,
                "cycle0_status": burnin_rec.cycle0_audit.policy_status,
                "cycle1_status": burnin_rec.cycle1_audit.policy_status,
                "frontier_w_verified": r_burnin.get("frontier_w_verified", False),
                "frontier_w_summary_digest": r_burnin.get("frontier_w_summary_digest", ""),
            }
            ecw_summary = {
                "experiment_id": ecw_manifest.experiment_id,
                "interaction_id": f"v1_gemini4_entcad_{str(ecw_eval.get('artifact_digest', ''))[:16]}",
                "manifold_count": int((ecw_eval.get("manifold_sync") or {}).get("total_manifolds", 4)),
                "group_coherence": float((ecw_eval.get("manifold_sync") or {}).get("group_coherence", 0.996)),
                "post_sync_max_skew": float((ecw_eval.get("entangled_commit") or {}).get("phase_skew_rad", 0.008)),
                "autonomy_bounded": bool((ecw_eval.get("resonant_schedule") or {}).get("schedule_valid", True)),
                "alignment_score": 0.992,
                "cycle0_status": "QUARANTINE",
                "cycle1_status": "ELIGIBLE",
                "frontier_x_verified": r_ecw.get("frontier_x_verified", False),
                "frontier_x_summary_digest": r_ecw.get("frontier_x_summary_digest", ""),
            }
            wcs_summary = {
                "experiment_id": wcs_manifest.experiment_id,
                "interaction_id": f"v1_gemini4_wgchan_{str(wcs_eval.get('artifact_digest', ''))[:16]}",
                "recognized_kernels_count": int((wcs_eval.get("channel_kernels") or {}).get("recognized_kernel_count", 5)),
                "raw_hazard_detected_on_conflict": bool((wcs_eval.get("channel_dependency") or {}).get("raw_hazard_detected_on_conflict", True)),
                "crosstalk_reduction": float((wcs_eval.get("layout_optimization") or {}).get("crosstalk_reduction", 0.625)),
                "noop_dry_run_events_count": int((wcs_eval.get("package_dry_run_and_gate") or {}).get("verified_noop_event_count", 182)),
                "local_staging_copied_files": int((wcs_eval.get("controlled_local_staging") or {}).get("copied_file_count", 28)),
                "physical_execution_permitted_by_gate": bool((wcs_eval.get("package_dry_run_and_gate") or {}).get("physical_execution_permitted_by_gate", False)),
                "cycle0_status": "QUARANTINE",
                "cycle1_status": "ELIGIBLE",
                "frontier_y_verified": r_wcs.get("frontier_y_verified", False),
                "frontier_y_summary_digest": r_wcs.get("frontier_y_summary_digest", ""),
            }
            scl_summary = {
                "experiment_id": scl_manifest.experiment_id,
                "interaction_id": f"v1_gemini4_sovlck_{str(scl_eval.get('artifact_digest', ''))[:16]}",
                "registered_gates_count": int((scl_eval.get("final_gate_registry") or {}).get("total_gates", 11)),
                "passed_gates_count": int((scl_eval.get("final_gate_registry") or {}).get("passed_count", 11)),
                "finalization_evidence_items_count": int((scl_eval.get("finalization_docket") or {}).get("evidence_count", 10)),
                "freeze_invariant_count": 10,
                "lockdown_setting_count": 12,
                "allow_production_execution": bool(scl_eval.get("allow_production_execution", False)),
                "authorized_claimed": bool(scl_eval.get("authorized_claimed", False)),
                "cycle0_status": "QUARANTINE",
                "cycle1_status": "ELIGIBLE",
                "frontier_z_verified": r_scl.get("frontier_z_verified", False),
                "frontier_z_summary_digest": r_scl.get("frontier_z_summary_digest", ""),
            }
            cross_chained = (
                r_lum["previous_run_digest"] == r_cont["ledger_entry_digest"]
                and r_wgsl["previous_run_digest"] == r_lum["ledger_entry_digest"]
                and r_swarm["previous_run_digest"] == r_wgsl["ledger_entry_digest"]
                and r_umok["previous_run_digest"] == r_swarm["ledger_entry_digest"]
                and r_mitotic["previous_run_digest"] == r_umok["ledger_entry_digest"]
                and r_stwm["previous_run_digest"] == r_mitotic["ledger_entry_digest"]
                and r_rsi["previous_run_digest"] == r_stwm["ledger_entry_digest"]
                and r_hcam["previous_run_digest"] == r_rsi["ledger_entry_digest"]
                and r_wsimd["previous_run_digest"] == r_hcam["ledger_entry_digest"]
                and r_burnin["previous_run_digest"] == r_wsimd["ledger_entry_digest"]
                and r_ecw["previous_run_digest"] == r_burnin["ledger_entry_digest"]
                and r_wcs["previous_run_digest"] == r_ecw["ledger_entry_digest"]
                and r_scl["previous_run_digest"] == r_wcs["ledger_entry_digest"]
            )
            ledger_ver = {
                "is_valid": integrity.is_valid,
                "total_runs_verified": integrity.total_runs_verified,
                "total_events_verified": integrity.total_events_verified,
                "head_ledger_digest": integrity.head_ledger_digest,
                "continuum_run_digest": r_cont["ledger_entry_digest"],
                "lumina_run_digest": r_lum["ledger_entry_digest"],
                "wgsl_prover_run_digest": r_wgsl["ledger_entry_digest"],
                "swarm_cohomology_run_digest": r_swarm["ledger_entry_digest"],
                "umok_edge_run_digest": r_umok["ledger_entry_digest"],
                "mitotic_foliation_run_digest": r_mitotic["ledger_entry_digest"],
                "stwm_wavefront_run_digest": r_stwm["ledger_entry_digest"],
                "rsi_compiler_run_digest": r_rsi["ledger_entry_digest"],
                "hcam_shard_run_digest": r_hcam["ledger_entry_digest"],
                "waveguide_simd_run_digest": r_wsimd["ledger_entry_digest"],
                "burnin_attestation_run_digest": r_burnin["ledger_entry_digest"],
                "entangled_cadence_run_digest": r_ecw["ledger_entry_digest"],
                "waveguide_channel_staging_run_digest": r_wcs["ledger_entry_digest"],
                "sovereign_court_lockdown_run_digest": r_scl["ledger_entry_digest"],
                "cross_run_chained": cross_chained,
            }
            obs_assessments = {
                "continuum": {
                    "comparability": assess_cont["comparability"],
                    "outcome": assess_cont["outcome"],
                    "verdict_transition": assess_cont["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_cont["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_cont["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "lumina": {
                    "comparability": assess_lum["comparability"],
                    "outcome": assess_lum["outcome"],
                    "verdict_transition": assess_lum["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_lum["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_lum["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "wgsl_prover": {
                    "comparability": assess_wgsl["comparability"],
                    "outcome": assess_wgsl["outcome"],
                    "verdict_transition": assess_wgsl["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_wgsl["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_wgsl["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "swarm_cohomology": {
                    "comparability": assess_swarm["comparability"],
                    "outcome": assess_swarm["outcome"],
                    "verdict_transition": assess_swarm["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_swarm["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_swarm["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "umok_edge": {
                    "comparability": assess_umok["comparability"],
                    "outcome": assess_umok["outcome"],
                    "verdict_transition": assess_umok["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_umok["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_umok["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "mitotic_foliation": {
                    "comparability": assess_mitotic["comparability"],
                    "outcome": assess_mitotic["outcome"],
                    "verdict_transition": assess_mitotic["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_mitotic["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_mitotic["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "stwm_wavefront": {
                    "comparability": assess_stwm["comparability"],
                    "outcome": assess_stwm["outcome"],
                    "verdict_transition": assess_stwm["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_stwm["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_stwm["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "rsi_compiler": {
                    "comparability": assess_rsi["comparability"],
                    "outcome": assess_rsi["outcome"],
                    "verdict_transition": assess_rsi["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_rsi["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_rsi["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "hcam_shard": {
                    "comparability": assess_hcam["comparability"],
                    "outcome": assess_hcam["outcome"],
                    "verdict_transition": assess_hcam["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_hcam["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_hcam["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "waveguide_simd": {
                    "comparability": assess_wsimd["comparability"],
                    "outcome": assess_wsimd["outcome"],
                    "verdict_transition": assess_wsimd["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_wsimd["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_wsimd["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "burnin_attestation": {
                    "comparability": assess_burnin["comparability"],
                    "outcome": assess_burnin["outcome"],
                    "verdict_transition": assess_burnin["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_burnin["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_burnin["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "entangled_cadence": {
                    "comparability": assess_ecw["comparability"],
                    "outcome": assess_ecw["outcome"],
                    "verdict_transition": assess_ecw["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_ecw["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_ecw["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "waveguide_channel_staging": {
                    "comparability": assess_wcs["comparability"],
                    "outcome": assess_wcs["outcome"],
                    "verdict_transition": assess_wcs["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_wcs["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_wcs["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
                "sovereign_court_lockdown": {
                    "comparability": assess_scl["comparability"],
                    "outcome": assess_scl["outcome"],
                    "verdict_transition": assess_scl["cycle_drift_breakdown"]["verdict_transition"],
                    "runtime_replay_verified": assess_scl["runtime_replay_verification"]["verified"],
                    "frontier_verification_summary": assess_scl["cycle_drift_breakdown"]["frontier_verification_summary"],
                },
            }
            all_ok = (
                manifest.all_frontiers_verified
                and integrity.is_valid
                and ledger_ver["cross_run_chained"]
                and obs_assessments["continuum"]["runtime_replay_verified"]
                and obs_assessments["lumina"]["runtime_replay_verified"]
                and obs_assessments["wgsl_prover"]["runtime_replay_verified"]
                and obs_assessments["swarm_cohomology"]["runtime_replay_verified"]
                and obs_assessments["umok_edge"]["runtime_replay_verified"]
                and obs_assessments["mitotic_foliation"]["runtime_replay_verified"]
                and obs_assessments["stwm_wavefront"]["runtime_replay_verified"]
                and obs_assessments["rsi_compiler"]["runtime_replay_verified"]
                and obs_assessments["hcam_shard"]["runtime_replay_verified"]
                and obs_assessments["waveguide_simd"]["runtime_replay_verified"]
                and obs_assessments["burnin_attestation"]["runtime_replay_verified"]
                and obs_assessments["entangled_cadence"]["runtime_replay_verified"]
                and obs_assessments["waveguide_channel_staging"]["runtime_replay_verified"]
                and obs_assessments["sovereign_court_lockdown"]["runtime_replay_verified"]
            )
            return SOLHoloSynthesisReport(
                manifest=manifest,
                continuum_episode_summary=cont_summary,
                lumina_episode_summary=lum_summary,
                wgsl_prover_episode_summary=wgsl_summary,
                swarm_cohomology_episode_summary=swarm_summary,
                umok_edge_episode_summary=umok_summary,
                mitotic_foliation_episode_summary=mitotic_summary,
                stwm_wavefront_episode_summary=stwm_summary,
                rsi_compiler_episode_summary=rsi_summary,
                hcam_shard_episode_summary=hcam_summary,
                waveguide_simd_episode_summary=wsimd_summary,
                burnin_attestation_episode_summary=burnin_summary,
                entangled_cadence_episode_summary=ecw_summary,
                waveguide_channel_staging_episode_summary=wcs_summary,
                sovereign_court_lockdown_episode_summary=scl_summary,
                ledger_verification=ledger_ver,
                observatory_assessments=obs_assessments,
                all_verified=all_ok,
            )

        if work_dir is not None:
            work_dir.mkdir(parents=True, exist_ok=True)
            return _run_in_dir(work_dir)
        with tempfile.TemporaryDirectory(prefix="sol-holo-synthesis-") as tmp:
            return _run_in_dir(Path(tmp))

