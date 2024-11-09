import sys

from projectmanager.core import specification
from projectmanager.util import io


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        display_info()
        exit(0)

    match args[0]:
        case "init":
            init(args[1:])
        case "add":
            add(args[1:])
        case "view":
            view(args[1:])
        case "rm":
            remove(args[1:])


def display_info():
    # TODO
    pass


def init(args: list[str]):
    title = input("Project title: ") if len(args) == 0 else ' '.join(args)

    new_spec_data = specification.init_spec(title)
    io.write_specification(new_spec_data)


def add(args: list[str]):
    spec_data = io.read_specification()

    what_to_add = input("What would you like to add? (objective | path): ") if len(args) == 0 else args[0]

    if what_to_add == "objective":
        objective_name = input("Objective name: ") if len(args) < 2 else args[1]
        objective_description = input("Objective description: ") if len(args) < 3 else ' '.join(args[2:])
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
        name_to_search = input("Please enter objective name to view: ") if len(args) == 1 else args[1]
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
        name_to_search = input("Please enter path group name to view: ") if len(args) == 1 else args[1]
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
    # TODO
    pass


if __name__ == '__main__':
    main()

