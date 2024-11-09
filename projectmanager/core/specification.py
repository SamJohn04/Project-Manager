def init_spec(project_title: str) -> dict:
    return {
        "title": project_title
    }


def add_objective(spec_data: dict, name: str, description: str = "") -> None:
    if ' ' in name:
        raise ValueError("Objective name should not have whitespace")

    if "objectives" not in spec_data:
        spec_data["objectives"] = []

    for objective in spec_data["objectives"]:
        if objective["name"] == name:
            raise ValueError("Objective name already exists.")

    spec_data["objectives"].append({"name": name, "description": description})


def add_path_group(spec_data: dict, name: str, dir_path: str, extensions: list[str]) -> None:
    if "pathGroups" not in spec_data:
        spec_data["pathGroups"] = []

    for path_group in spec_data["pathGroups"]:
        if path_group["name"] == name:
            raise ValueError("Path group name already exists.")

    spec_data["pathGroups"].append({"name": name, "dirPath": dir_path, "extensions": extensions})


def objective_to_str(objective: dict) -> str:
    return objective["name"] if objective["description"] == "" else f"{objective['name']}: {objective['description']}"


def path_group_to_str(path_group: dict) -> str:
    return f"{path_group['name']}: {path_group['dirPath']} [{','.join(path_group['extensions'])}]"


def remove_objective(spec_data: dict, name: str) -> None:
    key_index = None

    for index, objective in enumerate(spec_data.get("objectives", [])):
        if objective["name"] == name:
            key_index = index
            break

    if key_index is None:
        raise KeyError(f"{name} not in objectives.")

    spec_data["objectives"].pop(key_index)


def remove_path_group(spec_data: dict, name: str) -> None:
    key_index = None

    for index, path_group in enumerate(spec_data.get("pathGroups", [])):
        if path_group["name"] == name:
            key_index = index
            break

    if key_index is None:
        raise KeyError(f"{name} not in path groups.")

    spec_data["pathGroups"].pop(key_index)

