import logging

logger = logging.getLogger(__name__)

from logging import DEBUG, INFO, WARNING

from tests.common.log_glue import *
from tests.common.log_glue_incl import (  # log_msg_end,
    KEY_DBG_LOG_GLUE,
    KEY_DBG_LOGGING,
    TEST_CONTEXT,
    log_msg,
    ret_dict_info,
)

from pytest_bdd import parsers, given, when, then  # isort:skip

# from pytest_bdd.parsers import parse


# Some "globals":
EXPECTED_NUM_PARAMS = None  # TODO Implement scenario "Then" step for checking?

# When the "filename" uses Pytest-BDD hooks that calls the corresponding "log_glue" functions
@given(
    parsers.parse(
        'the "{filename}" uses Pytest-BDD hooks that calls the corresponding "{module}" functions'
    )
)
# def given_file_uses_hooks_calling_module(context: dict, filename: str, module: str):
def given_file_uses_hooks_calling_module(filename: str, module: str):
    logging.warning('Given a Pytest-BDD test using the "%s" file', filename)
    logging.warning('*' * 50)
    assert filename == 'filename', f'Uventet innhold i filename: "{filename}"'
    assert module == 'log_glue', f'Uventet innhold i module: "{module}"'


# Given I set "TEST_CONTEXT" item "logging" with valid value True
@given(parsers.parse('I set {context_name}" item "{item}" with value "{value}"'))
@given(parsers.parse('the "{context_name}" item "{item}" is "{value}"'))
def given_context_item_is(context: dict, context_name: str, item: str, value: str):
    assert context is not None  # This is the "normal" context fixture
    assert context_name == 'TEST_CONTEXT'  # This is the context fixture to test
    assert item == 'logging'
    assert value == 'True'
    the_context = TEST_CONTEXT if context_name == 'TEST_CONTEXT' else context
    # make bool from string
    the_val = True if value == 'True' else False if value == 'False' else value
    assert the_val is True
    the_context[item] = the_val

# # Given I set "TEST_CONTEXT" item "logging" with valid value "True"
# @given(parsers.parse('I set {context_name}" item "{item}" with value "{value}"'))
# # But the "TEST_CONTEXT" item "logging" is not present or is False
# def given_context_item_not_present_or_is(context: dict, context_name: str, item: str, value: str):
#     assert context is not None
#     assert context_name == 'TEST_CONTEXT'
#     assert item == 'dbg_logging'
#     assert value == 'False'


# Given the "TEST_CONTEXT" item "dbg_logging" is not present or is "False"
@given(parsers.parse('the "{context_name}" item "{item}" is not present or is "{value}"'))
# But the "TEST_CONTEXT" item "logging" is not present or is False
def given_context_item_not_present_or_is(context: dict, context_name: str, item: str, value: str):
    assert context is not None
    assert context_name == 'TEST_CONTEXT'
    assert item == 'dbg_logging'
    assert value == 'False'


# Given the run is configured with at least log_level = "INFO"
@given(parsers.parse('the run is configured with at least log_level = "{wanted_log_level}"'))
def given_run_is_configured_with_at_least_log_level(caplog_fixture, context: dict, wanted_log_level: str):
    logging.warning(f'Given the run is configured with at least log_level = "{log_level}"')
    assert wanted_log_level == 'INFO', f'Unexpected log_level: "{wanted_log_level}"'
    #TODO Implement scenario "Given the run is configured with at least log_level = "INFO""
    #Get logger used for logging
    logger = logging.getLogger()
    logger_name = logger.name
    print(f"The logger name is: {logger_name}")
    #Get the log level in use
    log_level = logger.getEffectiveLevel()
    assert log_level > wanted_log_level








@when('Pytest-BDD is run')
@when('the scenario is run')
def when_the_scenario_is_run(caplog_fixture, context: dict):
    assert context is not None

    # Clear the captured log records and formatted log output
    caplog_fixture.clear()

    # Assert that the log is cleared
    assert len(caplog_fixture.records) == 0
    assert caplog_fixture.text == ''


# Then there should not be any logging from "log_glue" functions
@then(parsers.parse('there should not be any logging from "{module}" functions'))
def given_step_using_the_module(caplog_fixture, context: dict, module: str):
    assert module == 'log_glue'
    # assert False, 'Stop here!!! (given_step_using_the_module)'
    context[KEY_DBG_LOG_GLUE] = True
    context[KEY_DBG_LOGGING] = None

    # Use the caplog_fixture to access the caplog object,
    # and assert that the log is empty
    # assert 'HUMBUG' in caplog_fixture.text, f'caplog is not empty! Found text: HUMBUG!'
    num_logs = len(caplog_fixture.records)
    assert num_logs == 0, f'caplog is not empty! Found {num_logs} logs'
    assert caplog_fixture.text == '', f'caplog is not empty! Found text!'
