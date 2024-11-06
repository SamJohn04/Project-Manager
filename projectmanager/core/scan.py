from projectmanager.config import OBJECTIVE_FLAG


def scan_todos_from_content(content: str, flag: str = "TODO"):
    found_instances = []

    for index, line in enumerate(content.splitlines()):
        if flag in line:
            found_instances.append(index)

    return found_instances


def scan_objectives_from_content(content: str):
    found_objectives = []

    for index, line in enumerate(content.splitlines()):
        if OBJECTIVE_FLAG not in line:
            continue

        line = line[line.index(OBJECTIVE_FLAG) + len(OBJECTIVE_FLAG):].strip()
        if len(line) == 0:
            raise ValueError("The Objective flag should be followed by the name of the objective.")
        parts = line.split()

        if len(parts) == 1 or len(parts[1]) == 0:
            found_objectives.append((index, parts[0], None))
        else:
            found_objectives.append((index, parts[0], parts[1]))

    return found_objectives

