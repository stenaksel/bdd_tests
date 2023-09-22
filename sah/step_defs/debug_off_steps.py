import logging
from logging import INFO

from tests.common.bdd_logger import BddLogger
from tests.common.log_glue_incl import (  # log_msg_end,
    GLUE_LOGGER,
    KEY_LOG_GLUE,
    KEY_LOGGER,
    TEST_CONTEXT,
    assert_messages,
    old_log_msg,
    ret_dict_info,
)

from pytest_bdd import parsers, given, when, then  # isort:skip

# # @given(parsers.parse('that item {item} is present')
# @given(parsers.re('that item "(?P<item>.+?)" is {presence} present'))
# # @given(parsers.parse('that item "{item}" is not present'))
# def step_impl(item: str, presence: str) -> None:
#     print("step_impl:")
#     print(presence)
#     if presence and presence.strip() == "not":
#     # if 'not' in presence:
#         # Handle the case when the item is not present in the context
#         print(f"The {item} is not present in the context")
#     else:
#         # Handle the case when the item is present in the context
#         print(f"The {item} is present in the context")


# from pytest_bdd.parsers import parse

# @given('the {str} item {str} is (not present|present)'
@given(parsers.parse('the "{context_name}" item "{item}" is {presence}'))
def given_context_item_present(context_name: str, item: str, presence: str, context: dict) -> bool:
    assert context is not None
    assert context_name == 'TEST_CONTEXT'
    # assert item == KEY_LOGGER
    assert presence == 'not present' or presence == 'present', f'Unknown "presence" ("{presence}")!'

    print(f'==> Given the "{context_name}" item "{item}" is {presence} <==')

    ctx = None
    # Check wich logger in question (assign to ctx)
    if context_name == 'TEST_CONTEXT':
        ctx = TEST_CONTEXT
    else:
        assert context_name == 'context'
        ctx = context
    assert ctx is not None

    print(f"==> The presence is: '{presence}'")
    # Check if we should have the item in the context (ctx)
    should_be_present = False if 'not' in presence else True
    the_value = ctx.get(item, None)
    print(f"==> should_be_present = {should_be_present} (the_value: '{the_value}')")

    if should_be_present:
        assert the_value is not None, f'Expected "{item}" had a value in "{context_name}"!'
    else:
        assert the_value is None, f'Expected "{item}" to not be present! (value: "{the_value}")'

    ctx['context_checked'] = ctx
    ctx['context_name'] = context_name
    ctx['item_in_context'] = item
    ctx['item_presence'] = should_be_present

    return True   # All asserts passed!


# @given('the {str} item {str} is (not present|present) or value {str}'
@given(parsers.parse('the "{context_name}" item "{item}" is {presence}present or value "{value}"'))
def given_context_item_present_or(
    context_name: str, item: str, presence: str, value: str, context: dict
) -> None:

    assert context is not None
    assert context_name == 'TEST_CONTEXT'
    assert item == KEY_LOGGER
    assert presence == 'is not ', f'Unknown "presence" ("{presence}")!'
    assert 'not' in presence, f'Unknown "presence" ("{presence}")!'

    # Calling other glue to assert the presence or not
    assert given_context_item_present(context_name, item, presence, context)
    assert context is not None

    ctx = context['context_checked']

    # Check if we should have the item in the context (ctx)
    should_be_present = False if 'not' in presence else True
    assert ctx['context_name'] == context_name
    assert ctx['item_in_context'] == item
    assert ctx['item_presence'] == should_be_present

    if should_be_present:
        assert value == 'True'
        assert ctx[KEY_LOGGER] == 'True'
    else:
        assert should_be_present == False
        assert value == 'False'
        assert ctx.get(KEY_LOGGER, None) is None

    # GLUE_LOGGER.info('***************** given_context_item_not_present_or_is *******************')
    # GLUE_LOGGER.info('Given the "TEST_CONTEXT" item "dbg_logging" is not present (or is "False")')
    print('***************** given_context_item_not_present_or_is *****************')
    print("Given the 'TEST_CONTEXT' item 'logging' is not present (or is 'False')")

    # First check if its already a null logger
    the_logger = ctx.get(KEY_LOGGER, None)
    assert the_logger is not None and isinstance(the_logger, logging.Logger), 'How come!'

    if the_logger is not None and the_logger.hasHandlers():
        found_it = False
        num_handlers = len(the_logger.hasHandlers())
        print("num_handlers = %s found in context '%s'!", num_handlers, context_name)
        assert num_handlers == 1, f'Found {num_handlers} in the logger in {context_name}'
        # Iterate over the handlers
        for handler in the_logger.handlers:
            # Check if handler is a null handler
            found_it = isinstance(logging.NullHandler, False)  # Null handler found

        assert found_it, 'No Null Handler found'
        if found_it:
            print("Null Handler found in context '%s'!", context_name)
            return
        # else: just continue

    # Create a null handler
    null_handler = logging.NullHandler()
    assert null_handler.handle(True) == """Stub."""

    # Create a logger and add the null handler
    null_logger = logging.getLogger(KEY_LOG_GLUE)
    logging.getLogger(item).addHandler(null_handler)

    null_logger.addHandler(null_handler)

    the_logger = ctx[KEY_LOGGER] if KEY_LOGGER in ctx else null_logger
    if isinstance(the_logger, GLUE_LOGGER.Logger):
        assert TEST_CONTEXT[KEY_LOGGER] is null_logger, 'TEST_CONTEXT["logger"] is not null_handler'
        assert the_logger.hasHandlers(null_handler)


# @given('the {str} uses Pytest-BDD hooks that calls the corresponding {str} functions')
@given(
    parsers.parse(
        'the "{filename}" uses Pytest-BDD hooks that calls the corresponding "{module}" functions'
    )
)
# def given_file_uses_hooks_calling_module(context: dict, filename: str, module: str) -> None:
def given_file_uses_hooks_calling_module(filename: str, module: str) -> None:
    GLUE_LOGGER.warning('Given a Pytest-BDD test using the "%s" file', filename)
    GLUE_LOGGER.warning('*' * 50)
    assert filename == 'conftest.py', f'Uventet innhold i filename: "{filename}"'
    assert module == KEY_LOG_GLUE, f'Uventet innhold i module: "{module}"'


# def given_file_uses_hooks_calling_module(context: dict, filename: str, module: str):
def given_file_uses_hooks_calling_module(filename: str, module: str):
    logging.warning('Given a Pytest-BDD test using the "%s" file', filename)
    logging.warning('*' * 50)
    assert filename == 'conftest.py', f'Uventet innhold i filename: "{filename}"'
    assert module == 'log_glue', f'Uventet innhold i module: "{module}"'


# Given I set "TEST_CONTEXT" item "logging" with valid value True
@given(parsers.parse('I set {context_name}" item "{item}" with value "{value}"'))
@given(parsers.parse('the "{context_name}" item "{item}" is "{value}"'))
def given_context_item_is(context: dict, context_name: str, item: str, value: str) -> None:
    assert context is not None  # This is the "normal" context fixture
    assert context_name == 'TEST_CONTEXT'  # This is the context fixture to test
    assert item == 'logging'
    assert value == 'True'
    the_context = TEST_CONTEXT if context_name == 'TEST_CONTEXT' else context
    # make bool from string
    the_val = True if value == 'True' else False if value == 'False' else value
    assert the_val is True
    the_context[item] = the_val


@given(parsers.parse('the run is configured with at least log_level = "{wanted_log_level}"'))
def given_run_is_configured_with_at_least_log_level(
    caplog_fixture, context: dict, wanted_log_level: str
) -> None:
    GLUE_LOGGER.warning(
        f'Given the run is configured with at least log_level = "{wanted_log_level}"'
    )
    assert wanted_log_level == 'DEBUG', f'Unexpected log_level: "{wanted_log_level}"'
    # TODO Implement scenario "Given the run is configured with at least log_level = "INFO""
    # Get logger used for logging
    glue_logger = logging.getLogger(KEY_LOG_GLUE)
    logger_name = glue_logger.name
    # print(f"The logger name should be: 'log_glue' = '{logger_name}'")
    assert logger_name == KEY_LOG_GLUE, f'The wanted logger is not in use! Using "{logger_name}"'

    # Get the log level in use
    actual = glue_logger.getEffectiveLevel()
    # Get wanted_log_level as int
    assert isinstance(glue_logger, logging.Logger)
    # From string to int for log level:
    wanted = logging.getLevelName(wanted_log_level)


# # Given I set "TEST_CONTEXT" item "logging" with valid value "True"
# @given(parsers.parse('I set {context_name}" item "{item}" with value "{value}"'))
# # But the "TEST_CONTEXT" item "logging" is not present or is False
# def given_context_item_not_present_or_is(context: dict, context_name: str, item: str, value: str):
#     assert context is not None
#     assert context_name == 'TEST_CONTEXT'
#     assert item == 'dbg_logging'
#     assert value == 'False'


def _just_show_test_context():
    logging.info('==> test_just_show_test_context')
    logging.info('TEST_CONTEXT: ')
    logging.info(TEST_CONTEXT)
    logging.info('<== test_just_show_test_context')


# Given the "TEST_CONTEXT" item "dbg_logging" is not present or is "False"
@given(parsers.parse('the "{context_name}" item "{item}" is not present or is "{value}"'))
# But the "TEST_CONTEXT" item "logging" is not present or is False
def given_context_item_not_present_or_is(context: dict, context_name: str, item: str, value: str):
    assert context is not None
    assert context_name == 'TEST_CONTEXT'
    assert item == 'dbg_logging'
    assert value == 'False'
    _just_show_test_context()

    assert isinstance(actual, int)
    assert isinstance(wanted, int)

    # Compare log_level (int) with wanted_log_level (str)

    assert (
        actual >= wanted
    ), f'Unexp. actual log_level={actual} >= Wanted={wanted} ({wanted_log_level})'


def _is_logging(logger, tf_caplog) -> bool:
    """Display caplog capture text"""
    # log at all logging levels
    logger.debug('DEBUG: log entry captured')
    logger.info('INFO: log entry captured')
    logger.error('ERROR: log entry captured')
    logger.warning('WARNING: log entry captured')
    # display capture log
    print('\nCAPLOG1:')
    output = tf_caplog.text.rstrip('\n').split(sep='\n')
    if output == ['']:
        print('\tNothing captured1')
        return False
    num_found = len(output)
    print(f'\tcaptured {num_found} loggings')

    # show last 15 loggings (if available)
    start_at = num_found if num_found <= 15 else (num_found - 15)
    # iterate from start_at to num_found

    for i in range(start_at, num_found):
        print(f'{i}: {output[i]}')

    return True


def _is_logging(logger, tf_caplog) -> bool:
    """Display caplog capture text"""
    # log at all logging levels
    logger.debug('DEBUG: log entry captured')
    logger.info('INFO: log entry captured')
    logger.error('ERROR: log entry captured')
    logger.warning('WARNING: log entry captured')
    # display capture log
    print('\nCAPLOG2:')
    output = tf_caplog.text.rstrip('\n').split(sep='\n')
    if output == ['']:
        print('\tNothing captured2')
        return False
    for i in range(len(output)):
        print(f'{i}: {output[i]}')
    return True


# Given the run is configured with at least log_level = "INFO"
@given(parsers.parse('the run is configured with at least log_level = "{wanted_log_level}"'))
def given_run_is_configured_with_at_least_log_level(
    caplog_fixture, context: dict, wanted_log_level: str
):
    logging.warning(f'Given the run is configured with at least log_level = "{wanted_log_level}"')
    assert wanted_log_level == 'INFO', f'Unexpected log_level: "{wanted_log_level}"'
    # TODO Implement scenario "Given the run is configured with at least log_level = "INFO""
    # Get logger used for logging
    logger = logging.getLogger()
    logger_name = logger.name
    print(f'The logger name is: {logger_name}')
    # Get the log level in use
    log_level = logger.getEffectiveLevel()

    wanted_log_level_int = logging.getLevelNamesMapping().get(wanted_log_level)
    assert (
        log_level >= wanted_log_level_int
    ), f'Unexpected log_level: "{logging.getLevelName(log_level)}" {log_level})'


@when('Pytest-BDD is run')
@when('the scenario is run')
def when_the_scenario_is_run(caplog_fixture, context: dict) -> None:
    assert context is not None

    # Clear the captured log records and formatted log output
    caplog_fixture.clear()

    # Assert that the log is cleared
    assert not _is_logging(GLUE_LOGGER, caplog_fixture), 'caplog was not cleared!'
    assert (
        len(caplog_fixture.records) == 0
    ), f'caplog was not cleared! Found {len(caplog_fixture.records)} records'

    GLUE_LOGGER.info('%s', '-' * 50)
    logging.warning('This message will be reported when running')
    logging.info('This message will be reported when running')
    GLUE_LOGGER.warning('This message will not be reported when running')
    GLUE_LOGGER.info('This message will not be reported when running')
    GLUE_LOGGER.info('%s', '-' * 50)

    assert _is_logging(GLUE_LOGGER, caplog_fixture)

    assert (
        len(caplog_fixture.records) == 2
    ), f'caplog is as expected! Found {len(caplog_fixture.records)} records'
    # assert caplog_fixture.text == '', f'caplog is as expected! Found text!\n{caplog_fixture.text}'


# Then there should not be any logging from "log_glue" functions
@then(parsers.parse('there should {want}be logging from "{module}" functions'))
def given_step_using_the_module(caplog_fixture, context: dict, want: str, module: str) -> None:
    # assert want in {'not ', 'not be any ', 'be '}, f'Unknown value for "want" (: "{want}")!'
    assert want == 'not ', f'Unknown value for "want" (: "{want}")!'
    assert module == KEY_LOG_GLUE

    # assert False, 'Stopping in func: given_step_using_the_module'
    assert len(caplog_fixture.records) == 0
    assert caplog_fixture.text == ''
    logging.warning('\nwhen_the_scenario_is_run\n')


# TODO Then there should not be any logging from "BDDLogger" functions
@then(parsers.parse('there should not be any logging from "{module}" functions'))
def given_step_using_the_module(caplog_fixture, context: dict, module: str):
    assert module == 'log_glue'
    # assert False, 'Stop here!!! (given_step_using_the_module)'
    context[KEY_DBG_LOG_GLUE] = True
    context[KEY_DBG_LOGGING] = None

    # Use the caplog_fixture to access the caplog object,
    # and assert that the log is empty
    # assert 'HUMBUG' in caplog_fixture.text, f'caplog is not empty! Found text: HUMBUG!'
    # caplog_fixture.clear()  # TODO Remove, just testing

    caplog_fixture.text
    num_logs = len(caplog_fixture.records)
    if 'not' in want:

        assert_messages(caplog_fixture, level=INFO)
        # assert_messages(caplog_fixture, level=INFO, caplog_fixture.records)

        assert num_logs == 0, f'caplog is not empty! Found {num_logs} logs'
        assert caplog_fixture.text == '', f'caplog is not empty! Found text!\n{caplog_fixture.text}'

    else:
        assert len(want) == 0, f'Unknown value for "want" (: "{want}")!'
    assert num_logs == 0, f'caplog is not empty! Found {num_logs} logs'
    assert caplog_fixture.text == '', f'caplog is not empty! Found text!'


# Then there should not be any logging from "log_glue" functions
@then(parsers.parse('there should be logging from "{module}" functions'))
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
