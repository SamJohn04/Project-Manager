from projectmanager.config import DEFAULT_OBJECTIVE_FLAG, DEFAULT_TODO_FLAG
from projectmanager.util import paths


def scan_path_group_for_todos(path_group: dict, flag: str | None = None):
    if flag is None:
        flag = DEFAULT_TODO_FLAG

    for path in paths.from_path_group(path_group):
        with open(path, encoding="utf-8") as file:
            scan_todos_from_content(file.read().splitlines(), flag, str(path))


def scan_path_group_for_objectives(path_group: dict, objectives: list[dict], flag: str | None = None):
    if flag is None:
        flag = DEFAULT_OBJECTIVE_FLAG

    objective_flags = {objective["name"]: [] for objective in objectives}

    for path in paths.from_path_group(path_group):
        with open(path, encoding="utf-8") as file:
            scan_objectives_from_content(file.read().splitlines(), flag, str(path), objective_flags)

    for objective_name in objective_flags:
        if len(objective_flags[objective_name]) == 0:
            print("no flag for", objective_name, "was found in", path_group["name"])
        else:
            print(objective_name, *objective_flags[objective_name], sep="\n\t")


def scan_todos_from_content(lines: list[str], flag: str, file_name: str):
    for index, line in enumerate(lines):
        if flag not in line:
            continue
        print(file_name)
        if index > 0:
            print(f"\t{index}. {lines[index-1]}")
        print(f"\t{index + 1}. {line}")
        if index < len(lines) - 1:
            print(f"\t{index + 2}. {lines[index+1]}")


def scan_objectives_from_content(lines: list[str], flag: str, file_name: str, objective_flags: dict):
    for index, line in enumerate(lines):
        if flag not in line:
            continue
        line = line[line.index(flag) + len(flag):].strip()
        if len(line) == 0:
            print(f"Unlabeled Objective Flag: {file_name} ({index + 1})")
            continue
        parts = line.split()

        if parts[0] not in objective_flags:
            print(f"Unrecognized Objective {parts[0]} in {file_name} ({index + 1})")
        else:
            status = "unmarked" if len(parts) == 1 or len(parts[1]) == 0 else parts[1]
            objective_flags[parts[0]].append(f"{status} ({file_name} {index + 1})")

