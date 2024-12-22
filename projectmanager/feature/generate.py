from argparse import Namespace

from projectmanager import config
from projectmanager.util import io
from projectmanager.core.generate import generate_objective_content


# @FEAT generate REVIEW
def generate(args: Namespace):
    spec_data = io.read_specification()

    if "objectivesFormat" not in spec_data:
        io.err("Format for objectives has not been added to the specification configuration.")
        return

    if args.objective is None and input("Generate code for all objectives? (y|N)") not in ("y", "Y"):
        return
    if args.path_group is None and input("Generate code for all path groups? (y|N)") not in ("y", "Y"):
        return

    for objective in spec_data.get("objectives", []):
        if args.objective is not None and objective["name"] != args.objective:
            continue
        generate_objective_content(spec_data, objective["name"], args.path_group)
        if args.verbosity != config.V_QUIET:
            io.success(f"Code of objective {objective['name']} has been generated successfully.")

