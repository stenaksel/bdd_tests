from logging import Logger
import pytest
from unittest import mock
from src.my_module import run_func


def test_run_func_logging():
    # with mock.patch('<module_name>.logger') as mock_logger:
    with mock.patch('test_logging.logger') as mock_logger:
        run_func()
        mock_logger.info.assert_called_once_with('Specific text')
