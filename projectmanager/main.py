import json
import sys

from projectmanager.core import specification, scan, template
from projectmanager.util import io


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        display_info()
        return

    match args[0]:
        case "init":
            init(args[1:])
        case "generate":
            generate(args[1:])
        case "add":
            add(args[1:])
        case "view":
            view(args[1:])
        case "rm":
            remove(args[1:])
        case "scan":
            scan_command(args[1:])


def init(args: list[str]):
    if io.read_specification() is not None:
        choice = input("Specification already exists. Initialize and overwrite the file? (y|N): ")
        if choice not in ("y", "Y"):
            return
    title = input("Project title: ") if len(args) < 1 else args[0]
    io.write_specification(specification.init_spec(title))


def generate(args: list[str]):
    if io.read_specification() is not None:
        choice = input("Specification already exists. Initialize and overwrite the file? (y|N): ")
        if choice not in ("y", "Y"):
            return
    title = input("Project title: ") if len(args) < 1 else args[0]
    template_path = input("Template path: ") if len(args) < 2 else args[1]

    with open(template_path, encoding="utf-8") as file:
        template.create_from_template(title, json.load(file))


def add(args: list[str]):
    spec_data = io.read_specification()

    if spec_data is None:
        print("Specification not found. Please initialize the specification first.")
        exit(1)

    what_to_add = input("What would you like to add? (objective | path): ") if len(args) < 1 else args[0]

    if what_to_add == "objective":
        objective_name = input("Objective name: ") if len(args) < 2 else args[1]
        objective_description = input("Objective description: ") if len(args) < 3 else args[2]
        try:
            specification.add_objective(spec_data, objective_name, objective_description)
        except ValueError as e:
            print(f"Adding Objective failed... {e}")
            exit(1)
    elif what_to_add == "path":
        path_name = input("Path Group name: ") if len(args) < 2 else args[1]
        path_dir = input("Path Group directory path: ") if len(args) < 3 else args[2]
        extensions = input("Extensions (separated by \", \"): ").split(", ") if len(args) < 4 else args[3:]
        try:
            specification.add_path_group(spec_data, path_name, path_dir, extensions)
        except ValueError as e:
            print(f"Adding Path Group failed... {e}")
            exit(1)
    else:
        print("Invalid option; please enter \"objective\" or \"path\".")
        exit(1)

    io.write_specification(spec_data)


def view(args: list[str]):
    spec_data = io.read_specification()

    if spec_data is None:
        display_info()
        return

    if len(args) == 0:
        print(spec_data["title"])
        print("Objectives")
        for objective in spec_data.get("objectives", []):
            print('\t', specification.objective_to_str(objective))
        print("\nPath Groups")
        for path_group in spec_data.get("pathGroups", []):
            print('\t', specification.path_group_to_str(path_group))
    elif args[0] == "objectives":
        for objective in spec_data.get("objectives", []):
            print(specification.objective_to_str(objective))
    elif args[0] == "objective":
        name_to_search = input("Please enter objective name to view: ") if len(args) < 2 else args[1]
        objective_to_display = None
        for objective in spec_data.get("objectives", []):
            if objective["name"] == name_to_search:
                objective_to_display = objective
        if objective_to_display is None:
            print("Objective not found.")
        else:
            print(specification.objective_to_str(objective_to_display))
    elif args[0] == "paths":
        for path_group in spec_data.get("pathGroups", []):
            print(specification.path_group_to_str(path_group))
    elif args[0] == "path":
        name_to_search = input("Please enter path group name to view: ") if len(args) < 2 else args[1]
        path_group_to_display = None
        for path_group in spec_data.get("pathGroups", []):
            if path_group["name"] == name_to_search:
                path_group_to_display = path_group
        if path_group_to_display is None:
            print("Path Group not found.")
        else:
            print(specification.path_group_to_str(path_group_to_display))
    else:
        print("Invalid option. To view all objectives, use objectives; To view all paths use paths. To view an objective or a path, use 'objective' or 'path'")


def remove(args: list[str]):
    spec_data = io.read_specification()

    if spec_data is None:
        print("Specification not found. Please init the specification first.")
        exit(1)

    what_to_remove = input("What would you like to remove ? (objective | path): ") if len(args) < 1 else args[0]
    if what_to_remove not in ("objective", "path"):
        print("Invalid option.")
        exit(1)
    name_to_remove = input(f"{what_to_remove} name: ") if len(args) < 2 else args[1]
    if what_to_remove == "objective":
        specification.remove_objective(spec_data, name_to_remove)
    else:
        specification.remove_path_group(spec_data, name_to_remove)

    io.write_specification(spec_data)


def scan_command(args: list[str]):
    spec_data = io.read_specification()

    if spec_data is None:
        print("Specification not found. Please init the specification first.")
        exit(1)

    item_to_scan = None if len(args) < 1 else args[0]

    if len(spec_data.get("pathGroups", [])) == 0:
        print("No path groups found. Please add a path group to scan.")
        exit(1)

    for path_group in spec_data["pathGroups"]:
        if item_to_scan is None or item_to_scan == "todos":
            print(f"Scanning {path_group['name']} for todos...")
            found_instances = scan.scan_path_group_for_todos(path_group)
            for found_instance in found_instances:
                if len(found_instance[1]) == 0:
                    continue
                print(found_instance[0], *found_instance[1], sep="\n\t")
        if item_to_scan is None or item_to_scan == "objecitves":
            print(f"Scanning {path_group['name']} for objectives...")
            found_instances = scan.scan_path_group_for_objectives(path_group)
            for found_instance in found_instances:
                if len(found_instance[1]) == 0:
                    continue
                print(found_instance[0], *found_instance[1], sep="\n\t")


def display_info():
    print("Project Manager\nA concise project management tool\n")
    print("init\t\tInitialize a new project specification")
    print("generate\t\tGenerate a new project specification from a template")
    print("add\t\tAdd an objective or a path to the specification")
    print("view\t\tView specification data")
    print("rm\t\tRemove an objective or path by name")
    print("scan\t\tScan path groups for todos and objective flags")


if __name__ == '__main__':
    main()

