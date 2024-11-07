import json

from projectmanager.config import PM_SPECIFICATION_FILE_NAME


def read_specification() -> dict:
    with open(PM_SPECIFICATION_FILE_NAME, encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def write_specification(specification: dict):
    with open(PM_SPECIFICATION_FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(specification, file)

