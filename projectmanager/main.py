import json

from projectmanager.arg_parse import parse_args
from projectmanager.core import specification, scan, template
from projectmanager.util import io


def main():
    args = parse_args()

    match args.command:
        case "init":
            init(args.title, args.force)
        case "generate":
            generate(args.title, args.path, args.force)
        case "add":
            assert args.item in ("objective", "path")
            if args.item == "objective":
                add_objective(args.name, args.description)
            else:
                add_path_group(args.name, args.dir)
        case "view":
            if args.item is None or args.item == "all":
                view_all()
            elif args.item == "objectives":
                view_objectives()
            elif args.item == "paths":
                view_path_groups()
            elif args.item == "objective":
                view_objective(args.name)
            elif args.item == "path":
                view_path_group(args.name)
        case "rm":
            remove(args.item, args.name)
        case "scan":
            scan_command()
        case "set":
            set_command(args.name, args.value)
        case "unset":
            set_command(args.name, None)


# @FEAT init DONE
def init(title: str, force: bool):
    if io.read_specification() is not None and not force:
        choice = input("Specification already exists. Initialize and overwrite the file? (y|N): ")
        if choice not in ("y", "Y"):
            exit(0)

    io.write_specification(specification.init_spec(title))


# @FEAT generate ON-HOLD
def generate(title: str, path: str | None, force: bool):
    if io.read_specification() is not None and not force:
        choice = input("Specification already exists. Initialize and overwrite the file? (y|N): ")
        if choice not in ("y", "Y"):
            exit(0)

    if path is None:
        path = input("Template path: ")

    with open(path, encoding="utf-8") as file:
        template_data = json.load(file)

    io.write_specification(template.create_from_template(title, template_data))


# @FEAT add.objective DONE
def add_objective(name: str, description: str | None):
    spec_data = get_spec_data()
    if description is None:
        description = ""
    try:
        specification.add_objective(spec_data, name, description)
    except ValueError as e:
        io.err(f"Adding Objective failed... {e}")
        exit(1)

    io.write_specification(spec_data)


# @FEAT add.path_group DONE
def add_path_group(name: str, dir_path: str):
    spec_data = get_spec_data()
    extensions = [extension.strip() for extension in input("Extensions (separated by \", \"): ").split(",")]
    try:
        specification.add_path_group(spec_data, name, dir_path, extensions)
    except ValueError as e:
        io.err(f"Adding Path Group failed... {e}")
        exit(1)

    io.write_specification(spec_data)


# @FEAT view.all DONE
def view_all():
    spec_data = get_spec_data()
    print(spec_data["title"])
    print("Objectives")
    for objective in spec_data.get("objectives", []):
        print('\t', specification.objective_to_str(objective))
    print("\nPath Groups")
    for path_group in spec_data.get("pathGroups", []):
        print('\t', specification.path_group_to_str(path_group))


# @FEAT view.objectives DONE
def view_objectives():
    spec_data = get_spec_data()
    for objective in spec_data.get("objectives", []):
        print(specification.objective_to_str(objective))


# @FEAT view.path_groups DONE
def view_path_groups():
    spec_data = get_spec_data()
    for path_group in spec_data.get("pathGroups", []):
        print(specification.path_group_to_str(path_group))


# @FEAT view.objective DONE
def view_objective(name: str):
    spec_data = get_spec_data()
    for objective in spec_data.get("objectives", []):
        if objective["name"] == name:
            print(specification.objective_to_str(objective))
            break
    else:
        print("Objective not found.")


# @FEAT view.path_group DONE
def view_path_group(name: str):
    spec_data = get_spec_data()
    for path_group in spec_data.get("pathGroups", []):
        if path_group["name"] == name:
            print(specification.path_group_to_str(path_group))
            break
    else:
        print("Path Group not found.")


# @FEAT remove DONE
def remove(item: str, name: str):
    spec_data = get_spec_data()
    if item == "objective":
        specification.remove_objective(spec_data, name)
    else:
        specification.remove_path_group(spec_data, name)
    io.write_specification(spec_data)


# @FEAT scan ON-HOLD
def scan_command():
    spec_data = get_spec_data()

    if len(spec_data.get("pathGroups", [])) == 0:
        print("No path groups found. Please add a path group to scan.")
        exit(1)

    for path_group in spec_data["pathGroups"]:
        print(f"Path Group: {path_group['name']}")
        print(f"Scanning {path_group['name']} for todos...")
        scan.scan_path_group_for_todos(path_group, spec_data.get("options", {}).get("todoFlag"))
        print(f"\nScanning {path_group['name']} for objectives...")
        scan.scan_path_group_for_objectives(path_group, spec_data.get("objectives", []), spec_data.get("options", {}).get("objectiveFlag"))
        print()


# @FEAT set-options DONE
def set_command(option_name: str, option_val: str | None):
    spec_data = get_spec_data()
    
    specification.set_option(spec_data, option_name, option_val)

    io.write_specification(spec_data)


def get_spec_data() -> dict:
    spec_data = io.read_specification()
    if spec_data is None:
        print("Specification not found. Please init the specification first.")
        exit(1)
    return spec_data


if __name__ == '__main__':
    main()

