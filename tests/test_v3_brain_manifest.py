"""
Comprehensive Unit & Integration Tests for V3 Brain Manifest & Reflective Agentic Domain
(`gemini-4-argon` Integration across `sol-llm`, `sol-continuum`, `sol-cortex`,
`sol-hippocampus`, `sol-evolve/self_train`, `sol-decide`, `sol-change`, and `sol-holo`).
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
for _rel in (
    "sol-holo",
    "sol-continuum",
    "sol-decide",
    "sol-edge/src",
    "sol-change",
    "sol/tools/sol-llm",
    "sol/tools/sol-evolve",
    "sol/tools/sol-cortex",
    "sol/tools/sol-hippocampus",
    "sol",
):
    _p = str(_REPO_ROOT / _rel)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from sol_continuum.reflective_domain import (
    REFLECTIVE_GUILD_AGENT_ROLES,
    SACRED_DEFAULT_GRAPH_SHA256,
    HolographicContextEncoder,
    HolographicSubstrateSnapshot,
    verify_sacred_core_graph_sha256,
)
from sol_decide.delivery.governance_ledger import GovernanceCourtLedger
from sol_holo.cli import main as sol_holo_cli_main
from sol_holo.v3_brain_manifest import (
    V3BrainManifest,
    V3BrainReflectiveOrchestrator,
    _load_tool_module,
)


class _DummyOutputItem:
    def __init__(self, item_type: str, text: str = "", summary: str = "", signature: str = "") -> None:
        self.type = item_type
        self.text = text
        self.summary = summary
        self.signature = signature


class _DummyUsage:
    def __init__(self) -> None:
        self.input_tokens = 14800
        self.output_tokens = 512
        self.thought_tokens = 640
        self.cached_tokens = 14080


class _DummyInteraction:
    def __init__(
        self,
        interaction_id: str,
        outputs: list[_DummyOutputItem],
        status: str = "completed",
    ) -> None:
        self.id = interaction_id
        self.outputs = outputs
        self.status = status
        self.usage = _DummyUsage()


class _DummyInteractionsAPI:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.get_calls: list[str] = []

    def create(self, **kwargs: Any) -> _DummyInteraction:
        self.calls.append(kwargs)
        idx = len(self.calls)
        if kwargs.get("background"):
            return _DummyInteraction(
                interaction_id=f"int-mock-bg-{idx}",
                outputs=[],
                status="in_progress",
            )
        return _DummyInteraction(
            interaction_id=f"int-mock-{idx}",
            outputs=[
                _DummyOutputItem(
                    "thought",
                    summary=f"Step {idx} reasoning summary over 140-node manifold.",
                    signature=f"sig-raw-{idx}-argon",
                ),
                _DummyOutputItem("text", text='{"part": 1, '),
                _DummyOutputItem("text", text=f'"step": {idx}}}'),
            ],
            status="completed",
        )

    def get(self, id: str = "", interaction_id: str = "") -> _DummyInteraction:
        resolved_id = id or interaction_id
        self.get_calls.append(resolved_id)
        return _DummyInteraction(
            interaction_id=resolved_id,
            outputs=[
                _DummyOutputItem(
                    "thought",
                    summary="Background deep research completed.",
                    signature="sig-bg-completed",
                ),
                _DummyOutputItem("text", text='{"background_completed": true}'),
            ],
            status="completed",
        )


class _DummyGenAIClient:
    def __init__(self) -> None:
        self.interactions = _DummyInteractionsAPI()


def test_sol_llm_gemini4_argon_config_and_interactions_client(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify sol-llm models.json, config.py, and client.py gemini-4-argon Interactions API support."""
    llm_config_mod = _load_tool_module("sol_llm_config_test", "sol/tools/sol-llm/config.py")
    llm_client_mod = _load_tool_module("sol_llm_client_test", "sol/tools/sol-llm/client.py")

    cfg = llm_config_mod.load_config()
    assert cfg["providers"]["google"]["sdk"] == "google-genai"
    assert cfg["providers"]["google"]["env_var"] == "GEMINI_API_KEY"
    assert cfg["providers"]["google"]["fallback_env_var"] == "GOOGLE_API_KEY"
    assert cfg["models"]["primary"]["id"] == "gemini-4-argon"
    assert cfg["models"]["primary"]["thinking_level"] == "high"
    assert cfg["models"]["primary"]["max_output_tokens"] >= 32768
    assert cfg["models"]["reasoning"]["id"] == "gemini-4-argon"
    assert cfg["models"]["fallback"]["id"] == "gemini-3.8-flash"

    dummy_client = _DummyGenAIClient()
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-argon")

    sol_llm = llm_client_mod.SolLLM()
    monkeypatch.setattr(sol_llm, "_get_genai_client", lambda _api_key: dummy_client)

    # Test standard synchronous interaction with multi-hop text concatenation & previous_interaction_id
    resp = sol_llm.complete(
        "Synthesize multi-knob update",
        slot="primary",
        system="System instruction",
        previous_interaction_id="int-prev-000",
    )
    assert resp.model == "gemini-4-argon"
    assert resp.interaction_id == "int-mock-1"
    assert resp.previous_interaction_id == "int-prev-000"
    assert resp.thinking_level == "high"
    assert resp.text == '{"part": 1, "step": 1}'
    assert resp.thought_step_count == 1
    assert len(resp.thought_signature_digests) == 1
    assert resp.cached_input_tokens == 14080

    call_kwargs = dummy_client.interactions.calls[0]
    gen_cfg = call_kwargs["generation_config"]
    assert gen_cfg["thinking_level"] == "high"
    assert gen_cfg["max_output_tokens"] >= 32768
    assert "temperature" not in gen_cfg
    assert "top_p" not in gen_cfg
    assert "top_k" not in gen_cfg
    assert call_kwargs["previous_interaction_id"] == "int-prev-000"

    # Test background=True polling path
    bg_resp = sol_llm.complete(
        "Run deep background epistemic campaign",
        slot="reasoning",
        background=True,
        poll_interval_s=0.01,
        max_wait_s=2.0,
    )
    assert bg_resp.interaction_id == "int-mock-bg-2"
    assert bg_resp.text == '{"background_completed": true}'
    assert dummy_client.interactions.get_calls == ["int-mock-bg-2"]


def test_holographic_context_encoder_prefix_invariance() -> None:
    """Verify 7-pillar HolographicSubstrateSnapshot and >= 4,096-token byte-identical prefix across all 4 guild agents."""
    snapshot = HolographicSubstrateSnapshot.capture(_REPO_ROOT)
    assert snapshot.sacred_core_graph_immutable is True
    assert snapshot.sacred_core_graph_sha256 == SACRED_DEFAULT_GRAPH_SHA256
    assert snapshot.sol_holo["total_frontiers"] == 26
    assert snapshot.sol_holo["verified_frontiers"] == 26

    encoder = HolographicContextEncoder(snapshot=snapshot)
    assert encoder.prefix_token_count >= 4096
    prefix = encoder.canonical_prefix

    digests = set()
    for idx, role in enumerate(REFLECTIVE_GUILD_AGENT_ROLES):
        built = encoder.build_agent_prompt(
            agent_role=role,
            agent_directive=f"Task for {role}",
            dynamic_payload={"step": idx + 1},
        )
        assert built["prompt"].startswith(prefix)
        assert built["byte_identical_prefix"] is True
        digests.add(built["prefix_digest"])

    assert len(digests) == 1


def test_reflective_gemini_teacher_and_cortex_hippocampus_pillars() -> None:
    """Verify ReflectiveGeminiTeacher (sol-evolve), run_holistic_manifold_reflection (sol-cortex), and consolidate_holo_reflective_traces (sol-hippocampus)."""
    snapshot = HolographicSubstrateSnapshot.capture(_REPO_ROOT)
    encoder = HolographicContextEncoder(snapshot=snapshot)
    snap_dict = snapshot.to_dict()

    # 1. sol-cortex holistic manifold reflection
    cortex_mod = _load_tool_module("sol_cortex_run_loop_test", "sol/tools/sol-cortex/run_loop.py")
    campaign = cortex_mod.run_holistic_manifold_reflection(
        holo_snapshot=snap_dict,
        canonical_prefix=encoder.canonical_prefix,
        live=False,
    )
    assert campaign["protocol"] == "Multi_Protocol_Epistemic_Campaign"
    assert campaign["sacred_core_graph_immutable"] is True
    assert set(campaign["coupled_knobs"]) >= {"c_press", "damping", "psi_diffusion", "cap_threshold"}

    # 2. sol-hippocampus dream consolidation & Rule 7 Law promotion
    hippo_mod = _load_tool_module("sol_hippocampus_dream_test", "sol/tools/sol-hippocampus/dream_cycle.py")
    consolidation = hippo_mod.consolidate_holo_reflective_traces(
        holo_snapshot=snap_dict,
        cortex_campaign=campaign,
        canonical_prefix=encoder.canonical_prefix,
        live=False,
        persist_overlay=False,
    )
    assert consolidation["mahalanobis_isometry_verified"] is True
    assert consolidation["mahalanobis_isometry_r"] >= 0.9968
    assert consolidation["sacred_core_graph_immutable"] is True
    assert consolidation["promoted_law"]["law_id"] == "LAW-V3-BRAIN-001"

    # 3. sol-evolve ReflectiveGeminiTeacher & loop integration
    teacher_mod = _load_tool_module("sol_evolve_teacher_test", "sol/tools/sol-evolve/self_train/teacher.py")
    models_mod = _load_tool_module("sol_evolve_models_test", "sol/tools/sol-evolve/self_train/models.py")
    baseline_pol = models_mod.Policy(
        policy_id="policy-g000",
        generation=0,
        knobs={
            "c_press": 0.35,
            "damping": 0.80,
            "psi_diffusion": 0.015,
            "cap_threshold": 0.30,
        },
    )
    r_teacher = teacher_mod.ReflectiveGeminiTeacher(seed=42, live=False)
    proposal, spec = r_teacher.propose_reflective_multi_knob(
        baseline=baseline_pol,
        generation=1,
        holo_snapshot=snap_dict,
        cortex_campaign=campaign,
        hippocampus_consolidation=consolidation,
        canonical_prefix=encoder.canonical_prefix,
        previous_interaction_id="int-hippo-prev",
    )
    assert spec.lyapunov_delta_v < 0.0
    assert spec.previous_interaction_id == "int-hippo-prev"
    assert len(spec.knob_deltas) >= 3
    assert proposal.candidate.knobs["c_press"] != baseline_pol.knobs["c_press"]
    assert proposal.candidate.knobs["damping"] != baseline_pol.knobs["damping"]
    assert proposal.candidate.knobs["psi_diffusion"] != baseline_pol.knobs["psi_diffusion"]


def test_v3_brain_manifest_end_to_end_and_fail_closed_boundaries() -> None:
    """Verify full V3BrainReflectiveOrchestrator synthesis, ledger persistence, observatory assessment, and fail-closed guards."""
    with tempfile.TemporaryDirectory(prefix="test-v3-brain-") as tmp_dir:
        tmp_path = Path(tmp_dir)
        ledger_db = tmp_path / "ledger.sqlite3"
        obs_db = tmp_path / "observatory.sqlite3"
        pkt_path = tmp_path / "packet.json"
        man_path = tmp_path / "manifest.json"
        obs_dir = tmp_path / "obs_bundle"

        orch = V3BrainReflectiveOrchestrator(model="gemini-4-argon", thinking_level="high", live=False)
        report = orch.run_v3_brain_synthesis(
            study_name="V3_Brain_Manifest_Unit_Test",
            ledger_db_path=ledger_db,
            observatory_db_path=obs_db,
            export_packet_path=pkt_path,
            export_manifest_path=man_path,
            export_observatory_dir=obs_dir,
            repeat_trial_count=5,
        )

        assert report.manifest.v3_brain_manifest_verified is True
        assert report.manifest.allow_production_execution is False
        assert report.manifest.authorized_claimed is False
        assert report.manifest.sacred_core_graph_immutable is True
        assert report.manifest.sacred_core_graph_sha256 == SACRED_DEFAULT_GRAPH_SHA256
        assert report.manifest.context_frame["prefix_token_count"] >= 4096
        assert report.manifest.context_frame["byte_identical_across_agents"] is True
        assert len(report.manifest.guild_agent_records) == 4
        assert report.manifest.cycle0_audit["policy_status"] == "QUARANTINE"
        assert report.manifest.cycle0_audit["pre_beta_1"] == 1
        assert report.manifest.cycle1_audit["policy_status"] == "ELIGIBLE"
        assert report.manifest.cycle1_audit["post_beta_1"] == 0
        assert report.manifest.edge_gate["replay_integrity_verified"] is True

        # Check ledger integrity
        assert report.ledger_record["verified"] is True
        assert report.ledger_record["v3_brain_manifest_verified"] is True
        integrity_dict = report.ledger_record["ledger_integrity"]
        assert (
            integrity_dict.get("isValid")
            or integrity_dict.get("is_valid")
            or integrity_dict.get("valid")
            or integrity_dict.get("verified")
        ) is True

        # Check observatory assessment & repeat trials
        assert report.observatory_assessment["v3_brain_manifest_verified"] is True
        assert report.observatory_assessment["comparability"] == "compatible"
        assert report.observatory_assessment["outcome"] == "improved"
        assert report.repeat_trial_evaluation["trial_count"] == 5
        assert report.repeat_trial_evaluation["outcome"] == "improved"

        # Check fail-closed rejection on allow_production_execution=True and tampered emergent_phenomena_summary
        bad_payload = report.manifest.to_dict()
        bad_payload["allow_production_execution"] = True
        ledger = GovernanceCourtLedger(db_path=ledger_db)
        try:
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(
                    evaluation_payload=bad_payload,
                    study_name="Bad_Prod_Execution",
                )
            for tamper_field, tamper_val in (
                ("awakened_subsystems_count", 6),
                ("spectral_prism_resolves_vector0", False),
                ("sheaf_cohomology_resolves_vector0_dilution", False),
            ):
                bad_em = report.manifest.to_dict()
                bad_em["emergent_phenomena_summary"] = dict(bad_em["emergent_phenomena_summary"])
                bad_em["emergent_phenomena_summary"][tamper_field] = tamper_val
                with pytest.raises(ValueError):
                    ledger.record_v3_brain_manifest_observatory_run(
                        evaluation_payload=bad_em,
                        study_name=f"Bad_Emergent_{tamper_field}",
                    )
        finally:
            ledger.close()

        # Verify standalone sol-holo/subsystems copies are byte-identical to source modules
        for src_rel, dst_rel in (
            ("sol-continuum/sol_continuum/reflective_domain.py", "sol-holo/subsystems/sol_continuum/reflective_domain.py"),
            ("sol-continuum/sol_continuum/substrate_tools.py", "sol-holo/subsystems/sol_continuum/substrate_tools.py"),
            ("sol-continuum/sol_continuum/dormant_clusters_awakening.py", "sol-holo/subsystems/sol_continuum/dormant_clusters_awakening.py"),
            ("sol-continuum/sol_continuum/exciton_snowball_bridge.py", "sol-holo/subsystems/sol_continuum/exciton_snowball_bridge.py"),
            ("sol-decide/sol_decide/delivery/governance_ledger.py", "sol-holo/subsystems/sol_decide_interop/governance_ledger.py"),
            ("sol-change/observatory/continuum.py", "sol-holo/subsystems/sol_change_observatory/continuum.py"),
        ):
            assert (_REPO_ROOT / src_rel).read_bytes() == (_REPO_ROOT / dst_rel).read_bytes(), f"Out-of-sync copy: {dst_rel}"

        # Verify sacred core graph remains untouched after all tests
        immutable_now, sha_now = verify_sacred_core_graph_sha256(_REPO_ROOT)
        assert immutable_now is True
        assert sha_now == SACRED_DEFAULT_GRAPH_SHA256


def test_sol_holo_cli_v3_brain_subcommand(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify sol_holo.cli v3-brain subcommand returns exit code 0 and valid JSON."""
    rc = sol_holo_cli_main(["v3-brain", "--trials", "3"])
    assert rc == 0
    captured = capsys.readouterr().out
    payload = json.loads(captured)
    assert payload["manifest"]["v3_brain_manifest_verified"] is True
    assert payload["manifest"]["allow_production_execution"] is False


def test_real_google_genai_model_output_content_list_and_usage_extraction() -> None:
    """Verify google-genai step.type=='model_output' with step.content=[Content(type='text', text=...)] is extracted without repr corruption."""
    client_mod = _load_tool_module("sol_llm_client_v3_content_test", "sol/tools/sol-llm/client.py")
    from sol_decide.agentic.live_llm_elicitation import LiveGeminiMoAElicitor

    class _TypedContentPart:
        def __init__(self, part_type: str, text: str) -> None:
            self.type = part_type
            self.text = text

    class _ModelOutputStep:
        def __init__(self, parts: list[_TypedContentPart]) -> None:
            self.type = "model_output"
            self.content = parts

    class _ThoughtStep:
        def __init__(self, summary_parts: list[_TypedContentPart], signature: bytes) -> None:
            self.type = "thought"
            self.summary = summary_parts
            self.signature = signature

    class _TotalUsageObj:
        def __init__(self) -> None:
            self.total_input_tokens = 4820
            self.total_output_tokens = 640
            self.total_thought_tokens = 2048
            self.total_cached_input_tokens = 4560

    class _SDKInteraction:
        def __init__(self, int_id: str, status: str, steps: list[Any]) -> None:
            self.id = int_id
            self.status = status
            self.outputs = steps
            self.output_text = '{"part_a": 42'  # intentionally truncated so multi-hop wins
            self.usage = _TotalUsageObj()

    completed_steps = [
        _ThoughtStep([_TypedContentPart("text", "First thought hop."), _TypedContentPart("text", " Second hop.")], b"sig-bytes-001"),
        _ModelOutputStep([_TypedContentPart("text", '{"part_a": 42, ')]),
        _ModelOutputStep([_TypedContentPart("text", '"part_b": "verified"}')]),
    ]
    completed_interaction = _SDKInteraction("int-sdk-typed-001", "completed", completed_steps)

    telemetry = client_mod.extract_gemini_interaction_telemetry(completed_interaction)
    assert json.loads(telemetry["content"]) == {"part_a": 42, "part_b": "verified"}
    assert telemetry["total_input_tokens"] == 4820
    assert telemetry["total_output_tokens"] == 640
    assert telemetry["total_thought_tokens"] == 2048
    assert telemetry["total_cached_input_tokens"] == 4560
    assert telemetry["thought_step_count"] == 1
    assert "First thought hop. Second hop." in telemetry["thought_summaries"][0]

    extracted_moa = LiveGeminiMoAElicitor._extract_interaction_output_text(completed_interaction)
    assert json.loads(extracted_moa) == {"part_a": 42, "part_b": "verified"}


def test_v3_brain_orchestrator_live_background_polling_and_stateful_guild_chain() -> None:
    """Verify V3BrainReflectiveOrchestrator(live=True, background=True) polls client.interactions.get across all 4 guild agents."""

    class _TypedContentPart:
        def __init__(self, text: str) -> None:
            self.type = "text"
            self.text = text

    class _StepObj:
        def __init__(self, step_type: str, content_text: str = "", sig: str = "") -> None:
            self.type = step_type
            if step_type == "thought":
                self.summary = [_TypedContentPart(content_text)]
                self.signature = sig
            else:
                self.content = [_TypedContentPart(content_text)]

    class _AsyncGuildInteractionsAPI:
        def __init__(self) -> None:
            self.create_calls: list[dict[str, Any]] = []
            self.poll_calls: list[str] = []
            self._poll_counts: dict[str, int] = {}
            self._payloads: dict[str, str] = {}

        def create(self, **kwargs: Any) -> Any:
            idx = len(self.create_calls) + 1
            int_id = f"live-guild-int-{idx:02d}"
            self.create_calls.append(kwargs)
            self._poll_counts[int_id] = 0
            prompt_str = str(kwargs.get("input", ""))
            if "Holo_Substrate_Synthesizer" in prompt_str:
                self._payloads[int_id] = json.dumps({
                    "substrate_ready": True,
                    "verified_frontiers": 26,
                    "synthesis_note": "Live Argon background-polled substrate verification complete.",
                })
            elif "Cortical_Epistemic_Architect" in prompt_str:
                self._payloads[int_id] = json.dumps({
                    "campaign_id": "camp_live_argon_bg",
                    "coupled_knobs": ["c_press", "damping", "psi_diffusion", "cap_threshold"],
                    "recommended_knob_targets": {"c_press": 0.486, "damping": 0.874, "psi_diffusion": 0.026, "cap_threshold": 0.332},
                    "epistemic_synthesis_rationale": "Live Argon multi-protocol epistemic synthesis verified.",
                })
            elif "Hippocampal_Dream_Consolidator" in prompt_str:
                self._payloads[int_id] = json.dumps({
                    "dream_session_id": "dream_live_argon_bg",
                    "consolidated_basin_count": 12,
                    "mahalanobis_isometry_r": 0.9982,
                    "rule_7_law_statement": "Live Argon Rule 7 Law promoted with sacred core immutability.",
                })
            else:
                self._payloads[int_id] = json.dumps({
                    "coupled_knobs": ["c_press", "damping", "psi_diffusion", "cap_threshold"],
                    "knob_adjustments": {"c_press": 0.486, "damping": 0.874, "psi_diffusion": 0.026, "cap_threshold": 0.332},
                    "lyapunov_delta_v": -0.365,
                    "predicted_anchor_delta": 0.048,
                    "predicted_explore_delta": 0.039,
                    "rationale": "Live Argon coordinated 4-knob Lyapunov contraction.",
                    "compiled_test_assertion": "assert lyapunov_delta_v < 0.0",
                })

            class _PendingInteraction:
                def __init__(self, i_id: str) -> None:
                    self.id = i_id
                    self.status = "in_progress"
                    self.outputs = []

            return _PendingInteraction(int_id)

        def get(self, id: str) -> Any:
            self.poll_calls.append(id)
            self._poll_counts[id] = self._poll_counts.get(id, 0) + 1
            if self._poll_counts[id] < 2:
                class _QueuedInteraction:
                    def __init__(self, i_id: str) -> None:
                        self.id = i_id
                        self.status = "queued"
                        self.outputs = []
                return _QueuedInteraction(id)

            payload_str = self._payloads[id]
            mid = len(payload_str) // 2

            class _DoneInteraction:
                def __init__(self, i_id: str) -> None:
                    self.id = i_id
                    self.status = "completed"
                    self.outputs = [
                        _StepObj("thought", f"Completed high-thinking reflection for {i_id}", sig=f"sig-{i_id}"),
                        _StepObj("model_output", payload_str[:mid]),
                        _StepObj("model_output", payload_str[mid:]),
                    ]

            return _DoneInteraction(id)

    class _MockAsyncGenAIClient:
        def __init__(self) -> None:
            self.interactions = _AsyncGuildInteractionsAPI()

    mock_client = _MockAsyncGenAIClient()
    orch = V3BrainReflectiveOrchestrator(
        model="gemini-4-argon",
        thinking_level="high",
        live=True,
        gemini_client=mock_client,
        background=True,
    )
    orch.poll_interval_s = 0.005
    rep = orch.run_v3_brain_synthesis(
        study_name="V3_Brain_Live_Background_Test",
        repeat_trial_count=3,
    )

    # All 4 guild agents invoked create() with background=True and polled get() twice each
    assert len(mock_client.interactions.create_calls) == 4
    assert len(mock_client.interactions.poll_calls) == 8
    for idx, call_kw in enumerate(mock_client.interactions.create_calls):
        assert call_kw["model"] == "gemini-4-argon"
        assert call_kw.get("background") is True
        gen_cfg = call_kw["generation_config"]
        assert gen_cfg["thinking_level"] == "high"
        assert gen_cfg["max_output_tokens"] >= 32768
        assert "temperature" not in gen_cfg
        assert "top_p" not in gen_cfg
        assert "top_k" not in gen_cfg
        if idx > 0:
            assert call_kw.get("previous_interaction_id") == f"live-guild-int-{idx:02d}"

    assert rep.manifest.v3_brain_manifest_verified is True
    assert [r["interaction_id"] for r in rep.manifest.guild_agent_records] == [
        "live-guild-int-01",
        "live-guild-int-02",
        "live-guild-int-03",
        "live-guild-int-04",
    ]
    assert rep.manifest.cortex_epistemic_campaign["epistemic_synthesis_rationale"] == (
        "Live Argon multi-protocol epistemic synthesis verified."
    )
    assert rep.manifest.hippocampus_dream_consolidation["promoted_law"]["statement"] == (
        "Live Argon Rule 7 Law promoted with sacred core immutability."
    )
    assert rep.manifest.rsi_self_train_synthesis["rationale"] == (
        "Live Argon coordinated 4-knob Lyapunov contraction."
    )


def test_governance_ledger_v3_brain_tamper_rejection_and_thought_signature_persistence() -> None:
    """Verify GovernanceCourtLedger persists all 4 guild thought signatures and rejects tampered V3 Brain payloads."""
    with tempfile.TemporaryDirectory(prefix="test-v3-ledger-tamper-") as tmp_dir:
        tmp_path = Path(tmp_dir)
        ledger_db = tmp_path / "ledger.sqlite3"
        orch = V3BrainReflectiveOrchestrator(model="gemini-4-argon", thinking_level="high", live=False)
        report = orch.run_v3_brain_synthesis(
            study_name="V3_Brain_Ledger_Tamper_Suite",
            ledger_db_path=ledger_db,
            repeat_trial_count=3,
        )

        ledger = GovernanceCourtLedger(db_path=ledger_db)
        try:
            run_id = report.ledger_record["run_id"]
            sigs = ledger.list_thought_signatures(run_id=run_id)
            assert len(sigs) == 4
            assert [s["agentRole"] for s in sigs] == list(REFLECTIVE_GUILD_AGENT_ROLES)

            base_dict = report.manifest.to_dict()

            # 1. Explicit v3_brain_manifest_verified=False must be rejected
            t1 = json.loads(json.dumps(base_dict))
            t1["v3_brain_manifest_verified"] = False
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(t1)

            # 2. Tampered sacred_core_graph_sha256 must be rejected
            t2 = json.loads(json.dumps(base_dict))
            t2["sacred_core_graph_sha256"] = "0" * 64
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(t2)

            # 3. Tampered guild thought_signature_digest must be rejected
            t3 = json.loads(json.dumps(base_dict))
            t3["guild_agent_records"][1]["thought_signature_digest"] = "not-a-valid-hex-digest"
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(t3)

            # 4. Prefix token count < 4096 must be rejected
            t4 = json.loads(json.dumps(base_dict))
            t4["context_frame"]["prefix_token_count"] = 2048
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(t4)

            # 5. Tampered artifact_digest must be rejected
            t5 = json.loads(json.dumps(base_dict))
            t5["artifact_digest"] = "f" * 64
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(t5)

            # 6. Invalid cycle0_audit or cycle1_audit status must be rejected
            t6 = json.loads(json.dumps(base_dict))
            t6["cycle1_audit"]["policy_status"] = "QUARANTINE"
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(t6)

            # 7. Verify live token telemetry (input_tokens, thought_tokens, output_tokens) is persisted in gemini_thought_signatures
            t_live = json.loads(json.dumps(base_dict))
            t_live["guild_agent_records"][0]["input_tokens"] = 15425
            t_live["guild_agent_records"][0]["thought_tokens"] = 778
            t_live["guild_agent_records"][0]["output_tokens"] = 323
            t_live["guild_agent_records"][3]["interaction_id"] = "v1_Chd5a3IzYWNx LiveTurn4"
            t_live["cycle1_audit"]["repair_interaction_id"] = "v1_Chd5a3IzYWNx LiveTurn4"
            t_live["cycle1_audit"]["previous_interaction_id"] = "v1_Chd1a3IzYWNx LiveTurn3"
            rec_live = ledger.record_v3_brain_manifest_observatory_run(t_live)
            sigs_live = ledger.list_thought_signatures(run_id=rec_live["run_id"])
            assert sigs_live[0]["inputTokens"] == 15425
            assert sigs_live[0]["thoughtTokens"] == 778
            assert sigs_live[0]["outputTokens"] == 323
        finally:
            ledger.close()


def test_partial_guild_failure_retry_and_fallback_chaining() -> None:
    """Verify transient API rate-limit retry and fallback chaining when an intermediate guild agent fails."""
    class _StepItem:
        def __init__(self, step_type: str, content_text: str = "", sig: str = "") -> None:
            self.type = step_type
            if step_type == "thought":
                self.summary = content_text
                self.signature = sig
            else:
                self.text = content_text

    class _FlakyGuildInteractionsAPI:
        def __init__(self, fail_agent3_permanently: bool = False) -> None:
            self.fail_agent3_permanently = fail_agent3_permanently
            self.create_calls: list[dict[str, Any]] = []
            self.agent3_attempts = 0
            self._turn = 0

        def create(self, **kwargs: Any) -> Any:
            prompt_str = str(kwargs.get("input", ""))
            if "[AGENT_ROLE]: Hippocampal_Dream_Consolidator" in prompt_str:
                self.agent3_attempts += 1
                if self.fail_agent3_permanently or self.agent3_attempts == 1:
                    raise RuntimeError("HTTP 429 Resource Exhausted: simulated transient rate limit")
            self.create_calls.append(kwargs)
            self._turn += 1
            int_id = f"live-flaky-int-{self._turn:02d}"

            if "[AGENT_ROLE]: Cortical_Epistemic_Architect" in prompt_str:
                out_json = json.dumps({
                    "campaign_id": "camp_flaky_v3",
                    "coupled_knobs": ["c_press", "damping", "psi_diffusion", "cap_threshold"],
                    "recommended_knob_targets": {"c_press": 0.486, "damping": 0.874, "psi_diffusion": 0.026, "cap_threshold": 0.332},
                    "epistemic_synthesis_rationale": "Recovered cortical campaign.",
                })
            elif "[AGENT_ROLE]: Hippocampal_Dream_Consolidator" in prompt_str:
                out_json = json.dumps({
                    "dream_session_id": "dream_flaky_v3",
                    "consolidated_basin_count": 12,
                    "mahalanobis_isometry_r": 0.9981,
                    "rule_7_law_statement": "Recovered hippocampal Rule 7 Law.",
                })
            elif "[AGENT_ROLE]: RSI_SelfTrain_Policy_Inventor" in prompt_str:
                out_json = json.dumps({
                    "coupled_knobs": ["c_press", "damping", "psi_diffusion", "cap_threshold"],
                    "knob_adjustments": {"c_press": 0.486, "damping": 0.874, "psi_diffusion": 0.026, "cap_threshold": 0.332},
                    "lyapunov_delta_v": -0.0412,
                    "predicted_anchor_delta": 0.0510,
                    "predicted_explore_delta": 0.0390,
                    "rationale": "Recovered RSI synthesis.",
                    "compiled_test_assertion": "assert lyapunov_delta_v == -0.0412",
                })
            else:
                out_json = json.dumps({
                    "substrate_ready": True,
                    "verified_frontiers": 26,
                    "synthesis_note": "Substrate ready.",
                })

            class _DoneObj:
                def __init__(self) -> None:
                    self.id = int_id
                    self.status = "completed"
                    self.outputs = [
                        _StepItem("thought", f"Thought for {int_id}", sig=f"sig-{int_id}"),
                        _StepItem("model_output", out_json),
                    ]

            return _DoneObj()

    class _FlakyClient:
        def __init__(self, fail_permanently: bool) -> None:
            self.interactions = _FlakyGuildInteractionsAPI(fail_agent3_permanently=fail_permanently)

    # Case A: Agent 3 fails once with HTTP 429, succeeds on retry 2
    client_retry = _FlakyClient(fail_permanently=False)
    orch_retry = V3BrainReflectiveOrchestrator(
        model="gemini-4-argon",
        thinking_level="high",
        live=True,
        gemini_client=client_retry,
    )
    orch_retry.poll_interval_s = 0.001
    rep_retry = orch_retry.run_v3_brain_synthesis(repeat_trial_count=3)
    assert client_retry.interactions.agent3_attempts == 2
    assert rep_retry.manifest.v3_brain_manifest_verified is True
    assert rep_retry.manifest.hippocampus_dream_consolidation["mahalanobis_isometry_r"] == 0.9981
    assert rep_retry.manifest.rsi_self_train_synthesis["lyapunov_delta_v"] == -0.0412
    assert rep_retry.manifest.rsi_self_train_synthesis["delta_anchor_score"] == 0.0510

    # Case B: Agent 3 fails all 3 retries and falls back cleanly; Agent 4 still chains to Agent 2's live ID
    client_fb = _FlakyClient(fail_permanently=True)
    orch_fb = V3BrainReflectiveOrchestrator(
        model="gemini-4-argon",
        thinking_level="high",
        live=True,
        gemini_client=client_fb,
    )
    orch_fb.poll_interval_s = 0.001
    rep_fb = orch_fb.run_v3_brain_synthesis(repeat_trial_count=3)
    assert client_fb.interactions.agent3_attempts == 3
    assert rep_fb.manifest.v3_brain_manifest_verified is True
    records_fb = rep_fb.manifest.guild_agent_records
    assert records_fb[0]["interaction_id"] == "live-flaky-int-01"
    assert records_fb[1]["interaction_id"] == "live-flaky-int-02"
    assert records_fb[2]["interaction_id"].startswith("int_v3_hippocampus_")
    # Agent 4 must chain to Agent 2's live interaction ID ("live-flaky-int-02") rather than dropping the chain
    assert records_fb[3]["previous_interaction_id"] == "live-flaky-int-02"
    assert records_fb[3]["interaction_id"] == "live-flaky-int-03"


def test_reflective_teacher_out_of_range_clamping_and_lyapunov_preservation() -> None:
    """Verify ReflectiveGeminiTeacher clamps out-of-range/NaN knobs and preserves negative lyapunov_delta_v in (-0.05, 0)."""
    teacher_mod = _load_tool_module("sol_evolve_teacher_clamp_test", "sol/tools/sol-evolve/self_train/teacher.py")
    models_mod = _load_tool_module("sol_evolve_models_clamp_test", "sol/tools/sol-evolve/self_train/models.py")

    class _StepItem:
        def __init__(self, step_type: str, content_text: str = "", sig: str = "") -> None:
            self.type = step_type
            if step_type == "thought":
                self.summary = content_text
                self.signature = sig
            else:
                self.text = content_text

    class _ExtremeOutputInteractions:
        def create(self, **kwargs: Any) -> Any:
            out_json = json.dumps({
                "coupled_knobs": ["c_press", "damping", "psi_diffusion", "cap_threshold"],
                "knob_adjustments": {
                    "c_press": -999.0,
                    "damping": 999.0,
                    "psi_diffusion": 0.025,
                    "cap_threshold": 0.33,
                },
                "lyapunov_delta_v": -0.0365,
                "predicted_anchor_delta": 0.0112,
                "predicted_explore_delta": 0.0041,
                "rationale": "Clamping and exact negative Lyapunov preservation test.",
                "compiled_test_assertion": "assert candidate.knobs['psi_diffusion'] == 0.025 and lyapunov_delta_v == -0.0365",
            })

            class _Resp:
                id = "live-clamp-int-01"
                status = "completed"
                outputs = [
                    _StepItem("thought", "Testing extreme knob clamping.", sig="sig-clamp-01"),
                    _StepItem("model_output", out_json),
                ]
            return _Resp()

    class _ExtremeClient:
        interactions = _ExtremeOutputInteractions()

    knob_bounds = {
        "c_press": (0.30, 0.60),
        "damping": (0.70, 0.95),
        "psi_diffusion": (0.01, 0.06),
        "cap_threshold": (0.20, 0.50),
    }
    baseline = models_mod.Policy(
        policy_id="policy-g000",
        generation=0,
        knobs={"c_press": 0.45, "damping": 0.85, "psi_diffusion": 0.03, "cap_threshold": 0.35},
    )
    teacher = teacher_mod.ReflectiveGeminiTeacher(
        knob_bounds=knob_bounds,
        live=True,
        gemini_client=_ExtremeClient(),
    )
    # Also verify non-finite NaN/Inf clamping directly
    nan_clamped = teacher._clamp_knob("c_press", float("nan"))
    assert 0.30 < nan_clamped < 0.60

    proposal, spec = teacher.propose_reflective(baseline=baseline, generation=1)
    for k, (lo, hi) in knob_bounds.items():
        assert lo < proposal.candidate.knobs[k] < hi
    assert spec.lyapunov_delta_v == -0.0365
    assert spec.predicted_anchor_delta == 0.0112
    assert spec.predicted_explore_delta == 0.0041
    assert spec.compiled_test_assertion == "assert candidate.knobs['psi_diffusion'] == 0.025 and lyapunov_delta_v == -0.0365"


def test_substrate_tool_sandbox_all_six_emergent_subsystems_and_edge_cases() -> None:
    """Verify all 12 awakened emergent subsystems in SubstrateToolSandbox plus boundary/error edge cases."""
    from sol_continuum.substrate_tools import SUBSTRATE_TOOL_DECLARATIONS, SubstrateToolSandbox

    assert len(SUBSTRATE_TOOL_DECLARATIONS) == 12
    for decl in SUBSTRATE_TOOL_DECLARATIONS:
        assert decl["type"] == "function"
        assert "name" in decl and "parameters" in decl

    sandbox = SubstrateToolSandbox(repo_root=_REPO_ROOT)
    live_telemetry = sandbox.get_live_node_telemetry()
    assert len(live_telemetry) == 140
    assert live_telemetry[0]["id"] == 1
    assert live_telemetry[0]["index"] == 0
    assert "rho" in live_telemetry[0] and "psi" in live_telemetry[0]

    # Run all 12 awakened subsystems
    summary = sandbox.run_deterministic_suite()
    assert len(sandbox.tool_executions) == 12
    assert summary["awakened_subsystems_count"] == 12
    assert summary["tool_execution_count"] == 12
    assert summary["superposition_shannon_entropy_bits"] > 0.0
    assert summary["working_memory_distractor_crosstalk"] == 0.0
    assert summary["wideword_64bit_mismatches"] == 0
    assert summary["causal_emergence_swarm_delta_ei_bits"] > 0.0
    assert summary["causal_emergence_riemannian_delta_ei_bits"] > 0.0
    assert summary["has_causal_emergence"] is True
    assert summary["spectral_prism_resolves_vector0"] is True
    assert summary["sheaf_cohomology_resolves_vector0_dilution"] is True
    assert summary["exciton_paper_claims_count"] >= 1
    assert summary["vectorized_csr_kernel_parity_passed"] is True
    assert summary["phonon_fdm_selectivity_verified"] is True
    assert summary["kb_hippocampus_chunks_indexed"] > 0
    assert summary["sovereign_rangers_patrolled_count"] == 57
    assert summary["spectral_prism_6d_l2_distance"] > 2.0
    assert summary["sacred_core_graph_immutable"] is True
    assert summary["sacred_core_graph_sha256"] == SACRED_DEFAULT_GRAPH_SHA256

    # Edge cases: extreme/out-of-bounds parameters clamp safely without crashing or mutating default_graph.json
    res_clamp = sandbox.execute_tool(
        "sol_fork_and_rollout_superposition",
        {"c_press": -50.0, "damping": 50.0, "steps": -10},
    )
    assert res_clamp["shannon_entropy_bits"] > 0.0
    assert res_clamp["state_restored_exact"] is True

    res_surg_fallback = sandbox.execute_tool(
        "sol_sandbox_topology_surgery",
        {"surgery_type": "NONEXISTENT_SURGERY", "steps": 0},
    )
    assert res_surg_fallback["surgery_type"] == "BRIDGE_ADD"
    assert res_surg_fallback["ricci_metric_positive_definite"] is True

    # Unknown tool name must raise ValueError
    with pytest.raises(ValueError, match="Unknown substrate tool"):
        sandbox.execute_tool("sol_nonexistent_tool", {})

    immutable_after, sha_after = verify_sacred_core_graph_sha256(_REPO_ROOT)
    assert immutable_after is True
    assert sha_after == SACRED_DEFAULT_GRAPH_SHA256


def test_run_gemini_interaction_with_tools_multi_turn_function_calling() -> None:
    """Verify multi-turn step.type=='function_call' -> function_result loop chained via previous_interaction_id."""
    client_mod = _load_tool_module("sol_llm_client_tools_test", "sol/tools/sol-llm/client.py")
    from sol_continuum.substrate_tools import SUBSTRATE_TOOL_DECLARATIONS

    class _FuncCallStep:
        def __init__(self, call_id: str, name: str, arguments: dict[str, Any]) -> None:
            self.type = "function_call"
            self.id = call_id
            self.name = name
            self.arguments = arguments

    class _ThoughtStep:
        def __init__(self, text: str, sig: str) -> None:
            self.type = "thought"
            self.summary = text
            self.signature = sig

    class _TextStep:
        def __init__(self, text: str) -> None:
            self.type = "text"
            self.text = text

    class _Usage:
        def __init__(self, inp: int, out: int, th: int, cached: int) -> None:
            self.total_input_tokens = inp
            self.total_output_tokens = out
            self.total_thought_tokens = th
            self.total_cached_input_tokens = cached

    class _MultiTurnToolInteractionsAPI:
        def __init__(self) -> None:
            self.calls: list[dict[str, Any]] = []

        def create(self, **kwargs: Any) -> Any:
            self.calls.append(kwargs)
            turn = len(self.calls)
            if turn == 1:
                class _Turn1:
                    id = "int-tool-turn-1"
                    status = "completed"
                    outputs = [
                        _ThoughtStep("Evaluating superposition and causal emergence tools.", "sig-tool-turn-1"),
                        _FuncCallStep("call-001", "sol_fork_and_rollout_superposition", {"c_press": 0.48, "damping": 0.87, "steps": 8}),
                        _FuncCallStep("call-002", "sol_evaluate_photonic_sheaf_and_causal_emergence", {"sheaf_Steps": 10}),
                    ]
                    usage = _Usage(14500, 180, 420, 14080)
                return _Turn1()
            else:
                class _Turn2:
                    id = "int-tool-turn-2"
                    status = "completed"
                    outputs = [
                        _ThoughtStep("Synthesizing final substrate verification from tool outputs.", "sig-tool-turn-2"),
                        _TextStep(json.dumps({
                            "substrate_ready": True,
                            "verified_frontiers": 26,
                            "synthesis_note": "Verified via live multi-turn tool calls.",
                        })),
                    ]
                    usage = _Usage(14900, 210, 510, 14400)
                return _Turn2()

    class _MockToolClient:
        def __init__(self) -> None:
            self.interactions = _MultiTurnToolInteractionsAPI()

    dispatched_calls: list[tuple[str, dict[str, Any]]] = []

    def _dispatcher(name: str, args: dict[str, Any]) -> dict[str, Any]:
        dispatched_calls.append((name, args))
        return {"status": "ok", "tool_name": name, "echo_args": args}

    mock_client = _MockToolClient()
    result = client_mod.run_gemini_interaction_with_tools(
        client=mock_client,
        model="gemini-4-argon",
        prompt="Run emergent substrate tools and synthesize report.",
        tools=SUBSTRATE_TOOL_DECLARATIONS,
        tool_dispatcher=_dispatcher,
        thinking_level="high",
        max_output_tokens=32768,
        previous_interaction_id="int-prev-root",
    )

    assert len(mock_client.interactions.calls) == 2
    assert mock_client.interactions.calls[0]["previous_interaction_id"] == "int-prev-root"
    assert mock_client.interactions.calls[1]["previous_interaction_id"] == "int-tool-turn-1"
    turn2_input = mock_client.interactions.calls[1]["input"]
    assert isinstance(turn2_input, list) and len(turn2_input) == 2
    assert turn2_input[0]["type"] == "function_result"
    assert turn2_input[0]["call_id"] == "call-001"
    assert turn2_input[1]["call_id"] == "call-002"

    assert len(dispatched_calls) == 2
    assert result["interaction_id"] == "int-tool-turn-2"
    assert result["thought_step_count"] == 2
    assert len(result["thought_signature_digests"]) == 2
    assert len(result["tool_executions"]) == 2
    assert result["total_input_tokens"] == 14500 + 14900
    assert result["total_output_tokens"] == 180 + 210
    assert result["total_thought_tokens"] == 420 + 510
    assert json.loads(result["content"])["substrate_ready"] is True


def test_governance_ledger_emergent_substrate_tamper_rejection() -> None:
    """Verify GovernanceCourtLedger rejects tampered emergent_phenomena_summary and substrate_tool_executions."""
    with tempfile.TemporaryDirectory(prefix="test-v3-emergent-tamper-") as tmp_dir:
        ledger_db = Path(tmp_dir) / "ledger.sqlite3"
        orch = V3BrainReflectiveOrchestrator(model="gemini-4-argon", thinking_level="high", live=False)
        report = orch.run_v3_brain_synthesis(
            study_name="V3_Brain_Emergent_Tamper_Test",
            ledger_db_path=ledger_db,
            repeat_trial_count=3,
        )
        base_dict = report.manifest.to_dict()
        assert len(base_dict["substrate_tool_executions"]) == 12
        assert base_dict["emergent_phenomena_summary"]["has_causal_emergence"] is True
        assert base_dict["emergent_phenomena_summary"]["spectral_prism_resolves_vector0"] is True
        assert base_dict["emergent_phenomena_summary"]["sheaf_cohomology_resolves_vector0_dilution"] is True

        ledger = GovernanceCourtLedger(db_path=ledger_db)
        try:
            # 1. Tamper tool execution_digest
            bad_exec = json.loads(json.dumps(base_dict))
            bad_exec["substrate_tool_executions"][0]["execution_digest"] = "invalid-digest"
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_exec)

            # 2. Tamper has_causal_emergence=False
            bad_ce = json.loads(json.dumps(base_dict))
            bad_ce["emergent_phenomena_summary"]["has_causal_emergence"] = False
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_ce)

            # 3. Tamper working_memory_distractor_crosstalk > 0
            bad_wm = json.loads(json.dumps(base_dict))
            bad_wm["emergent_phenomena_summary"]["working_memory_distractor_crosstalk"] = 0.12
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_wm)

            # 4. Tamper wideword_64bit_mismatches > 0
            bad_ww = json.loads(json.dumps(base_dict))
            bad_ww["emergent_phenomena_summary"]["wideword_64bit_mismatches"] = 2
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_ww)

            # 5. Tamper tool execution result payload without updating execution_digest (cryptographic mismatch)
            bad_res_hash = json.loads(json.dumps(base_dict))
            bad_res_hash["substrate_tool_executions"][0]["result"]["shannon_entropy_bits"] = 999.0
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_res_hash)

            # 6. Tamper spectral_prism_resolves_vector0=False
            bad_spec = json.loads(json.dumps(base_dict))
            bad_spec["emergent_phenomena_summary"]["spectral_prism_resolves_vector0"] = False
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_spec)

            # 7. Tamper sheaf_cohomology_resolves_vector0_dilution=False
            bad_sheaf = json.loads(json.dumps(base_dict))
            bad_sheaf["emergent_phenomena_summary"]["sheaf_cohomology_resolves_vector0_dilution"] = False
            with pytest.raises(ValueError, match="fail-closed"):
                ledger.record_v3_brain_manifest_observatory_run(bad_sheaf)
        finally:
            ledger.close()


def test_engine_grounded_snapshot_encoder_and_tool_edge_cases() -> None:
    """
    Verify:
      1. HolographicSubstrateSnapshot.capture_from_organism(engine=...) populates emergent_substrate_metrics.
      2. HolographicContextEncoder(engine=...) encodes live_v, gru_h_norm_l2 (||h_i||_2), node_degree, and incident_edge_weights.
      3. sol_synthesize_and_reflect_circuit awakens SwarmGuidedSynthesizer, MetacognitiveOrchestrator, MetaplasticityEngine, and OracleWideWordVM.
      4. run_gemini_interaction_with_tools handles malformed/string function_call arguments and max_tool_rounds fallback turn.
      5. sol_decide.cli and sol_holo.cli accept --enable-substrate-tools, --no-substrate-tools, and --max-tool-rounds.
    """
    from sol_continuum.substrate_tools import SUBSTRATE_TOOL_DECLARATIONS, SubstrateToolSandbox

    sandbox = SubstrateToolSandbox(repo_root=_REPO_ROOT)
    snap = HolographicSubstrateSnapshot.capture_from_organism(
        repo_root=_REPO_ROOT,
        engine=sandbox.engine,
    )
    assert "emergent_substrate_metrics" in snap.to_dict()
    assert "dormant_subsystems_awakening_summary" in snap.to_dict()
    assert snap.dormant_subsystems_awakening_summary["awakened_subsystems_total"] == 12
    assert snap.dormant_subsystems_awakening_summary["cross_language_mjs_py_parity_verified"] is True
    assert snap.emergent_substrate_metrics["gru_h_dim"] == 8
    assert snap.emergent_substrate_metrics["superposition_shannon_entropy_bits"] > 0.0
    assert snap.emergent_substrate_metrics["hoel_causal_emergence_delta_ei_bits"] > 0.0

    enc = HolographicContextEncoder(snapshot=snap, engine=sandbox.engine)
    assert "continuity_and_cognitive_load" in enc.hippocampus_overlay_summary
    assert len(enc.hippocampus_overlay_summary["continuity_and_cognitive_load"]["next_damping_window"]) == 2
    catalog = enc._build_140_node_canonical_catalog()
    assert len(catalog) == 140
    assert any(n["live_v"] != 0.0 for n in catalog)
    assert any(n["gru_h_norm_l2"] > 0.0 for n in catalog)
    assert all("node_degree" in n and "incident_edge_weights" in n for n in catalog)
    prefix_text = enc.encode_canonical_prefix()
    assert "||h_i||_2=" in prefix_text
    assert "edge_w=" in prefix_text
    assert "continuity_and_cognitive_load" in prefix_text
    assert callable(getattr(sandbox, "run_all_emergent_tools", None))

    synth_res = sandbox.execute_tool("sol_synthesize_and_reflect_circuit", {"spec_name": "XOR", "word_width": 64})
    assert synth_res["swarm_consensus_score"] > 0.8
    assert synth_res["metacognitive_plan_verified"] is True
    assert synth_res["metaplasticity_healed"] is True
    assert synth_res["wideword_oracle_match"] is True
    assert synth_res["wideword_mismatches"] == 0
    assert sandbox.tool_executions[-1]["pre_execution_sacred_graph_immutable"] is True
    assert sandbox.tool_executions[-1]["post_execution_sacred_graph_immutable"] is True

    phot_res = sandbox.execute_tool("sol_evaluate_photonic_sheaf_and_causal_emergence", {"roundtrips": 15, "noise_eps": 0.02})
    assert phot_res["hoel_canonical_delta_ei_bits"] > 0.0

    lum_res = sandbox.execute_tool("sol_compile_lumina_agent_and_claim", {"basin_name": "Basin_A_SUM"})
    assert lum_res["dispatcher_hotfix_intercepted"] is True

    # Test malformed/string function_call arguments and max_tool_rounds exhaustion fallback
    client_mod = _load_tool_module("sol_llm_client_edge_test", "sol/tools/sol-llm/client.py")

    class _RawFuncStep:
        def __init__(self, call_id: str, name: str, arguments: Any) -> None:
            self.type = "function_call"
            self.id = call_id
            self.name = name
            self.arguments = arguments

    class _TextStep:
        def __init__(self, text: str) -> None:
            self.type = "text"
            self.text = text

    class _ExhaustMaxRoundsInteractionsAPI:
        def __init__(self) -> None:
            self.calls: list[dict[str, Any]] = []

        def create(self, **kwargs: Any) -> Any:
            self.calls.append(kwargs)
            turn = len(self.calls)
            if turn == 1:
                # Valid JSON string arguments + malformed JSON string arguments
                class _T1:
                    id = "int-edge-1"
                    status = "completed"
                    outputs = [
                        _RawFuncStep("c-str", "sol_fork_and_rollout_superposition", '{"c_press": 0.48, "damping": 0.87, "psi_diffusion": 0.026}'),
                        _RawFuncStep("c-bad", "sol_control_gated_working_memory", "{malformed_json"),
                    ]
                    usage = None
                return _T1()
            elif turn == 2:
                # Still returning function_call at round 2 (exhausting max_tool_rounds=2)
                class _T2:
                    id = "int-edge-2"
                    status = "completed"
                    outputs = [
                        _RawFuncStep("c-none", "sol_sandbox_topology_surgery", None),
                    ]
                    usage = None
                return _T2()
            else:
                # Fallback final turn with response_format and no tools
                class _T3:
                    id = "int-edge-final"
                    status = "completed"
                    outputs = [
                        _TextStep(json.dumps({"substrate_ready": True, "verified_frontiers": 26, "synthesis_note": "Fallback turn succeeded."}))
                    ]
                    usage = None
                return _T3()

    class _MockEdgeClient:
        def __init__(self) -> None:
            self.interactions = _ExhaustMaxRoundsInteractionsAPI()

    dispatched: list[tuple[str, dict[str, Any]]] = []
    edge_client = _MockEdgeClient()
    edge_res = client_mod.run_gemini_interaction_with_tools(
        client=edge_client,
        model="gemini-4-argon",
        prompt="Test edge cases",
        tools=SUBSTRATE_TOOL_DECLARATIONS,
        tool_dispatcher=lambda n, a: (dispatched.append((n, a)) or {"ok": True}),
        max_tool_rounds=2,
        response_format={"type": "text", "mime_type": "application/json"},
    )
    assert len(edge_client.interactions.calls) == 3
    assert "tools" not in edge_client.interactions.calls[2]
    assert "response_format" in edge_client.interactions.calls[2]
    assert dispatched[0] == ("sol_fork_and_rollout_superposition", {"c_press": 0.48, "damping": 0.87, "psi_diffusion": 0.026})
    assert dispatched[1] == ("sol_control_gated_working_memory", {"raw": "{malformed_json"})
    assert dispatched[2] == ("sol_sandbox_topology_surgery", {})
    assert json.loads(edge_res["content"])["synthesis_note"] == "Fallback turn succeeded."
    # Verify sandbox handles coerced malformed JSON kwargs cleanly
    malformed_exec = sandbox.execute_tool(dispatched[1][0], dispatched[1][1])
    assert malformed_exec["sacred_core_graph_immutable"] is True
