import json
from pathlib import Path

from projectmanager.config import PM_SPECIFICATION_FILE_NAME
from projectmanager.util import style
from projectmanager.validation.specification import validate_spec
from projectmanager.validation.template import validate_template


def specification_exists() -> bool:
    return Path(PM_SPECIFICATION_FILE_NAME).is_file()


def read_specification() -> dict:
    if not Path(PM_SPECIFICATION_FILE_NAME).is_file():
        raise Exception("Specification not found. Please initialize the specification first.")

    with open(PM_SPECIFICATION_FILE_NAME, encoding='utf-8') as file:
        spec_data = json.load(file)
    
    if not validate_spec(spec_data):
        raise Exception("Your specification is invalid. It is recommended to reinitialize the specification.")

    return spec_data


def write_specification(specification: dict):
    with open(PM_SPECIFICATION_FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(specification, file, indent=4)


def read_template(template_path: str) -> dict:
    try:
        with open(template_path, encoding='utf-8') as file:
            json_data = json.load(file)
    except Exception as e:
        err(f"Something went wrong when parsing the specification file: {e}")
        exit(1)

    if not validate_template(json_data):
        err("The template is invalid.")
        exit(1)

    return json_data


def err(message: str):
    print(style.red_text(f"ERROR: {message}"))


def warn(message: str):
    print(style.yellow_text(f"WARNING: {message}"))


def success(message: str):
    print(style.green_text(message))

