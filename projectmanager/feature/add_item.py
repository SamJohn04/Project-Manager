from argparse import Namespace

from projectmanager import config
from projectmanager.util import io
from projectmanager.core import specification


# @FEAT add_item REVIEW
def add_item(args: Namespace):
    spec_data = io.read_specification()
    assert args.item in ("objective", "path")

    try:
        if args.item == "objective":
            specification.add_objective(spec_data, args.name, args.description)
        else:
            extensions = [extension.strip() for extension in input("Extensions (separated by \", \"): ").split(",")]
            specification.add_path_group(spec_data, args.name, args.dir, extensions)
    except Exception as e:
        if args.verbosity == config.V_QUIET:
            io.err("add failed")
        else:
            io.err(f"Adding {args.item} failed: {e}")
        return

    io.write_specification(spec_data)

    if args.verbosity == config.V_NORMAL:
        io.success(f"Addition of {args.item} successful.")
    elif args.verbosity == config.V_VERBOSE:
        io.success(f"{args.item} {args.name} has been added successfully.")

