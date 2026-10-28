"""
SOL-Holo (`sol_holo`)
=====================

Holographic Autopoietic Continuum & Sovereign Digital Organism spanning Frontiers A–T
across `c:\\sol-systems` (`sol-decide`, `sol-edge`, `sol-continuum`, `sol-change`,
`Frontier_OS`, `conJecture`, `sol`, and `sol-lens`).
"""

from .holo_engine import (
    FRONTIER_CATALOG,
    SOLHoloFrontierRecord,
    SOLHoloMasterManifest,
    SOLHoloOrganism,
    SOLHoloSynthesisReport,
    compute_holographic_merkle_root,
)

_V3_EXPORTS = frozenset({
    "V3BrainManifest",
    "V3BrainReflectiveOrchestrator",
    "V3BrainSynthesisReport",
})


def __getattr__(name):
    """Load workspace-dependent V3 APIs only when explicitly requested."""
    if name in _V3_EXPORTS:
        from importlib import import_module

        value = getattr(import_module(".v3_brain_manifest", __name__), name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "FRONTIER_CATALOG",
    "SOLHoloFrontierRecord",
    "SOLHoloMasterManifest",
    "SOLHoloOrganism",
    "SOLHoloSynthesisReport",
    "V3BrainManifest",
    "V3BrainReflectiveOrchestrator",
    "V3BrainSynthesisReport",
    "compute_holographic_merkle_root",
]

__version__ = "1.0.0"

