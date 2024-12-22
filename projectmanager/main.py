from argparse import Namespace
from projectmanager.arg_parse import parse_args

from projectmanager.feature.add_item import add_item
from projectmanager.feature.generate import generate
from projectmanager.feature.init import init
from projectmanager.feature.remove import remove
from projectmanager.feature.set_options import set_options
from projectmanager.feature.status import status
from projectmanager.feature.view import view

from projectmanager.util import io


def main():
    args = parse_args()

    try:
        act(args)
    except Exception as e:
        io.err(str(e))


def act(args: Namespace):
    match args.command:
        case "init":
            init(args)
        case "add":
            add_item(args)
        case "view":
            view(args)
        case "rm":
            remove(args)
        case "status" | "scan":
            status(args)
        case "generate":
            generate(args)
        case "set" | "unset":
            set_options(args)


if __name__ == '__main__':
    main()

