from argparse import Namespace

from projectmanager import config
from projectmanager.core import scan
from projectmanager.util import io, style


# @FEAT status ON-HOLD refactor core.scan necessary;
def status(args: Namespace):
    spec_data = io.read_specification()
    if len(spec_data.get("pathGroups", [])) == 0:
        if args.verbosity != config.V_QUIET:
            io.warn("No path groups found. Please add a path group to scan.")
        return

    for path_group in spec_data["pathGroups"]:
        print(style.bold(f"Path Group: {path_group['name']}"))
        print(f"Scanning {path_group['name']} for todos...")
        scan.scan_path_group_for_todos(path_group, spec_data.get("options", {}).get("todoFlag"), args.verbosity)
        print(f"\nScanning {path_group['name']} for objectives...")
        scan.scan_path_group_for_objectives(path_group, spec_data.get("objectives", []), spec_data.get("options", {}).get("objectiveFlag"), args.verbosity)
        print()

