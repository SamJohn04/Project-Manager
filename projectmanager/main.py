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
            if len(args) != 2:
                print("Project manager init failed; Please provide title in format: manage init title")
                exit(1)
            new_specification = specification.init_spec(args[1])
            io.write_specification(new_specification)
        case "add":
            # TODO
            pass
        case "view":
            # TODO
            pass
        case "rm":
            # TODO
            pass


def display_info():
    # TODO
    pass


if __name__ == '__main__':
    main()

