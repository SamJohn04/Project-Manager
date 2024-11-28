from projectmanager.validation import template


def test_validate_template():
    assert not template.validate_template(None)
    assert not template.validate_template("template")
    assert not template.validate_template({})

    assert not template.validate_template({"name": None})
    assert not template.validate_template({"name": 1})
    assert not template.validate_template({"name": "templ"})

    assert not template.validate_template({"name": "templ", "toCreate": None})
    assert not template.validate_template({"name": "templ", "toCreate": 1})
    assert not template.validate_template({"name": "templ", "toCreate": "toCreate"})
    assert not template.validate_template({"name": "templ", "toCreate": ["toCreate"]})

    assert not template.validate_template({"name": "templ", "toCreate": [], "pathGroups": None})
    assert not template.validate_template({"name": "templ", "toCreate": [], "pathGroups": 1})
    assert not template.validate_template({"name": "templ", "toCreate": [], "pathGroups": "pathGroups"})
    assert not template.validate_template({"name": "templ", "toCreate": [], "pathGroups": ["pathGroups"]})

    assert template.validate_template({"name": "templ", "toCreate": []})
    assert template.validate_template({"name": "templ", "toCreate": [{"type": "file", "path": "a.py"}]})
    assert template.validate_template({"name": "templ", "toCreate": [{"type": "file", "path": "a.py"}], "pathGroups": []})
    assert template.validate_template({"name": "templ", "toCreate": [{"type": "file", "path": "a.py"}], "pathGroups": [{"name": "name", "dirPath": "src", "extensions": []}]})


def test_validate_to_create_item():
    assert not template.validate_to_create_item(None)
    assert not template.validate_to_create_item("toCreate")
    assert not template.validate_to_create_item({})
    assert not template.validate_to_create_item({"type": "file"})
    assert not template.validate_to_create_item({"type": "abc", "path": "a.py"})
    assert not template.validate_to_create_item({"type": 1, "path": "a.py"})
    assert not template.validate_to_create_item({"type": "file", "path": 1})

    assert template.validate_to_create_item({"type": "file", "path": "a.py"})

    assert not template.validate_to_create_item({"type": "file", "path": "a.py", "content": 1})
    assert template.validate_to_create_item({"type": "file", "path": "a.py", "content": "def todo():\n\tpass\n"})

    assert not template.validate_to_create_item({"type": "dir"})
    assert not template.validate_to_create_item({"type": "dir", "path": 1})
    assert not template.validate_to_create_item({"type": "dir", "path": "src", "content": ""})

    assert template.validate_to_create_item({"type": "dir", "path": "src"})

