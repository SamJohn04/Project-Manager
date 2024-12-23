from argparse import Namespace

from projectmanager import config
from projectmanager.core import scan
from projectmanager.util import io, style


# @FEAT status REVIEW
def status(args: Namespace):
    spec_data = io.read_specification()
    if len(spec_data.get("pathGroups", [])) == 0:
        if args.verbosity != config.V_QUIET:
            io.warn("No path groups found. Please add a path group to scan.")
        return

    todo_flag = spec_data.get("options", {}).get("todoFlag", config.DEFAULT_TODO_FLAG)
    objective_flag = spec_data.get("options", {}).get("objectiveFlag", config.DEFAULT_OBJECTIVE_FLAG)

    objective_names = {objective["name"] for objective in spec_data.get("objectives", [])}

    for path_group in spec_data["pathGroups"]:
        print(style.bold(f"Path Group {path_group['name']}: TODOs"))
        todo_instances = scan.scan_path_group(path_group, todo_flag)
        display_todo_instances(todo_instances, args.verbosity)
        print()

        print(style.bold(f"Path Group {path_group['name']}: Objectives"))
        objective_instances = scan.scan_path_group(path_group, objective_flag)
        display_objective_instances(objective_instances, objective_names, objective_flag, args.verbosity)
        print()


def display_todo_instances(scan_instances: list[scan.ScanInstance], verbosity_level: int = config.V_NORMAL):
    if len(scan_instances) == 0:
        print("No TODOs found!")
        return

    todo_instances_by_path = {}

    for scan_instance in scan_instances:
        if scan_instance.path not in todo_instances_by_path:
            todo_instances_by_path[scan_instance.path] = []
        todo_instances_by_path[scan_instance.path].append(scan_instance)

    for path in todo_instances_by_path:
        if verbosity_level == config.V_QUIET:
            print(f"{path}:", ', '.join(todo_instance.index for todo_instance in todo_instances_by_path[path]))
            continue
        print(path)
        if verbosity_level == config.V_NORMAL:
            for todo_instance in todo_instances_by_path[path]:
                print(f"\t{todo_instance.index + 1}. {todo_instance.line}")
            continue
        for todo_instance in todo_instances_by_path[path]:
            if todo_instance.index > 0:
                print(f"\t{todo_instance.index}. {todo_instance.all_lines[todo_instance.index - 1]}")
            print(style.bold(f"\t{todo_instance.index + 1}. {todo_instance.line}"))
            if todo_instance.index < len(todo_instance.all_lines) - 1:
                print(f"\t{todo_instance.index + 2}. {todo_instance.all_lines[todo_instance.index + 1]}")


def display_objective_instances(scan_instances: list[scan.ScanInstance], objective_names: set[str], objective_flag: str, verbosity_level: int = config.V_NORMAL):
    found_objectives = {objective_name: [] for objective_name in objective_names}
    statuses = {}

    for scan_instance in scan_instances:
        line_items = scan_instance.line[scan_instance.line.index(objective_flag) + len(objective_flag):].strip().split()

        if len(line_items) == 0:
            io.warn(f"Unlabeled Objective Flag: {scan_instance.path} (line {scan_instance.index + 1})")
            continue

        objective = line_items[0]
        status = line_items[1] if len(line_items) > 1 else "Unmarked"

        if objective in objective_names:
            found_objectives[objective].append((status, scan_instance.path, scan_instance.index))
        else:
            io.warn(f"Unrecognized Objective \"{objective}\" (status: {status}) in {scan_instance.path} (line {scan_instance.index + 1})")

        if status not in statuses:
            statuses[status] = 0
        statuses[status] += 1

    if verbosity_level == config.V_NORMAL:
        for objective in found_objectives:
            print(f"{objective}:", ", ".join(status for status, *_ in found_objectives[objective]))
        print()
    elif verbosity_level == config.V_VERBOSE:
        for objective in found_objectives:
            if len(found_objectives[objective]) == 0:
                print(f"No flag for {objective} was found.")
                continue
            print(objective)
            for status, file_name, index in found_objectives[objective]:
                print(f"\t{status} ({file_name}: line {index + 1})")
        print()

    total_statuses = sum(statuses.values())
    for status in statuses:
        print(f"{style.green_text(status)}: {statuses[status]}/{total_statuses}")

