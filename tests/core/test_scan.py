import pytest
from projectmanager.core import scan

def test_scan_todos_from_content():
    content = """def main():
        print("How are you?")


    def next():
        # TODO
        print("this is TODO")

    """

    assert scan.scan_todos_from_content(content) == [5, 6]
    assert scan.scan_todos_from_content(content, flag = "# TODO") == [5]

    assert scan.scan_todos_from_content("Hello There!!\nHow are you?") == []
    assert scan.scan_todos_from_content("Hello There!!\nHow are you?", flag = "are") == [1]


def test_scan_objectives_from_content():
    content = """
    # @OBJECTIVE main
    def main():
        print("how are you?")
    

    # @OBJECTIVE next todo
    def next():
        # TODO
        pass
    """

    with pytest.raises(ValueError):
        scan.scan_objectives_from_content("@OBJECTIVE\ndef abc():\n\tprint()")

    assert scan.scan_objectives_from_content(content) == [(1, "main", None), (6, "next", "todo")]
    assert scan.scan_objectives_from_content("HELLO WORLD!\nHOW ARE YOU?") == []

