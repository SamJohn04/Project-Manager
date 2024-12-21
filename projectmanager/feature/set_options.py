from argparse import Namespace

from projectmanager import config
from projectmanager.core import specification
from projectmanager.util import io


# @FEAT set_options REVIEW
def set_options(args: Namespace):
    spec_data = io.read_specification()
    specification.set_option(spec_data, args.name, args.value if args.command == 'set' else None)
    io.write_specification(spec_data)

    if args.verbosity == config.V_NORMAL:
        io.success(f"{args.name} {args.command}")
    elif args.verbosity == config.V_VERBOSE:
        if args.command == 'set':
            io.success(f"{args.name} has been set to {args.value}.")
        else:
            io.success(f"{args.name} has been unset.")

