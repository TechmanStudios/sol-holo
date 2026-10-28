"""Core commands remain usable without the optional SOL Systems workspace."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


_ISOLATED_CLI = """
import importlib.abc
import sys

class NoWorkspace(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'sol_continuum', 'sol_decide', 'sol_edge', 'observatory'}:
            raise ModuleNotFoundError('workspace dependency unavailable', name=fullname)

sys.meta_path.insert(0, NoWorkspace())
from sol_holo import SOLHoloOrganism
from sol_holo.cli import main
assert 'sol_holo.v3_brain_manifest' not in sys.modules
raise SystemExit(main(sys.argv[1:]))
"""


@pytest.fixture
def standalone_checkout(tmp_path: Path) -> Path:
    source = Path(__file__).resolve().parents[1]
    checkout = tmp_path / "sol-holo"
    for directory in ("sol_holo", "packets"):
        shutil.copytree(source / directory, checkout / directory)
    return checkout


def _run_cli(checkout: Path, command: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(checkout)}
    return subprocess.run(
        [sys.executable, "-c", _ISOLATED_CLI, command],
        cwd=checkout,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.parametrize("command", ["manifest", "synthesize"])
def test_core_cli_without_workspace(standalone_checkout: Path, command: str) -> None:
    result = _run_cli(standalone_checkout, command)
    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    manifest = document if command == "manifest" else document["manifest"]
    assert manifest["total_frontiers"] == 26
    assert manifest["all_frontiers_verified"] is True


def test_v3_cli_explains_missing_workspace(standalone_checkout: Path) -> None:
    result = _run_cli(standalone_checkout, "v3-brain")
    assert result.returncode == 2
    assert "requires the sol-systems workspace dependencies" in result.stderr
    assert "Traceback" not in result.stderr
