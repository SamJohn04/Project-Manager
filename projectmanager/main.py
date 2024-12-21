from projectmanager import config
from projectmanager.arg_parse import parse_args
from projectmanager.core import specification, scan
from projectmanager.core.generate import generate_objective_content
from projectmanager.feature.add_item import add_item
from projectmanager.feature.init import init
from projectmanager.feature.remove import remove
from projectmanager.feature.set_options import set_options
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
            remove(args)
        case "status" | "scan":
            scan_command(args.verbosity)
        case "generate":
            generate(args.objective, args.path_group, args.verbosity)
        case "set" | "unset":
            set_options(args)


# @FEAT generate REPURPOSE
def generate(objective_name: str | None, path_group: str | None, verbosity_level: int = config.V_NORMAL):
    spec_data = get_spec_data()

    for objective in spec_data.get("objectives", []):
        if objective_name is not None and objective["name"] != objective_name:
            continue
        generate_objective_content(spec_data, objective["name"], path_group)
        if verbosity_level != config.V_QUIET:
            io.success(f"Code of objective {objective['name']} has been generated successfully.")


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


def get_spec_data() -> dict:
    spec_data = io.read_specification()
    if spec_data is None:
        io.err("Specification not found. Please initialize the specification first.")
        exit(1)
    return spec_data


if __name__ == '__main__':
    main()

