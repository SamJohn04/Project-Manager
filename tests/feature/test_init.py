import pathlib
from projectmanager.feature import init


# @FEAT init ON-HOLD
def test_init():
    # TODO
    pass


def test_get_items_to_create():
    assert init.get_items_to_create({"name": "templ", "toCreate": []}) == init.ItemsToCreate([], [])
    assert init.get_items_to_create({"name": "templ", "toCreate": [{"type": "dir", "path": "a"}, {"type": "dir", "path": "b"}]}) == init.ItemsToCreate(
            dirs=[pathlib.Path("a"), pathlib.Path("b")],
            files=[]
            )
    assert init.get_items_to_create({"name": "templ", "toCreate": [{"type": "file", "path": "a.py"}]}) == init.ItemsToCreate(
            dirs=[],
            files=[(pathlib.Path("a.py"), "")]
            )
    assert init.get_items_to_create({"name": "templ", "toCreate": [{"type": "file", "path": "a.py", "content": "hello world"}]}) == init.ItemsToCreate(
            dirs=[],
            files=[(pathlib.Path("a.py"), "hello world")]
            )
    assert init.get_items_to_create({"name": "templ", "toCreate": [{"type": "file", "path": "a.py", "content": "hello world"}, {"type": "dir", "path": "a"}]}) == init.ItemsToCreate(
            dirs=[pathlib.Path("a")],
            files=[(pathlib.Path("a.py"), "hello world")]
            )

