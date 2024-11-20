def validate_spec(spec_data) -> bool:
    if not isinstance(spec_data, dict):
        return False
    if not isinstance(spec_data.get("title"), str):
        return False
    if not isinstance(spec_data.get("objectives", []), list):
        return False
    if not isinstance(spec_data.get("pathGroups", []), list):
        return False

    names = set()
    for objective in spec_data.get("objectives", []):
        if not validate_objective(objective):
            return False
        if objective["name"] in names:
            return False
        names.add(objective["name"])

    names = set()
    for path_group in spec_data.get("pathGroups", []):
        if not validate_path_group(path_group):
            return False
        if path_group["name"] in names:
            return False
        names.add(path_group["name"])

    if not isinstance(spec_data.get("options", {}), dict):
        return False
    for key, value in spec_data.get("options", {}).items():
        if not isinstance(key, str) or not isinstance(value, str):
            return False
    
    return True


def validate_objective(objective) -> bool:
    if not isinstance(objective, dict):
        return False
    if not isinstance(objective.get("name"), str):
        return False
    if not isinstance(objective.get("description"), str):
        return False

    if ' ' in objective["name"]:
        return False

    return True


def validate_path_group(path_group) -> bool:
    if not isinstance(path_group, dict):
        return False
    if not isinstance(path_group.get("name"), str):
        return False
    if not isinstance(path_group.get("dirPath"), str):
        return False

    if not isinstance(path_group.get("extensions"), list):
        return False

    for extension in path_group["extensions"]:
        if not isinstance(extension, str):
            return False

    return True

