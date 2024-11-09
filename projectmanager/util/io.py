import json
from pathlib import Path

from projectmanager.config import PM_SPECIFICATION_FILE_NAME


def read_specification() -> dict:
    if not Path(PM_SPECIFICATION_FILE_NAME).is_file():
        print("Specification has not yet been initialized. Please initialize the specification file with init.")
        exit(1)

    with open(PM_SPECIFICATION_FILE_NAME, encoding='utf-8') as file:
        json_data = json.load(file)

    return json_data


def write_specification(specification: dict):
    with open(PM_SPECIFICATION_FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(specification, file)

