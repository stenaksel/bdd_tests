import logging
from logging import INFO

from tests.common.log_glue_incl import (  # log_msg_end,; TEST_CONTEXT,
    GLUE_LOGGER,
    KEY_LOG_GLUE,
    KEY_LOGGER,
    assert_messages,
)

# from tests.common.pytest_bdd_logger import PytestBddLogger
from tests.common.pytest_bdd_logger_interface import TEST_CONTEXT, _ret_func_name

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


def _expect_present(expected_present: bool, context_name: str, key: str, context: dict) -> bool:
    assert expected_present is not None, f'Expected "expected_present" to be present!'
    assert context_name is not None, f'Expected "context_name" to be present!'
    assert key is not None,       f'Expected "key" to be present!'

    # Check wich logger in question (assign to ctx)
    the_context = TEST_CONTEXT if context_name == 'TEST_CONTEXT' else context
    assert the_context is not None, 'context must be provided'

    print(f"==> The presence is: '{expected_present}'")
    the_value = the_context.get(key, None)
    print(f"==> expected_present = {expected_present} (the_value: '{the_value}')")

    if expected_present:
        assert the_value is not None, f'Expected "{key}" to be present!'
    else:
        assert the_value is None, f'Expected "{key}" to not be present! (value: "{the_value}")'

    return True   # All asserts passed!


# @given('xthe {str} item {str} is (not present|present)'
@given(parsers.parse('xthe "{context_name}" item "{item}" {is_present} present'))
def given_context_item_present(
    context_name: str, item: str, is_present: str, context: dict
) -> bool:
    assert context is not None, 'context must be provided'
    assert context_name == 'TEST_CONTEXT'
    # assert item == KEY_LOGGER
    assert is_present == 'is not' or is_present == 'is', f'Unknown "is_present" ("{is_present}")!'

    print(f'==> Given the "{context_name}" item "{item}" is {is_present} <==')

    should_be_present = False if 'not' in is_present else True

    assert _expect_present(
        should_be_present, context_name, item, context
    ), f'Expected "{item}" to be present in "{context_name}"! \
        (value: "{TEST_CONTEXT.get(item, None)}")'

    print(f"==> The is_present is: '{is_present}'")
    # Check if we should have the item in the context (ctx)
    should_be_present = False if 'not' in is_present else True
    the_value = TEST_CONTEXT.get(item, None)
    print(f"==> should_be_present = {should_be_present} (the_value: '{the_value}')")

    if should_be_present:
        assert the_value is not None, f'Expected "{item}" had a value in "{context_name}"!'
    else:
        assert the_value is None, f'Expected "{item}" to not be present! (value: "{the_value}")'

    if should_be_present:   # We might check its value so add it to the TEST_CONTEXT
        TEST_CONTEXT['checked_context_name'] = context_name
        TEST_CONTEXT['checked_context_item_name'] = item
        TEST_CONTEXT['checked_context_item_value'] = the_value
        # TODO should these be removed in after_scenario?
        TEST_CONTEXT['remove_in_after_scenario'] = [
            'checked_context_name',
            'checked_context_item_name',
            'checked_context_item_value',
        ]
    logging.info('TEST_CONTEXT: %s', TEST_CONTEXT)

    return True   # All asserts passed!


# @then('xthe {str} item {str} should (not be|be) present'
# @then(parsers.parse('xthe "{context_name}" item "{item}" should {is_present} present'))
# def then_context_should_be_item_present(\
# context: dict, context_name: str, item: str, is_present: str) -> bool:
#     return then_context_item_present(context, context_name, item, is_present)


# @then('the {str} item {str} should (not be|be) present'
@then(parsers.parse('the "{context_name}" item "{item}" should {be_present} present'))
def then_context_item_present(context: dict, context_name: str, item: str, be_present: str) -> bool:
    assert context is not None, 'context must be provided'
    assert context_name == 'TEST_CONTEXT'
    assert be_present == 'not be' or be_present == 'be', f'Unknown "be_present" ("{be_present}")!'
    logging.info(
        '==> Given the "%s" item "%s" should %s present <==',
        context_name,
        item,
        be_present,
    )

    should_be_present = False if 'not' in be_present else True

    assert _expect_present(
        should_be_present, context_name, item, context
    ), f'Expected "{item}" to be present in "{context_name}"!'
    # assert False, f'Stopping!! ("{be_present}")!'

    if should_be_present:   # We might check its value so add it to the context in question
        context['checked_context_name'] = context_name
        context['checked_context_item_name'] = item
        context['checked_context_item_value'] = TEST_CONTEXT.get(item, None)
        # TODO should these be removed in after_scenario?
        context['remove_in_after_scenario'] = [
            'checked_context_name',
            'checked_context_item_name',
            'checked_context_item_value',
        ]
    assert False


# @then('the value should be {str}.')
@then(parsers.parse('the value should be "{expected_value}".'))
def then_value_should_be(context: dict, expected_value: str) -> None:
    assert context is not None, 'context must be provided'
    assert expected_value is not None, f'Expected "expected_value" to be present!'
    # 'checked_context_name',
    # 'checked_context_item_name',
    # 'checked_context_item_value'
    # assert False, 'Stopping!!! then_value_should_be()'

    ctx = TEST_CONTEXT
    logging.info('TEST_CONTEXT: %s', ctx)
    logging.info('context: %s', context)
    # ctx = context   #TODO remove

    if 'checked_context_name' in context and 'checked_context_name' == 'context':
        ctx = context
        logging.warning('Switch ctx from TEST_CONTEXT to context')

    assert ctx is not None, f'Expected "ctx" to be present!'

    if 'checked_context_item_value' in ctx:
        actual_value = ctx.get('checked_context_item_value', None)
        assert (
            actual_value == expected_value
        ), f'Expected "{expected_value}" but got "{actual_value}"'
    else:
        assert (
            False
        ), f'Expected "{expected_value}", \
            but no knowledge of what to check against! {_ret_func_name()}'


# @given('the {str} item {str} is (not present|present) or value {str}'
@given(
    parsers.parse('the "{context_name}" item "{item}" is {is_present}present or value "{value}"')
)
def given_context_item_present_or(
    context_name: str, item: str, is_present: str, value: str, context: dict
) -> None:

    assert context is not None, 'context must be provided'
    assert context_name == 'TEST_CONTEXT'
    assert item == KEY_LOGGER
    assert is_present == 'is not ', f'Unknown "is_present" ("{is_present}")!'   # TODO Needs fixing
    assert 'not' in is_present, f'Unknown "is_present" ("{is_present}")!'

    # Calling other glue to assert the presence or not
    assert given_context_item_present(context_name, item, is_present, context)
    assert context is not None, 'context must be provided'

    ctx = context['context_checked']

    # Check if we should have the item in the context (ctx)
    should_be_present = False if 'not' in is_present else True
    assert ctx['context_name'] == context_name
    assert ctx['item_in_context'] == item
    assert ctx['item_is_present'] == should_be_present

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
            found_it = isinstance(handler, logging.NullHandler)  # Null handler found

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


@given(parsers.parse('the run is configured with at least log_level = "{wanted_level}"'))
def given_run_is_configured_with_at_least_log_level(
    caplog_fixture, context: dict, wanted_level: str
) -> None:
    GLUE_LOGGER.warning('Given the run is configured with at least log_level = "%s"', wanted_level)
    assert wanted_level == 'DEBUG', f'Unexpected log_level: "{wanted_level}"'
    # TODO Implement scenario "Given the run is configured with at least log_level = "INFO""
    # Get logger used for logging
    glue_logger = logging.getLogger(KEY_LOG_GLUE)
    logger_name = glue_logger.name
    # print(f"The logger name should be: 'log_glue' = '{logger_name}'")
    assert logger_name == KEY_LOG_GLUE, f'The wanted logger is not in use! Using "{logger_name}"'

    # Get the log level in use
    actual = glue_logger.getEffectiveLevel()
    # Get wanted_level as int
    assert isinstance(glue_logger, logging.Logger)
    # From string to int for log level:
    wanted = logging.getLevelName(wanted_level)
    assert actual == wanted, f'Unexpected log_level: "{actual}"! wanted: "{wanted}"'


# # Given I set "TEST_CONTEXT" item "logging" with valid value "True"
# @given(parsers.parse('I set {context_name}" item "{item}" with value "{value}"'))
# # But the "TEST_CONTEXT" item "logging" is not present or is False
# def given_context_item_not_present_or_is(context: dict, context_name: str, item: str, value: str):
#     assert context is not None, 'context must be provided'
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
    assert context is not None, 'context must be provided'
    assert context_name == 'TEST_CONTEXT'
    assert item == 'dbg_logging'
    assert value == 'False'
    _just_show_test_context()

    # assert isinstance(actual, int)
    # assert isinstance(wanted, int)

    # # Compare log_level (int) with wanted_level (str)

    # assert (
    #     actual >= wanted
    # ), f'Unexp. actual log_level={actual} >= Wanted={wanted} ({wanted_level})'


def x_is_logging(logger, tf_caplog) -> bool:
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
@given(parsers.parse('the run is configured with at least log_level = "{wanted_level}"'))
def given_run_is_configured_with_at_least_log_level2(
    caplog_fixture, context: dict, wanted_level: str
):
    logging.warning('Given the run is configured with at least log_level = "%s"', wanted_level)
    assert wanted_level == 'INFO', f'Unexpected log_level: "{wanted_level}"'
    # TODO Implement scenario "Given the run is configured with at least log_level = "INFO""
    # Get logger used for logging
    logger = logging.getLogger()
    logger_name = logger.name
    print(f'The logger name is: {logger_name}')
    # Get the log level in use
    log_level = logger.getEffectiveLevel()

    wanted_level_int = logging.getLevelNamesMapping().get(wanted_level)
    assert (
        log_level >= wanted_level_int
    ), f'Unexpected log_level: "{logging.getLevelName(log_level)}" {log_level})'


@when('Pytest-BDD is run')
@when('the scenario is run')
def when_the_scenario_is_run(caplog_fixture, context: dict) -> None:
    assert context is not None, 'context must be provided'

    # Clear the captured log records and formatted log output
    # caplog_fixture.clear()

    # TODO move to another step def: Given the logger is empty
    # Assert that the log is cleared
    # assert not _is_logging(GLUE_LOGGER, caplog_fixture), 'caplog was not cleared!'
    # assert (
    #     len(caplog_fixture.records) == 0
    # ), f'caplog was not cleared! Found {len(caplog_fixture.records)} records'

    GLUE_LOGGER.info('%s', '-' * 50)
    logging.warning('This message will be reported when running (warning)')
    logging.info('This message will be reported when running (info)')
    GLUE_LOGGER.warning('This message will not be reported when running! (warning)')
    GLUE_LOGGER.info('This message will not be reported when running! (info)')
    GLUE_LOGGER.info('%s', '-' * 50)

    assert _is_logging(GLUE_LOGGER, caplog_fixture)

    assert (
        len(caplog_fixture.records) == 2
    ), f'caplog is as expected! Found {len(caplog_fixture.records)} records'
    # assert caplog_fixture.text == '', f'caplog is as expected! Found text!\n{caplog_fixture.text}'


# Then there should not be any logging from "log_glue" functions
@then(parsers.parse('x-there should be logging from "{module}" functions'))
def x_then_step_using_the_module(caplog_fixture, context: dict, module: str):
    assert module == 'log_glue'
    # assert False, 'Stop here!!! (given_step_using_the_module)'
    context[KEY_DBG_LOG_GLUE] = True
    context[KEY_DBG_LOGGING] = None

    # Use the caplog_fixture to access the caplog object,
    # and assert that the log is empty
    num_logs = len(caplog_fixture.records)
    assert num_logs == 0, f'caplog is not empty! Found {num_logs} logs'
    assert caplog_fixture.text == '', f'caplog is not empty! Found text!'


# Then there should not be any logging from "log_glue" functions
@then(parsers.parse('there should {want}be logging from "{module}" functions'))
def then_step_using_the_module(caplog_fixture, context: dict, want: str, module: str) -> None:
    # assert want in {'not ', 'not be any ', 'be '}, f'Unknown value for "want" (: "{want}")!'
    assert want == 'not ', f'Unknown value for "want" (: "{want}")!'
    assert module == KEY_LOG_GLUE

    # assert False, 'Stopping in func: given_step_using_the_module'
    assert len(caplog_fixture.records) == 0
    assert caplog_fixture.text == ''
    logging.warning('\nwhen_the_scenario_is_run\n')


# TODO Then there should not be any logging from "PytestBddLogger" functions
@then(parsers.parse('there should {want} logging from "{module}" functions'))
def given_step_using_the_module(caplog_fixture, context: dict, want: str, module: str):
    assert want in ['not be any', 'be'], f'Unknown value for "want" (: "{want}")!'
    assert module == 'log_glue'   # TODO Use real name: 'PytestBddLogger'
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

    assert num_logs == 0, f'caplog is not empty! Found {num_logs} logs'
    assert caplog_fixture.text == '', f'caplog is not empty! Found text!'
