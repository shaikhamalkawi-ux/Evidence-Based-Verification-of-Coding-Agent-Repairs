"""P12 visibly available, predeclared tests for the PDM include-group update regression.

These are NOT held-out task tests and NOT the original SWE-bench-Live test patch.
Run with PDM's original pytest fixtures using:
  cp pilot/pdm/visible_local_tests.py "$UPSTREAM/tests/cli/test_p12_visible.py"
  cd "$UPSTREAM"; python -m pytest tests/cli/test_p12_visible.py -q
"""
import pytest
from pdm.formats.base import make_array


def _groups(project):
    """Read the actual TOML lock package group metadata, not only project declarations."""
    project.lockfile.reload()
    return {item["name"]: set(item.get("groups", []))
            for item in project.lockfile._data["package"]}


def _setup_group_project(project, repository, pdm):
    # All names are present in the test suite's fake repository (no live index).
    project.pyproject.dependency_groups.update({
        "shared": ["pytz"],
        "lint": make_array([{"include-group": "shared"}, "chardet"]),
        "independent": ["urllib3"],
    })
    project.pyproject.write()
    pdm(["lock"], obj=project, strict=True)
    groups = _groups(project)
    assert {"shared", "lint"} <= groups["pytz"]
    assert "lint" in groups["chardet"]
    assert "independent" in groups["urllib3"]
    assert "lint" not in groups["urllib3"]
    return groups


def test_partial_update_preserves_included_dependency_groups(project, repository, pdm):
    before = _setup_group_project(project, repository, pdm)
    # "chardet" is directly in lint; "pytz" is included via shared.
    # The observed bug in the original task removes lint from pytz on update.
    pdm(["update", "chardet", "-G", "lint", "--no-sync"], obj=project, strict=True)
    after = _groups(project)
    assert "lint" in after["pytz"], (before, after)
    assert "shared" in after["pytz"], (before, after)
    assert "lint" in after["chardet"], (before, after)
    assert "independent" in after["urllib3"], (before, after)
    assert "lint" not in after["urllib3"], (before, after)


def test_pinned_update_must_not_erase_included_group_metadata(project, repository, pdm):
    before = _setup_group_project(project, repository, pdm)
    # Updating without a changed resolved version should not erase metadata.
    pdm(["update", "chardet", "-G", "lint", "--no-sync"], obj=project, strict=True)
    after = _groups(project)
    assert before["pytz"] == after["pytz"], (before, after)
    assert before["chardet"] == after["chardet"], (before, after)
    assert before["urllib3"] == after["urllib3"], (before, after)


def test_nested_include_preserves_provenance(project, repository, pdm):
    project.pyproject.dependency_groups.update({
        "shared": ["pytz"],
        "lint": make_array([{"include-group": "shared"}, "chardet"]),
        "outer": make_array([{"include-group": "lint"}]),
    })
    project.pyproject.write()
    pdm(["lock"], obj=project, strict=True)
    before = _groups(project)
    assert {"shared", "lint", "outer"} <= before["pytz"]
    pdm(["update", "chardet", "-G", "lint", "--no-sync"], obj=project, strict=True)
    after = _groups(project)
    assert {"shared", "lint", "outer"} <= after["pytz"], (before, after)
    assert {"lint", "outer"} <= after["chardet"], (before, after)
