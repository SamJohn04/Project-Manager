from projectmanager.validation import specification


def test_validate_spec():
    assert not specification.validate_spec("spec")
    assert not specification.validate_spec(None)
    assert not specification.validate_spec({})

    assert not specification.validate_spec({"title": None})
    assert not specification.validate_spec({"title": 1})

    assert specification.validate_spec({"title": "project"})

    assert not specification.validate_spec({"title": "project", "objectives": "abc"})
    assert not specification.validate_spec({"title": "project", "objectives": [1]})
    assert not specification.validate_spec({"title": "project", "objectives": ["ab"]})
    assert not specification.validate_spec({"title": "project", "objectives": [{"name": "ab", "description": ""}, 1]})
    assert not specification.validate_spec({"title": "project", "objectives": [{"name": "ab", "description": ""}, {"name": "ab", "description": "a b c"}]})
    assert not specification.validate_spec({"title": "project", "objectives": [{"name": "ab", "description": None}]})

    assert specification.validate_spec({"title": "project", "objectives": [{"name": "ab", "description": ""}, {"name": "abc", "description": "a b c"}]})

    assert not specification.validate_spec({"title": "project", "pathGroups": "abc"})
    assert not specification.validate_spec({"title": "project", "pathGroups": [1]})
    assert not specification.validate_spec({"title": "project", "pathGroups": ["ab"]})
    assert not specification.validate_spec({"title": "project", "pathGroups": [{"name": "ab", "dirPath": "src", "extensions": []}, 1]})
    assert not specification.validate_spec({
        "title": "project",
        "pathGroups": [
            {"name": "ab", "dirPath": "src", "extensions": ["py"]},
            {"name": "ab", "dirPath": "main", "extensions": []}
            ]})

    assert specification.validate_spec({"title": "project", "pathGroups": [{"name": "main", "dirPath": "src", "extensions": ["py"]}]})

    assert not specification.validate_spec({"title": "project", "options": None})
    assert not specification.validate_spec({"title": "project", "options": "a"})
    assert not specification.validate_spec({"title": "project", "options": []})
    assert not specification.validate_spec({"title": "project", "options": {"todoFlag": 1}})

    assert specification.validate_spec({"title": "project", "options": {"todoFlag": "# TODO"}})

    assert specification.validate_spec({
        "title": "project",
        "objectives": [{"name": "ab", "description": ""}],
        "pathGroups": [{"name": "main", "dirPath": "src", "extensions": ["py", "json"]}],
        "options": {"todoFlag": "# TODO"}
        })


def test_validate_objective():
    assert not specification.validate_objective("objective")
    assert not specification.validate_objective(None)
    assert not specification.validate_objective({})

    assert not specification.validate_objective({"name": None})
    assert not specification.validate_objective({"name": 1})
    assert not specification.validate_objective({"name": "a"})
    assert not specification.validate_objective({"name": None, "description": "a"})
    assert not specification.validate_objective({"name": 1, "description": "a"})
    assert not specification.validate_objective({"name": "a", "description": None})
    assert not specification.validate_objective({"name": "a", "description": 1})
    assert not specification.validate_objective({"name": "a b", "description": "a"})

    assert specification.validate_objective({"name": "ab", "description": "a b c"})
    assert specification.validate_objective({"name": "ab", "description": ""})


def test_validate_path_group():
    assert not specification.validate_path_group("path group")
    assert not specification.validate_path_group(None)
    assert not specification.validate_path_group({})

    assert not specification.validate_path_group({"name": None})
    assert not specification.validate_path_group({"name": 1})
    assert not specification.validate_path_group({"name": "main"})
    assert not specification.validate_path_group({"name": None, "dirPath": "src", "extensions": ["py"]})
    assert not specification.validate_path_group({"name": 1, "dirPath": "src", "extensions": ["py"]})
    assert not specification.validate_path_group({"name": "main", "dirPath": "src"})
    assert not specification.validate_path_group({"name": "main", "dirPath": None, "extensions": []})
    assert not specification.validate_path_group({"name": "main", "dirPath": "src", "extensions": None})
    assert not specification.validate_path_group({"name": "main", "dirPath": "src", "extensions": "a"})
    assert not specification.validate_path_group({"name": "main", "dirPath": "src", "extensions": ["py", 1]})

    assert specification.validate_path_group({"name": "main", "dirPath": "src", "extensions": []})
    assert specification.validate_path_group({"name": "main", "dirPath": "src", "extensions": ["py"]})

