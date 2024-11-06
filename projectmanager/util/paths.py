from pathlib import Path


def from_path_group(path_group: dict) -> list[Path]:
    dir_path = Path(path_group["dirPath"])

    paths = []

    for extension in path_group["extensions"]:
        paths.extend(dir_path.glob("**/*." + extension))

    return paths

