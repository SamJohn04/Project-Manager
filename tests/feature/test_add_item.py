import os
import tempfile

from projectmanager import arg_parse
from projectmanager.feature import add_item, init
from projectmanager.util import io


# @FEAT add_item IN-PROGRESS
def test_add_item():
    parser = arg_parse.get_parser()
    with tempfile.TemporaryDirectory() as temp_dir_name:
        os.chdir(temp_dir_name)

        init.init(parser.parse_args(['init', 'title']))

        add_item.add_item(parser.parse_args(['add', 'objective', 'first']))
        add_item.add_item(parser.parse_args(['add', 'objective', '-d', 'description', 'second']))

        spec_data = io.read_specification()
        
        assert len(spec_data['objectives']) == 2
        assert spec_data['objectives'][0]['name'] == 'first'
        assert spec_data['objectives'][1]['name'] == 'second' and spec_data['objectives'][1]['description'] == 'description'

