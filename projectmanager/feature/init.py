from argparse import Namespace
from collections import namedtuple
import pathlib
from projectmanager import config
from projectmanager.core import specification, template
from projectmanager.util import io

ItemsToCreate = namedtuple("ItemsToCreate", ["dirs", "files"])


# @FEAT init REVIEW
def init(args: Namespace):
    if io.specification_exists() and not args.force:
        io.err("Specification file already exists. Use -f | --force to reinitialize and overwrite anyway.")
        return

    if args.template is None:
        spec_data = specification.init_spec(args.title)
    else:
        template_data = io.read_template(args.template)
        spec_data = template.create_from_template(args.title, template_data, args.verbosity)

    io.write_specification(spec_data)

    if args.verbosity == config.V_NORMAL:
        io.success(f"Specification initialized")
    elif args.verbosity == config.V_VERBOSE:
        io.success(f"{args.title}: specification has been initialized successfully.")


def from_template(title: str, template_data: dict, verbosity_level: int = config.V_NORMAL) -> dict:
    items_to_create = get_items_to_create(template_data)

    for dir_path in items_to_create.dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        if verbosity_level == config.V_VERBOSE:
            print(f"Directory \"{dir_path}\" created.")

    for file_path, file_content in items_to_create.files:
        io.write_content(file_content, file_path, to_append=False, title=title)
        if verbosity_level == config.V_VERBOSE:
            print(f"File \"{file_path}\" created.")

    if verbosity_level != config.V_QUIET:
        io.success("Files and Directories to be created have been generated.")

    spec_data = specification.init_spec(title)

    if "pathGroups" in template_data:
        spec_data["pathGroups"] = template_data["pathGroups"]

    if verbosity_level == config.V_NORMAL and len(spec_data.get("pathGroups", [])) > 0:
        print("Path Groups:", *(path_group["name"] for path_group in spec_data["pathGroups"]))
    elif verbosity_level == config.V_VERBOSE and len(spec_data.get("pathGroups", [])) > 0:
        print("Path Groups")
        for path_group in spec_data["pathGroups"]:
            print('|--', specification.path_group_to_str(path_group))
    
    return spec_data


def get_items_to_create(template_data: dict) -> ItemsToCreate:
    items_to_create = ItemsToCreate([], [])

    for item_to_create in template_data["toCreate"]:
        path_to_create = pathlib.Path(item_to_create["path"])
        if item_to_create["type"] == "dir":
            items_to_create.dirs.append(path_to_create)
        elif item_to_create["type"] == "file":
            items_to_create.files.append((path_to_create, item_to_create.get("content", "")))

    return items_to_create

