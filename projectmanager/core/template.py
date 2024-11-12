from pathlib import Path

from projectmanager.core import specification
from projectmanager.util import io


def create_from_template(project_title: str, template_data: dict):
    for item_to_create in template_data["toCreate"]:
        path_to_create = Path(item_to_create["path"])
        if item_to_create["type"] == "dir":
            path_to_create.mkdir(parents=True, exist_ok=True)
        elif item_to_create["type"] == "file":
            path_to_create.parent.mkdir(parents=True, exist_ok=True)
            with open(path_to_create, 'w') as file:
                file.write(item_to_create.get("content", ""))

    spec_data = specification.init_spec(project_title)
    if "pathGroups" in template_data:
        spec_data["pathGroups"] = template_data["pathGroups"]

    # TODO Handle spec already existing?
    io.write_specification(spec_data)

