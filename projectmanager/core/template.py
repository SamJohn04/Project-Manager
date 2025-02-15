from pathlib import Path

from projectmanager import config
from projectmanager.util import io
from projectmanager.core import generate, specification


def create_from_template(project_title: str, template_data: dict, verbosity_level: int = config.V_NORMAL) -> dict:
    for item_to_create in template_data["toCreate"]:
        path_to_create = Path(item_to_create["path"])
        if verbosity_level == config.V_VERBOSE:
            print("Creating", item_to_create["type"], path_to_create)
        if item_to_create["type"] == "dir":
            path_to_create.mkdir(parents=True, exist_ok=True)
        elif item_to_create["type"] == "file":
            content = item_to_create.get("content", "")
            create_file(project_title, path_to_create, content)

    if verbosity_level != config.V_QUIET:
        io.success("Files and Directories to be created have been generated.")

    spec_data = specification.init_spec(project_title)
    if "pathGroups" in template_data:
        spec_data["pathGroups"] = template_data["pathGroups"]

    if verbosity_level == config.V_NORMAL:
        print("Path Groups:", *(path_group["name"] for path_group in spec_data.get("pathGroups", [])))
    if verbosity_level == config.V_VERBOSE:
        print("Path Groups")
        for path_group in spec_data.get("pathGroups", []):
            print('|--', specification.path_group_to_str(path_group))
    
    return spec_data


def create_file(project_title: str, file_path_to_create: Path, content: str):
    content = generate.replace_placeholders_in_content(content, title=project_title)

    file_path_to_create.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path_to_create, 'w') as file:
        file.write(content)

