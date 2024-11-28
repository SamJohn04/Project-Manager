from projectmanager.validation import specification


def validate_template(template_data) -> bool:
    if not isinstance(template_data, dict):
        return False
    if not isinstance(template_data.get("name"), str):
        return False
    if not isinstance(template_data.get("pathGroups", []), list):
        return False
    if not isinstance(template_data.get("toCreate"), list):
        return False

    for path_group in template_data.get("pathGroups", []):
        if not specification.validate_path_group(path_group):
            return False

    for to_create_item in template_data["toCreate"]:
        if not validate_to_create_item(to_create_item):
            return False

    return True


def validate_to_create_item(to_create_item) -> bool:
    if not isinstance(to_create_item, dict):
        return False
    if not isinstance(to_create_item.get("path"), str):
        return False
    
    if to_create_item.get("type") not in ["file", "dir"]:
        return False

    if "content" in to_create_item and to_create_item["type"] != "file":
        return False

    if not isinstance(to_create_item.get("content", ""), str):
        return False

    return True

