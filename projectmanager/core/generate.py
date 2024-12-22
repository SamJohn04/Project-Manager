import pathlib
from projectmanager import config


def generate_objective_content(spec_data: dict, objective_name: str, path_group_to_generate_in: str | None = None):
    for objective_format_item in spec_data["objectivesFormat"]:
        if path_group_to_generate_in is not None and objective_format_item["pathGroup"] != path_group_to_generate_in:
            continue
        content = replace_placeholders_in_content(
                objective_format_item["content"],
                title=spec_data["title"],
                objective_name=objective_name
                )
        file_path = replace_placeholders_in_content(
                objective_format_item["path"],
                title=spec_data["title"],
                objective_name=objective_name
                )
        file_path = pathlib.Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'a' if objective_format_item.get("append") else 'w') as file:
            file.write(content)


def replace_placeholders_in_content(content: str, **kwargs):
    for placeholder in config.PLACEHOLDERS:
        if placeholder in kwargs:
            content = content.replace(config.PLACEHOLDERS[placeholder], kwargs[placeholder])
    return content

