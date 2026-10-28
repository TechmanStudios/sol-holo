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
from .v3_brain_manifest import (
    V3BrainManifest,
    V3BrainReflectiveOrchestrator,
    V3BrainSynthesisReport,
)

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

