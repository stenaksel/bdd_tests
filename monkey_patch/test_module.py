import logging

from src.my_module import run_func

LOGGER = logging.getLogger(__name__)


def test_func(caplog) -> None:
    with caplog.at_level(logging.WARNING):
        run_func()
    assert 'Something bad happened!' in caplog.text
