import argparse

from projectmanager import config


def parse_args():
    parser = argparse.ArgumentParser(description="A concise project management tool")
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='store_const', const=config.V_VERBOSE, dest="verbosity",
                                 help="Enable verbose mode (detailed output)")
    verbosity_group.add_argument('-q', '--quiet', action='store_const', const=config.V_QUIET, dest="verbosity",
                                 help="Enable quiet mode (minimal output)")
    verbosity_group.set_defaults(verbosity=config.V_NORMAL)

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_init_subparser(subparsers)
    add_generate_subparser(subparsers)
    add_add_subparser(subparsers)
    add_view_subparser(subparsers)
    add_remove_subparser(subparsers)
    add_scan_subparser(subparsers)
    add_set_subparser(subparsers)
    add_unset_subparser(subparsers)

    return parser.parse_args()


def add_init_subparser(subparsers):
    init_parser = subparsers.add_parser(
            "init",
            help="Initialize a new project specification",
            description="Initialize a new project specification from a source template or with only the project title"
            )
    init_parser.add_argument("title", help="Project title")
    init_parser.add_argument("--template", help="Path to the source template")
    init_parser.add_argument("-f", "--force", action="store_true", help="Initialze specification by force, overwriting the file if it exists.")


def add_generate_subparser(subparsers):
    generate_parser = subparsers.add_parser(
            "generate",
            help="Generate code for objectives from objectivesFormat in project specification. Does not check if the specification is already defined.",
            description="Generate code for objectives from objectivesFormat in project specification."
            )
    generate_parser.add_argument("name", help="Name of objective")
    generate_parser.add_argument("--path-group", help="Path group name to generate the objective code for.", dest="path_group")
    # generate_parser.add_argument("-f", "--force", action="store_true", help="Initialze specification by force, overwriting the file if it exists.")


def add_add_subparser(subparsers):
    add_parser = subparsers.add_parser(
            "add",
            help="Add an objective or a path group to the specification",
            description="Add a new objective or path group to the project specification."
            )
    add_subparsers = add_parser.add_subparsers(dest="item")

    add_objective_parser = add_subparsers.add_parser(
            "objective",
            help="Add an objective to the specification",
            description="Add a new objective to the project specification."
            )
    add_objective_parser.add_argument("name", help="Name of the objective")
    add_objective_parser.add_argument("-d", "--description", help="Description of the objective")

    add_path_group_parser = add_subparsers.add_parser(
            "path",
            help="Add a path group to the specification",
            description="Add a new path group to the project specification"
            )
    add_path_group_parser.add_argument("name", help="Name of the path group")
    add_path_group_parser.add_argument("dir", help="Directory path of the path group")


def add_view_subparser(subparsers):
    view_parser = subparsers.add_parser(
            "view",
            help="View specification data",
            description="View project specification data."
            )
    view_subparsers = view_parser.add_subparsers(dest="item", required=False)

    view_subparsers.add_parser(
            "all",
            help="View all specification data",
            description="View all information in the project specification."
            )
    view_subparsers.add_parser(
            "objectives",
            help="View all objectives of the specification data",
            description="View all objectives in the project specification."
            )
    view_subparsers.add_parser(
            "paths",
            help="View all path groups of the specification data",
            description="View all path groups in the project specification."
            )

    view_subparsers.add_parser(
            "objective",
            help="View an objective by name",
            description="View an objective in the project specification by name."
            ).add_argument("name", help="Name of the objective to view")
    view_subparsers.add_parser(
            "path",
            help="View a path group by name",
            description="View a path group in the project specification by name."
            ).add_argument("name", help="Name of the path group to view")


def add_remove_subparser(subparsers):
    rm_parser = subparsers.add_parser(
            "rm",
            help="Remove an objective or a path group from the specification",
            description="Remove an objective or path group from the project specification by name."
            )
    rm_parser.add_argument("item", choices=["objective", "path"], help="Type of the item to be removed from the specification")
    rm_parser.add_argument("name", help="Name of the item to be removed")


def add_scan_subparser(subparsers):
    subparsers.add_parser(
            "scan",
            help="Scan path groups for todos and objective flags",
            description="Scan the files in the path groups for todos and objectives (by flag). Custom flags can be set using the set command."
            )


def add_set_subparser(subparsers):
    set_parser = subparsers.add_parser(
            "set",
            help="Set options to the specification",
            description="Set options (such as flags) to the specification. Can be removed using unset."
            )
    set_parser.add_argument("name", choices=["todoFlag", "objectiveFlag"], help="The option name (key) to be set.")
    set_parser.add_argument("value", help="The option value to be assigned.")


def add_unset_subparser(subparsers):
    set_parser = subparsers.add_parser(
            "unset",
            help="Unset options from the specification",
            description="Unset options (such as flags) from the specification."
            )
    set_parser.add_argument("name", choices=["todoFlag", "objectiveFlag"], help="The option name (key) to be unset.")

