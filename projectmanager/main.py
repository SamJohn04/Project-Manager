import sys

from projectmanager.core import specification
from projectmanager.util import io


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        display_info()
        exit(0)

    match args[0]:
        case "init":
            init(args[1:])
        case "add":
            add(args[1:])
        case "view":
            view(args[1:])
        case "rm":
            remove(args[1:])


def display_info():
    # TODO
    pass


def init(args: list[str]):
    if len(args) == 0:
        title = input("Project title: ")
    else:
        title = ' '.join(args)

    new_spec_data = specification.init_spec(title)
    io.write_specification(new_spec_data)


def add(args: list[str]):
    try:
        spec_data = io.read_specification()
    except FileNotFoundError:
        print("Specification has not yet been initialized. Please initialize the specification file with init.")
        exit(1)

    if len(args) == 0:
        what_to_add = input("What would you like to add? (objective | path): ")
    else:
        what_to_add = args[0]

    match what_to_add:
        case "objective":
            if len(args) < 2:
                objective_name = input("Objective name: ")
            else:
                objective_name = args[1]
            if len(args) < 3:
                objective_description = input("Objective description: ") if len(args) < 3 else ' '.join(args[2:])
            else:
                objective_description = ' '.join(args[2:])

            try:
                specification.add_objective(spec_data, objective_name, objective_description)
            except ValueError as e:
                print(f"Adding Objective failed... {e}")
                exit(1)
        case "path":
            if len(args) < 2:
                path_name = input("Path Group name: ")
            else:
                path_name = args[1]
            if len(args) < 3:
                path_dir = input("Path Group directory path: ")
            else:
                path_dir = args[2]
            if len(args) < 4:
                extensions = input("Extensions (separated by \", \"): ").split(", ")
            else:
                extensions = args[3:]

            try:
                specification.add_path_group(spec_data, path_name, path_dir, extensions)
            except ValueError as e:
                print(f"Adding Path Group failed... {e}")
                exit(1)
        case _:
            print("Invalid option; please enter \"objective\" or \"path\".")
            exit(-1)

    io.write_specification(spec_data)


def view(args: list[str]):
    # TODO
    pass


def remove(args: list[str]):
    # TODO
    pass


if __name__ == '__main__':
    main()

