from argparse import Namespace

from projectmanager import config
from projectmanager.util import io
from projectmanager.core import specification


# @FEAT remove REVIEW
def remove(args: Namespace):
    spec_data = io.read_specification()
    try:
        if args.item == "objective":
            specification.remove_objective(spec_data, args.name)
        else:
            specification.remove_path_group(spec_data, args.name)
    except KeyError as e:
        if args.verbosity == config.V_QUIET:
            io.err("rm failed")
        else:
            io.err(f"Removing {args.item} failed: {e}")
        return

    io.write_specification(spec_data)

    if args.verbosity == config.V_NORMAL:
        io.success(f"Removed {args.item} {args.name}")
    elif args.verbosity == config.V_VERBOSE:
        io.success(f"{args.item} {args.name} has been removed successfully.")

