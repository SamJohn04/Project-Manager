from projectmanager import config
from projectmanager.arg_parse import parse_args
from projectmanager.core import specification, scan, template
from projectmanager.core.generate import generate_objective_content
from projectmanager.util import io, style


def main():
    args = parse_args()

    match args.command:
        case "init":
            init(args.title, args.template, args.force, args.verbosity)
        case "generate":
            generate(args.objective, args.path_group, args.verbosity)
        case "add":
            assert args.item in ("objective", "path")
            if args.item == "objective":
                add_objective(args.name, args.description, args.verbosity)
            else:
                add_path_group(args.name, args.dir, args.verbosity)
        case "view":
            if args.item is None or args.item == "all":
                view_all(args.verbosity)
            elif args.item == "objectives":
                view_objectives(args.verbosity)
            elif args.item == "paths":
                view_path_groups(args.verbosity)
            elif args.item == "objective":
                view_objective(args.name, args.verbosity)
            elif args.item == "path":
                view_path_group(args.name, args.verbosity)
        case "rm":
            remove(args.item, args.name, args.verbosity)
        case "status":
            scan_command(args.verbosity)
        case "set":
            set_command(args.name, args.value, args.verbosity)
        case "unset":
            set_command(args.name, None, args.verbosity)


# @FEAT init DONE
def init(title: str, template_path: str, force: bool, verbosity_level: int = config.V_NORMAL):
    if io.read_specification() is not None and not force:
        io.err("Specification already exists. Use -f | --force to reinitialize and overwrite anyway.")
        exit(1)

    if template_path is None:
        spec_data = specification.init_spec(title)
    else:
        template_data = io.read_template(template_path)
        spec_data = template.create_from_template(title, template_data, verbosity_level)

    io.write_specification(spec_data)

    if verbosity_level == config.V_NORMAL:
        io.success(f"Specification initialized")
    if verbosity_level == config.V_VERBOSE:
        print(style.bold(title), end=": ")
        io.success("Specification has been initialized successfully.")


# @FEAT generate REPURPOSE
def generate(objective_name: str | None, path_group: str | None, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    for objective in spec_data.get("objectives", []):
        if objective_name is not None and objective["name"] != objective_name:
            continue
        generate_objective_content(spec_data, objective["name"], path_group)
        if verbosity_level != config.V_QUIET:
            io.success(f"Code of objective {objective['name']} has been generated successfully.")


# @FEAT add_objective DONE
def add_objective(name: str, description: str | None, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()
    if description is None:
        description = ""
    try:
        specification.add_objective(spec_data, name, description)
    except ValueError as e:
        if verbosity_level == config.V_QUIET:
            io.err("add failed")
        else:
            io.err(f"Adding Objective failed: {e}")
        exit(1)

    io.write_specification(spec_data)

    if verbosity_level == config.V_NORMAL:
        io.success("Objective added")
    elif verbosity_level == config.V_VERBOSE:
        io.success(f"Objective {name} has been added successfully.")


# @FEAT add_path_group DONE
def add_path_group(name: str, dir_path: str, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()
    extensions = [extension.strip() for extension in input("Extensions (separated by \", \"): ").split(",")]

    if verbosity_level == config.V_VERBOSE:
        print("Extensions", *extensions, sep="\n\t")

    try:
        specification.add_path_group(spec_data, name, dir_path, extensions)
    except ValueError as e:
        if verbosity_level == config.V_QUIET:
            io.err("add failed")
        else:
            io.err(f"Adding Path Group failed: {e}")
        exit(1)

    io.write_specification(spec_data)

    if verbosity_level == config.V_NORMAL:
        io.success("Path group added")
    elif verbosity_level == config.V_VERBOSE:
        io.success(f"Path Group {name} has been added successfully.")


# @FEAT view_all DONE
def view_all(verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    print(style.blue_text(style.bold(spec_data["title"])))

    if verbosity_level == config.V_QUIET:
        print(style.blue_text("Objectives"), end=": ")
        print(', '.join(objective["name"] for objective in spec_data.get("objectives", [])))
        print(style.blue_text("Path Groups"), end=": ")
        print(', '.join(path_group["name"] for path_group in spec_data.get("pathGroups", [])))
    else:
        print(style.blue_text("Objectives"))
        for objective in spec_data.get("objectives", []):
            print('|--', specification.objective_to_str(objective))
        print()
        print(style.blue_text("Path Groups"))
        for path_group in spec_data.get("pathGroups", []):
            print('|--', specification.path_group_to_str(path_group))

    if verbosity_level == config.V_VERBOSE and "options" in spec_data:
        print()
        print(style.blue_text("Options"))
        for option_name in spec_data["options"]:
            print(f"|-- {option_name}: {spec_data['options'][option_name]}")


# @FEAT view_objectives DONE
def view_objectives(verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    if verbosity_level == config.V_QUIET:
        print(style.blue_text("Objectives"), end=": ")
        print(', '.join(objective["name"] for objective in spec_data.get("objectives", [])))
    elif verbosity_level == config.V_NORMAL:
        for objective in spec_data.get("objectives", []):
            print(specification.objective_to_str(objective))
    else:
        print(style.blue_text("Objectives"))
        for objective in spec_data.get("objectives", []):
            print('|--', specification.objective_to_str(objective))


# @FEAT view_path_groups DONE
def view_path_groups(verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    if verbosity_level == config.V_QUIET:
        print(style.blue_text("Path Groups"), end=": ")
        print(', '.join(path_group["name"] for path_group in spec_data.get("pathGroups", [])))
    elif verbosity_level == config.V_NORMAL:
        for path_group in spec_data.get("pathGroups", []):
            print(specification.path_group_to_str(path_group))
    else:
        print(style.blue_text("Path Groups"))
        for path_group in spec_data.get("pathGroups", []):
            print('|--', specification.path_group_to_str(path_group))


# @FEAT view_objective DONE
def view_objective(name: str, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()
    for objective in spec_data.get("objectives", []):
        if objective["name"] != name:
            continue
        if verbosity_level == config.V_QUIET:
            print(name)
        else:
            print(specification.objective_to_str(objective))
        break
    else:  # Executes if break was never called, i.e., name not found
        if verbosity_level != config.V_QUIET:
            io.warn("Objective not found.")


# @FEAT view_path_group DONE
def view_path_group(name: str, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()
    for path_group in spec_data.get("pathGroups", []):
        if path_group["name"] == name:
            continue
        if verbosity_level == config.V_QUIET:
            print(name)
        else:
            print(specification.path_group_to_str(path_group))
        break
    else:
        if verbosity_level != config.V_QUIET:
            io.warn("Path Group not found.")


# @FEAT remove DONE
def remove(item: str, name: str, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()
    try:
        if item == "objective":
            specification.remove_objective(spec_data, name)
        else:
            specification.remove_path_group(spec_data, name)
    except KeyError as e:
        if verbosity_level == config.V_QUIET:
            io.err("rm failed")
        else:
            io.err(f"Remove {item} failed: {e}")
        exit(1)

    io.write_specification(spec_data)

    if verbosity_level == config.V_NORMAL:
        io.success(f"Removed {item} {name}")
    elif verbosity_level == config.V_VERBOSE:
        io.success(f"{item} {name} has been removed successfully.")


# @FEAT scan DONE
def scan_command(verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    if len(spec_data.get("pathGroups", [])) == 0:
        if verbosity_level != config.V_QUIET:
            io.warn("No path groups found. Please add a path group to scan.")
        exit(1)

    for path_group in spec_data["pathGroups"]:
        print(style.bold(f"Path Group: {path_group['name']}"))
        print(f"Scanning {path_group['name']} for todos...")
        scan.scan_path_group_for_todos(path_group, spec_data.get("options", {}).get("todoFlag"), verbosity_level)
        print(f"\nScanning {path_group['name']} for objectives...")
        scan.scan_path_group_for_objectives(path_group, spec_data.get("objectives", []), spec_data.get("options", {}).get("objectiveFlag"), verbosity_level)
        print()


# @FEAT set_options DONE
def set_command(option_name: str, option_val: str | None, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()
    
    specification.set_option(spec_data, option_name, option_val)

    io.write_specification(spec_data)

    if verbosity_level == config.V_NORMAL:
        if option_val is None:
            io.success(f"{option_name} unset")
        else:
            io.success(f"{option_name} set")
    elif verbosity_level == config.V_VERBOSE:
        if option_val is None:
            io.success(f"{option_name} has been unset.")
        else:
            io.success(f"{option_name} has been set to {option_val}.")


def get_spec_data() -> dict:
    spec_data = io.read_specification()
    if spec_data is None:
        io.err("Specification not found. Please initialize the specification first.")
        exit(1)
    return spec_data


if __name__ == '__main__':
    main()

