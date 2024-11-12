from pathlib import Path
import tempfile
import pytest

from projectmanager.core import scan


def test_scan_path_group_for_todos():
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)

        (temp_dir / "src" / "util" / "subf").mkdir(parents=True)

        python_files = [
                (temp_dir / "main.py", "def main():\n\t# TODO\n\tpass\n"),
                (temp_dir / "a.py", "\n# @OBJECTIVE main\ndef next():\n\tpass\n\t# TODO\n"),
                (temp_dir / "src" / "b.py", "# TODO"),
                (temp_dir / "src" / "util" / "subf" / "c.py", ""),
                ]

        for file_path, content in python_files:
            with open(file_path, "x") as file:
                file.write(content)

        assert scan.scan_path_group_for_todos({"name": "main", "dirPath": temp_dir_name, "extensions": ["py"]}) == [
                (python_files[0][0], [1]),
                (python_files[1][0], [4]),
                (python_files[2][0], [0]),
                (python_files[3][0], [])
                ]


def test_scan_path_group_for_objectives():
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)

        (temp_dir / "src" / "util" / "subf").mkdir(parents=True)

        python_files = [
                (temp_dir / "main.py", "def main():\n\t# TODO\n\tpass\n"),
                (temp_dir / "a.py", "\n# @OBJECTIVE main\ndef next():\n\tpass\n\t# TODO\n"),
                (temp_dir / "src" / "b.py", "# TODO"),
                (temp_dir / "src" / "util" / "subf" / "c.py", ""),
                ]

        for file_path, content in python_files:
            with open(file_path, "x") as file:
                file.write(content)

        assert scan.scan_path_group_for_objectives({"name": "main", "dirPath": temp_dir_name, "extensions": ["py"]}) == [
                (python_files[0][0], []),
                (python_files[1][0], [(1, "main", None)]),
                (python_files[2][0], []),
                (python_files[3][0], [])
                ]


def test_scan_todos_from_content():
    content = """def main():
        print("How are you?")


    def next():
        # TODO
        print("this is TODO")

    """

    assert scan.scan_todos_from_content(content, "TODO") == [5, 6]
    assert scan.scan_todos_from_content(content, flag="# TODO") == [5]

    assert scan.scan_todos_from_content("Hello There!!\nHow are you?" "TODO") == []
    assert scan.scan_todos_from_content("Hello There!!\nHow are you?", flag="are") == [1]


def test_scan_objectives_from_content():
    content = """
    # @OBJECTIVE main
    def main():
        # @FEAT main done
        print("how are you?")
    

    # @OBJECTIVE next todo
    def next():
        # TODO
        pass
    """

    with pytest.raises(ValueError):
        scan.scan_objectives_from_content("@OBJECTIVE\ndef abc():\n\tprint()")

    assert scan.scan_objectives_from_content(content, "@OBJECTIVE") == [(1, "main", None), (7, "next", "todo")]
    assert scan.scan_objectives_from_content(content, flag="@FEAT") == [(3, "main", "done")]

    assert scan.scan_objectives_from_content("HELLO WORLD!\nHOW ARE YOU?", "@OBJECTIVE") == []
    assert scan.scan_objectives_from_content("HELLO WORLD!\nHOW ARE YOU?", flag="ARE") == [(1, "YOU?", None)]

