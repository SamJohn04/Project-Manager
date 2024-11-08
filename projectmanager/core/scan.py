from typing import Callable
from projectmanager.util import paths


def scan_path_group_for_todos(path_group: dict, flag: str = "TODO"):
    return scan_path_group(path_group, lambda content: scan_todos_from_content(content, flag))


def scan_path_group_for_objectives(path_group: dict, flag: str = "@OBJECTIVE"):
    return scan_path_group(path_group, lambda content: scan_objectives_from_content(content, flag))


def scan_path_group(path_group: dict, scan_method: Callable):
    """
    Execute scan_method for contents of each path from the path group
    returns: list of each path and corresponding result as a tuple
    """
    found_instances: list = []

    for path in paths.from_path_group(path_group):
        with open(path, encoding="utf-8") as file:
            found_instances.append((path, scan_method(file.read())))

    return found_instances


def scan_todos_from_content(content: str, flag: str = "TODO"):
    found_instances = []

    for index, line in enumerate(content.splitlines()):
        if flag in line:
            found_instances.append(index)

    return found_instances


def scan_objectives_from_content(content: str, flag: str = "@OBJECTIVE"):
    found_objectives = []

    for index, line in enumerate(content.splitlines()):
        if flag not in line:
            continue

        line = line[line.index(flag) + len(flag):].strip()
        if len(line) == 0:
            raise ValueError("The Objective flag should be followed by the name of the objective.")
        parts = line.split()

        if len(parts) == 1 or len(parts[1]) == 0:
            found_objectives.append((index, parts[0], None))
        else:
            found_objectives.append((index, parts[0], parts[1]))

    return found_objectives

