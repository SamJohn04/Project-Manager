import json
from pathlib import Path

from projectmanager import config
from projectmanager.util import style
from projectmanager.validation.specification import validate_spec
from projectmanager.validation.template import validate_template


def specification_exists() -> bool:
    return Path(config.PM_SPECIFICATION_FILE_NAME).is_file()


def read_specification() -> dict:
    if not Path(config.PM_SPECIFICATION_FILE_NAME).is_file():
        raise Exception("Specification not found. Please initialize the specification first.")

    with open(config.PM_SPECIFICATION_FILE_NAME, encoding='utf-8') as file:
        spec_data = json.load(file)
    
    if not validate_spec(spec_data):
        raise Exception("Your specification is invalid. It is recommended to reinitialize the specification.")

    return spec_data


def write_specification(specification: dict):
    with open(config.PM_SPECIFICATION_FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(specification, file, indent=4)


def read_template(template_path: str) -> dict:
    with open(template_path, encoding='utf-8') as file:
        template_data = json.load(file)

    if not validate_template(template_data):
        raise Exception("The template is invalid.")

    return template_data


def write_content(content: str, path: Path, to_append: bool = False, **kwargs: str):
    for placeholder in config.PLACEHOLDERS:
        if placeholder in kwargs:
            content = content.replace(config.PLACEHOLDERS[placeholder], kwargs[placeholder])

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a' if to_append else 'w', encoding='utf-8') as file:
        file.write(content)


def err(message: str):
    print(style.red_text(f"ERROR: {message}"))


def warn(message: str):
    print(style.yellow_text(f"WARNING: {message}"))


def success(message: str):
    print(style.green_text(message))

