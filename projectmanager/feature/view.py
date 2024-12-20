from argparse import Namespace

from projectmanager import config
from projectmanager.core import specification
from projectmanager.util import io, style


# @FEAT view REVIEW
def view(args: Namespace):
    spec_data = io.read_specification()

    if args.item is None or args.item == "all":
        print(style.bold(spec_data["title"]))

    if args.item != "paths":
        view_objectives(spec_data, args.verbosity)
        print()

    if args.item != "objectives":
        view_path_groups(spec_data, args.verbosity)
        print()

    if args.verbosity == config.V_VERBOSE and "options" in spec_data:
        print(style.blue_text("Options"))
        for option_name in spec_data["options"]:
            print(f"|-- {option_name}: {spec_data['options'][option_name]}")



def view_objectives(spec_data: dict, verbosity: int):
    if verbosity == config.V_QUIET:
        print(
                style.blue_text("Objectives:"),
                ', '.join(objective["name"] for objective in spec_data.get("objectives", [])),
                end=""
                )
        return
    print(style.blue_text("Objectives"))
    for objective in spec_data.get("objectives", []):
        print('|--', specification.objective_to_str(objective))


def view_path_groups(spec_data: dict, verbosity: int):
    if verbosity == config.V_QUIET:
        print(
                style.blue_text("Path Groups:"),
                ', '.join(path_group["name"] for path_group in spec_data.get("pathGroups", [])),
                end=""
                )
        return
    print(style.blue_text("Path Groups"))
    for path_group in spec_data.get("pathGroups", []):
        print('|--', specification.path_group_to_str(path_group))

