import os
import json
import pathlib
import tempfile

from projectmanager import arg_parse
from projectmanager.feature import init
from projectmanager import config


# @FEAT init IN-PROGRESS
def test_init():
    parser = arg_parse.get_parser()
    with tempfile.TemporaryDirectory() as temp_dir_name:
        os.chdir(temp_dir_name)

        init.init(parser.parse_args(['init', 'title']))

        spec_file_path = pathlib.Path(config.PM_SPECIFICATION_FILE_NAME)
        assert spec_file_path.is_file()
        
        with open(spec_file_path, encoding='utf-8') as spec_file:
            json_data = json.load(spec_file)

        assert json_data == {'title': 'title'}


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

