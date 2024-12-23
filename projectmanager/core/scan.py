from collections import namedtuple
from pathlib import Path

from projectmanager.util import paths

ScanInstance = namedtuple("ScanInstance", ["line", "index", "path", "all_lines"])


def scan_path_group(path_group: dict, flag: str) -> list[ScanInstance]:
    scan_instances = []
    for path in paths.from_path_group(path_group):
        scan_instances.extend(scan_path(path, flag))
    return scan_instances


def scan_path(path: Path, flag: str) -> list[ScanInstance]:
    scan_instances = []

    with open(path, encoding="utf-8") as file:
        lines = file.read().splitlines()

    for index, line in enumerate(lines):
        if flag in line:
            scan_instances.append(ScanInstance(line, index, path, lines))
    return scan_instances

