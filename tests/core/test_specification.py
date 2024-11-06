import pytest

from projectmanager.core import specification


def test_init_spec():
    spec = specification.init_spec("TITLE")
    assert isinstance(spec, dict) and spec.get("title") == "TITLE"


def test_add_objective():
    spec = specification.init_spec("TITLE")

    specification.add_objective(spec, "first")
    specification.add_objective(spec, "second", "description of 2nd")

    assert spec["objectives"][0] == {"name": "first", "description": ""}
    assert spec["objectives"][1] == {"name": "second", "description": "description of 2nd"}

    with pytest.raises(ValueError):
        specification.add_objective(spec, "first", "description of first")

    assert len(spec["objectives"]) == 2


def test_add_path_group():
    spec = specification.init_spec("TITLE")

    specification.add_path_group(spec, "main", "src", ["py"])
    specification.add_path_group(spec, "tests", "tests", [])

    assert spec["pathGroups"][0] == {"name": "main", "dirPath": "src", "extensions": ["py"]}
    assert spec["pathGroups"][1] == {"name": "tests", "dirPath": "tests", "extensions": []}

    with pytest.raises(ValueError):
        specification.add_path_group(spec, "main", "main", [])

    assert len(spec["pathGroups"]) == 2


def test_objectives_to_str():
    spec = specification.init_spec("TITLE")

    specification.add_objective(spec, "first")
    specification.add_objective(spec, "second", "description of 2nd")

    assert specification.objectives_to_str(spec) == "first\nsecond: description of 2nd"
    assert specification.objectives_to_str(spec, sep='\t') == "first\tsecond: description of 2nd"


def test_path_groups_to_str():
    spec = specification.init_spec("TITLE")

    specification.add_path_group(spec, "main", "src", ["py"])
    specification.add_path_group(spec, "tests", "tests", [])

    assert specification.path_groups_to_str(spec) == "main: src [py]\ntests: tests []"
    assert specification.path_groups_to_str(spec, sep='\t') == "main: src [py]\ttests: tests []"


def test_remove_objective():
    spec = specification.init_spec("TITLE")

    specification.add_objective(spec, "first")
    specification.add_objective(spec, "second", "description of 2nd")

    with pytest.raises(KeyError):
        specification.remove_objective(spec, "third")

    assert specification.remove_objective(spec, "second") is None
    assert spec["objectives"][0] == {"name": "first", "description": ""} and len(spec["objectives"]) == 1

    with pytest.raises(KeyError):
        specification.remove_objective(spec, "second")


def test_remove_path_group():
    spec = specification.init_spec("TITLE")

    specification.add_path_group(spec, "main", "src", ["py"])
    specification.add_path_group(spec, "tests", "tests", [])

    with pytest.raises(KeyError):
        specification.remove_path_group(spec, "src")

    assert specification.remove_path_group(spec, "main") is None
    assert spec["pathGroups"][0] == {"name": "tests", "dirPath": "tests", "extensions": []} and len(spec["pathGroups"]) == 1

    with pytest.raises(KeyError):
        specification.remove_path_group(spec, "main")

