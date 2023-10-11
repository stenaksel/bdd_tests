import pytest

# @pytest.mark.ok
@pytest.mark.skip
def test_example(pytestconfig):
    # Access command-line options
    if pytestconfig.getoption('verbose'):
        print('Running in verbose mode')

    # Access configuration values from pytest.ini or pytest.cfg
    log_level = pytestconfig.getini('log_level')
    print(f'Log level: {log_level}')

    # # Access environment variables
    # api_key = pytestconfig.getoption("api_key")
    # print(f"API key: {api_key}")
