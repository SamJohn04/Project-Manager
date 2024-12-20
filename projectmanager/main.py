from projectmanager import config
from projectmanager.arg_parse import parse_args
from projectmanager.core import specification, scan
from projectmanager.core.generate import generate_objective_content
from projectmanager.feature.add_item import add_item
from projectmanager.feature.init import init
from projectmanager.feature.view import view
from projectmanager.util import io, style


def main():
    args = parse_args()

    match args.command:
        case "init":
            init(args)
        case "add":
            add_item(args)
        case "view":
            view(args)
        case "rm":
            remove(args.item, args.name, args.verbosity)
        case "status" | "scan":
            scan_command(args.verbosity)
        case "generate":
            generate(args.objective, args.path_group, args.verbosity)
        case "set":
            set_command(args.name, args.value, args.verbosity)
        case "unset":
            set_command(args.name, None, args.verbosity)


# @FEAT generate REPURPOSE
def generate(objective_name: str | None, path_group: str | None, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    for objective in spec_data.get("objectives", []):
        if objective_name is not None and objective["name"] != objective_name:
            continue
        generate_objective_content(spec_data, objective["name"], path_group)
        if verbosity_level != config.V_QUIET:
            io.success(f"Code of objective {objective['name']} has been generated successfully.")


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

