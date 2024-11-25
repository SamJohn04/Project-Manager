from projectmanager import config
from projectmanager.config import DEFAULT_OBJECTIVE_FLAG, DEFAULT_TODO_FLAG
from projectmanager.util import io, paths, style


def scan_path_group_for_todos(path_group: dict, flag: str | None = None, verbosity_level: int = config.V_NORMAL):
    todo_found_in_group = False
    if flag is None:
        flag = DEFAULT_TODO_FLAG

    for path in paths.from_path_group(path_group):
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
        todo_indices = scan_todos_from_content(lines, flag)
        display_todos_by_content(path, lines, todo_indices, verbosity_level)
        if len(todo_indices) > 0:
            todo_found_in_group = True

    if not todo_found_in_group and verbosity_level != config.V_QUIET:
        io.success(f"No TODOs found in {path_group['name']}")


def scan_path_group_for_objectives(path_group: dict, objectives: list[dict], flag: str | None = None, verbosity_level: int = config.V_NORMAL):
    if flag is None:
        flag = DEFAULT_OBJECTIVE_FLAG

    objective_flags = {objective["name"]: [] for objective in objectives}
    statuses = {}

    for path in paths.from_path_group(path_group):
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
        scan_objectives_from_content(lines, flag, str(path), objective_flags, statuses)

    if verbosity_level == config.V_QUIET:
        total_statuses = sum(statuses.values())
        for status in statuses:
            print(f"{style.green_text(status)}: {statuses[status]}/{total_statuses}")
        return

    if verbosity_level == config.V_NORMAL:
        for objective in objective_flags:
            print(objective, end=": ")
            print(", ".join(status for status, *_ in objective_flags[objective]))
        print()
        total_statuses = sum(statuses.values())
        for status in statuses:
            print(f"{style.green_text(status)}: {statuses[status]}/{total_statuses}")
        return

    for objective in objective_flags:
        if len(objective_flags[objective]) == 0:
            print("No flag for", objective, "was found in", path_group["name"])
        if len(objective_flags[objective]) > 0:
            print(objective)
            for status, file_name, index in objective_flags[objective]:
                print(f"\t{status} ({file_name}: line {index + 1})")
    
    print()
    total_statuses = sum(statuses.values())
    for status in statuses:
        print(f"{style.green_text(status)}: {statuses[status]}/{total_statuses}")


def scan_todos_from_content(lines: list[str], flag: str):
    todo_indices = []

    for index, line in enumerate(lines):
        if flag in line:
            todo_indices.append(index)

    return todo_indices


def scan_objectives_from_content(lines: list[str], flag: str, file_name: str, objective_flags: dict, statuses: dict) -> dict[str, int]:
    for index, line in enumerate(lines):
        if flag not in line:
            continue
        line = line[line.index(flag) + len(flag):].strip()
        if len(line) == 0:
            io.warn(f"Unlabeled Objective Flag: {file_name} (line {index + 1})")
            continue

        parts = line.split()

        objective = parts[0]
        status = "unmarked" if len(parts) == 1 or len(parts[1]) == 0 else parts[1]

        if objective not in objective_flags:
            io.warn(f"Unrecognized Objective \"{objective}\" (status: {status}) in {file_name} (line {index + 1})")
        else:
            objective_flags[objective].append((status, file_name, index))
        
        if status not in statuses:
            statuses[status] = 0
        statuses[status] += 1

    return statuses


def display_todos_by_content(file_name, lines: list[str], todo_indices: list[int], verbosity_level: int = config.V_NORMAL):
    if len(todo_indices) == 0:
        return

    if verbosity_level == config.V_QUIET:
        print(file_name, end=": ")
        print(', '.join(str(todo_index) for todo_index in todo_indices))
        return

    if verbosity_level == config.V_NORMAL:
        print(file_name)
        for todo_index in todo_indices:
            print(style.bold(f"\t{todo_index + 1}. {lines[todo_index]}"))
        return

    print(file_name)
    for todo_index in todo_indices:
        if todo_index > 0:
            print(f"\t{todo_index}. {lines[todo_index-1]}")
        print(style.bold(f"\t{todo_index + 1}. {lines[todo_index]}"))
        if todo_index < len(lines) - 1:
            print(f"\t{todo_index + 2}. {lines[todo_index+1]}")

