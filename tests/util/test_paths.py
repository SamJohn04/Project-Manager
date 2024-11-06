import tempfile
from pathlib import Path

from projectmanager.util import paths


def test_from_path_group():
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)

        (temp_dir / "src" / "util" / "subf").mkdir(parents=True)

        python_files = [
                temp_dir / "main.py",
                temp_dir / "a.py",
                temp_dir / "src" / "b.py",
                temp_dir / "src" / "util" / "subf" / "c.py",
                ]

        json_files = [
                temp_dir / "src" / "a.json",
                temp_dir / "src" / "util" / "subf" / "c.json",
                ]

        for file_path in python_files + json_files:
            open(file_path, "x").close()


        assert paths.from_path_group({"name": "main", "dirPath": temp_dir_name, "extensions": []}) == []

        assert paths.from_path_group({"name": "main", "dirPath": temp_dir_name, "extensions": ["py"]}) == python_files
        assert paths.from_path_group({"name": "main", "dirPath": temp_dir_name, "extensions": ["json"]}) == json_files
        assert paths.from_path_group({"name": "main", "dirPath": temp_dir_name, "extensions": ["py", "json"]}) == python_files + json_files
        assert paths.from_path_group({"name": "main", "dirPath": temp_dir_name, "extensions": ["json", "py"]}) == json_files + python_files

        assert paths.from_path_group({"name": "main", "dirPath": str(temp_dir / "src"), "extensions": ["py"]}) == python_files[2:]

