from connect_to_forum.main import main
from unittest.mock import patch

import pytest

from tests.common import get_event_with_data


def test_main():
    

    data = (1, 'name')

    with patch('connect_to_forum.main.session'):
        with pytest.raises(TypeError):
            main(get_event_with_data(data), 'context')
