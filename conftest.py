# content of "root" conftest.py

"""
It is NOT possible to use multiple conftest.py files simultaneously.
When pytest runs, it automatically discovers and applies the conftest.py file
that is closest to the test file being executed.

The best location for the conftest.py file in a pytest project is typically in
the top-level test directory or the project root directory.
Placing the conftest.py file in the top-level directory allows it to have
a broader scope and makes the fixtures and configurations defined in
the conftest.py file available to all tests in the project.
------------------------------------------------------------------------------
In the context of this example there are multiple folders
that each have their own features folder and step_defs folder,
so the conftest.py file have been put in the root folder.
(Only conftest_glue have a "local" conftest.py for it's example code)
"""

import logging
from collections import OrderedDict

# from logging import WARN
from typing import Any, Callable, Optional

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Item
from pytest_bdd.parser import Feature, Scenario, Step

from tests.common.log_helper import (
    KEY_CURR_FEATURE,
    KEY_FEATURES,
    KEY_LOG_GLUE,
    KEY_LOGGER,
    KEY_PT_HOOKS,
    KEY_MY_HOOKS,
    TEST_CONTEXT,
    LogHelper,
)
from tests.common.pytest_bdd_logger import PytestBddLogger

from pytest_bdd import parsers, given, when, then  # isort:skip

GLUE_LOGGER = logging.getLogger(KEY_LOG_GLUE)

bdd_logger = PytestBddLogger()  # The wanted logger for Pytest BDD

########################
##### Pytest hooks #####
########################


@pytest.hookimpl
def pytest_configure(config: pytest.Config) -> None:
    """
    pytest_configure is a hook provided by the pytest testing framework.
    It is called once during the initialization phase of pytest.
    It allows you to perform custom configuration or setup tasks before the tests are executed.
    """
    print('\n==> pytest_configure 0 ("root"/conftest.py)')

    logging.warning('\n==> pytest_configure 1("root"/conftest.py)')  # <- logged!
    logging.info('\n==> pytest_configure 2("root"/conftest.py)')  # <- not logged! TODO Why ?
    # Configure the logging format
    logging.basicConfig(format='%(message)s', level=logging.WARNING)

    bdd_logger.configure(config)  # TODO Copy content below to bdd_logger.configure ?

    # Set the log level for the root logger
    # logging.getLogger().disabled = True
    # logging.getLogger().getLevel(log_level)

    # root_logger = logging.getLogger()
    default_logger = logging.getLogger(KEY_LOG_GLUE)
    default_logger.disabled = True

    # Check if logging is configured
    # TEST_CONTEXT[KEY_LOGGER] = False
    logger_config = TEST_CONTEXT.get(KEY_LOGGER, None)
    print('* * * * * * * * * * * > logger_config ==', logger_config)

    print(f"Found value: [{logger_config}] in TEST_CONTEXT['logger'] ie. logger_config")
    assert logger_config is None, f'Found value "{logger_config}" in TEST_CONTEXT logger_config'
    assert logger_config is None or isinstance(
        logger_config, bool
    ), 'Found non-bool value in TEST_CONTEXT logger'
    print(f'pytest_configure: {logger_config}')
    logging.warning('pytest_configure: %s', logger_config)
    GLUE_LOGGER.warning('pytest_configure: %s', logger_config)

    # assert logger_config and isinstance(logger_config, bool), 'Found non-bool value:logger_config'
    # GLUE_LOGGER.warning('Found non-bool value: logger_config = %s', logger_config)

    if logger_config is None:
        # Without any logger_config we default to "NullHandler" funcionality
        logger_config = False

    if logger_config is False:
        assert logger_config is False
        # Create a null handler
        null_handler = logging.NullHandler()
        # logging.getLogger().addHandler(null_handler)
        logging.getLogger(KEY_LOG_GLUE).addHandler(null_handler)  # TODO Is both needed?
        # GLUE_LOGGER.setHandlers(null_handler)
        # the_logger = default_logger
    # #
    # TEST_CONTEXT[KEY_LOGGER] = the_logger

    # assert the_logger.name == KEY_LOG_GLUE
    # xlog_msg_start(log_level=WARN)

    # # # Load the logging configuration from the TOML file
    # # with open('logging_config.toml', 'r') as config_file:
    # #     config = tomli.load(config_file)

    # # GLUE_LOGGER.config.dictConfig(config)

    # # Now you can log messages in your module and other modules
    # default_logger = logging.getLogger(__name__)  # Use this logger in your module
    # # logger.info('\n==> pytest_configure ("root"/conftest.py) ' + __name__)

    # # Example log messages
    # default_logger.debug('This is a DEBUG message from your module.')
    # default_logger.warning(__name__)
    GLUE_LOGGER.warning(__name__)
    # logging.warning('This is a WARNING message from logging in "%s" module.', __name__)
    GLUE_LOGGER.warning('This is a WARNING message from GLUE_LOGGER in "%s" module.', __name__)

    # assert False, 'Stopping in func: pytest_configure!'
    # log_msg_end()

# TODO: Is it possible to "monkey patch" step_func and log it's parameters?
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item: Item, nextitem: Optional[Item]) -> bool:
    """
    The pytest_runtest_protocol hook is a powerful hook in pytest
    that allows you to intercept and modify the execution of individual tests.
    It is called for each test item (test function or test class) during the test execution process.
    This hook provides a way to customize the test execution flow, capture test results,
    and perform additional actions before and after each test.
    """
    LogHelper.log_func_call()
    return bdd_logger.runtest_protocol(item, nextitem)
    assert False, 'Stopping in func: pytest_runtest_protocol!'


def is_before_feature_needed(feature: Feature):
    # True if not reported yet?
    return feature.name not in TEST_CONTEXT.get(KEY_FEATURES, [])


@pytest.hookimpl
def pytest_bdd_before_scenario(
    request: FixtureRequest, feature: Feature, scenario: Scenario
) -> None:
    """Called before scenario is executed."""
    # logging.info('%s', '--' * 50)
    LogHelper.log_func_call()
    LogHelper.log_func_name_with_info(feature.name, fillchar='H>')
    # assert False, 'Not supposed to pass this point! pytest_bdd_before_scenario'

    bdd_logger.maybe_log_configuration()

    if is_before_feature_needed(feature):
        logging.info('%s', '1' * 50)
        # logging.info('TEST_CONTEXT: %s', TEST_CONTEXT)
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT1')
        bdd_logger.before_feature(request, feature)
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT2')
        logging.info('%s', '2' * 50)

    current_feature = TEST_CONTEXT.get(KEY_CURR_FEATURE, '-feature not logged-')
    assert (
        current_feature == feature.name
    ), f"Feature name don't match! {current_feature} != {feature.name}"
    # assert False, 'Not supposed to pass this point! pytest_bdd_before_scenario'
    print('bdd_logger.before_scenario called')
    bdd_logger.before_scenario(request, feature, scenario)
    # assert feature.name == 'Debug Off'
    # assert scenario.feature.name == 'Debug Off'
    # log_msg_end()
    # GLUE_LOGGER.info(ret_dict_info(TEST_CONTEXT, '* =====> TEST_CONTEXT'))
    # GLUE_LOGGER.info('%s', '¤' * 50)
    # bdd_logger.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT', 'end')


@pytest.hookimpl
def pytest_bdd_after_scenario(
    request: FixtureRequest, feature: Feature, scenario: Scenario
) -> None:
    """Called after scenario is executed."""
    # TODO: checkif def after_feature is needed
    LogHelper.log_func_call()
    LogHelper.log_func_name_with_info(feature.name, fillchar='H:')

    logging.info(' ----------> pytest_bdd_after_scenario')
    LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT')

    LogHelper.log_func_name_with_info(scenario.name, fillchar='H:')
    bdd_logger.after_scenario(request, feature, scenario)
    # GLUE_LOGGER.info('hook <== %s', ret_func_name())
    # log_msg_end()
    # assert False, 'Not supposed to pass this point! conftest'
    logging.info(' <---------- pytest_bdd_after_scenario')
    LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT')


@pytest.hookimpl
def pytest_bdd_before_step(
    request: FixtureRequest,
    feature: Feature,
    scenario: Scenario,
    step: Step,
    step_func: Callable,
) -> None:
    """Called before step function is set up."""
    LogHelper.log_func_call()
    LogHelper.log_func_name_with_info(step.name, fillchar='->s:')

    # log_msg_start()   # TODO Move call into PytestBddLogger
    bdd_logger.before_step(request, feature, scenario, step, step_func)
    # # "Monkey patching" the glue code
    # GLUE_LOGGER.info('Monkey patching" the glue code')
    # def patched_step_func(*args, **kwargs) -> None:
    #     # Perform any desired actions before the original step function is called
    #     GLUE_LOGGER.info('Parameters:', args, kwargs)
    #     return step_func(*args, **kwargs)

    # return patched_step_func
    # log_msg_end()   # TODO Move call into PytestBddLogger


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(
    request: FixtureRequest,
    feature: Feature,
    scenario: Scenario,
    step: Step,
    step_func: Callable,
    step_func_args: dict[str, Any],
) -> None:
    """Called after step function is successfully executed."""
    LogHelper.log_func_call()
    LogHelper.log_func_name_with_info(step.name, fillchar='<-s:')

    bdd_logger.after_step(request, feature, scenario, step, step_func, step_func_args)


###########################
##### Pytest fixtures #####
###########################

# @pytest.fixture
# def mock_logger() -> None:
#     """
#     mock_logger fixture (in "root" 'conftest.py')
#     Used by tests when needed.
#     """
#     # Fixture setup logic
#     yield logging
#     # Fixture teardown logic


# Using name='cap_log' here instead of just function name "cap_log_fixture".
@pytest.fixture(name='caplog_fixture')  # Using name='caplog_fixture'.
def func_caplog_fixture(caplog: pytest.LogCaptureFixture) -> None:
    LogHelper.log_func_name()
    logging.info('func_caplog_fixture aka. "caplog_fixture" called!')
    yield caplog
    # Perform any necessary cleanup after the test


# Using name='context' here instead of just function name "context".
# Fixes glue warning: "Redefining name 'context' from outer scope".
@pytest.fixture(name='context')
def func_context_fixture() -> dict:
    """
    context fixture (in "root" 'conftest.py')
    Returns an empty dictionary for use by glue code functions
    """
    # ret = {}   # TEST_CONTEXT.copy()
    ret = OrderedDict({'name': 'context'})
    logging.info(
        '\t%screating and returning "context" in %s() ( caller: %s() )!',
        bdd_logger.COL_CONTEXT,
        LogHelper.ret_func_name(),
        LogHelper.ret_func_name(1),
    )
    GLUE_LOGGER.debug('... returning the context fixture (in "root"/conftest.py):')
    GLUE_LOGGER.debug(LogHelper.ret_dict_info(ret, 'context', '<----'))
    return ret


########################
##### Common glue  #####
########################

# # @given(parsers.re('that item "(?P<item>.+?)" is {presence} present'))
# # @given(parsers.parse('that item "{item}" is not present'))
# @given(parsers.parse('that item {item} is {presence} present'))
# def step_impl(item: str, presence: str) -> None:
#     print("step_impl:")
#     print(presence)
#     if presence.strip() == "not":
#         print(f"The item '{item}' is not present in the context")
#     else:
#         print(f"The item '{item}' is present in the context")


@given(parsers.parse('a Pytest-BDD test using the "{module}" module'))
def given_step_using_the_module(context: dict, module: str) -> None:
    GLUE_LOGGER.warning('Given a Pytest-BDD test using the "%s" module', module)
    assert module == KEY_LOG_GLUE, f'Uventet innhold i module: "{module}"'
    logger = logging.getLogger(KEY_LOG_GLUE)
    context[KEY_LOGGER] = logger

    # Set default logger to module name
    # logger = logging.getLogger(KEY_LOG_GLUE)
    logger = logging.getLogger(module)

    logger_name = logger.name
    # print(f"The logger name is: '{logger_name}' now!")
    # GLUE_LOGGER.warning(
    # "The logger name is:     'root' = '%s' [logging.getLogger()]", logging.getLogger().name
    # )
    # GLUE_LOGGER.warning("The logger name is:=  '%s' [get_logger().name]", get_logger().name)
    # GLUE_LOGGER.warning("The logger name is: KEY_LOG_GLUE = '%s' [logger.name]", logger_name)
    assert logger_name == KEY_LOG_GLUE, f'The wanted logger is not in use! Using "{logger_name}"'
    # assert False, 'Stopping in func: given_step_using_the_module'


@given(
    parsers.parse(
        'the "{file_name}" uses Pytest-BDD hooks that calls the corresponding "{module}" functions'
    )
)
def given_file_uses_hooks_that_calls_corresponding_module_func(
    context: dict, file_name: str
) -> None:
    assert context is not None, 'context must be provided!'
    assert file_name is not None or len(file_name) > 0, 'A value for "file_name" was not supplied!'
    assert file_name == 'conftest.py'


# Then information in context "TEST_CONTEXT", will include "Current glue"
# Then information in TEST_CONTEXT will not include "Current glue"
@then(parsers.parse('information in {info_in}, {will} include "{info}"'))
def then_information_about_context_will_include(
    context: dict, info_in: str, will: str, info: str
) -> None:
    assert context is not None, 'context must be provided!'
    assert info_in is not None, 'A value for "info_in" was not supplied!'
    assert info_in in [
        'context',
        'TEST_CONTEXT',
    ], f'Unknown value for "info_in": "{info_in}"'
    assert will is not None, f'"{will}" is not a valid value! (Only "will"/"will not")'
    assert will in [
        'will',
        'will not',
    ], f'"{will}" is not a valid value! (Only "will"/"will not")'
    assert info is not None, f'"{info}" is not a valid value!'
    logging.info('_______________________then_information_about_context_will_include _____________')
    logging.info('information in %s, %sinclude "%s"  ', info_in, will, info)
    logging.warning('information in %s, %sinclude "%s"  ', info_in, will, info)
    # logging.warning('Stopping in func: then_information_about_context_will_include: will=' + will)
    # assert False, 'Stopping in func: then_information_about_context_will_include: will=' + will

    assert will in [
        'will',
        'will not',
    ], f'"{will}" is not a valid value! (Only "will"/"will not")'
    logging.info('information about context ["%s"] %s include "%s"', info_in, will, info)
    the_context = context if info_in == 'context' else TEST_CONTEXT
    LogHelper.log_dict_now(the_context, info_in)
    logging.info(LogHelper.ret_dict_info(the_context, f'* =====> {info_in}', '*__*'))
    # assert context[info] is not None if will == 'will' else None  #TODO


####################################################################################################

def assert_hook_function(ctx_name: str, context: dict) -> None:
    assert ctx_name in ['context', 'TEST_CONTEXT'], f'Unknown value for "ctx_name": "{ctx_name}"'
    ctx = TEST_CONTEXT if ctx_name == 'TEST_CONTEXT' else context
    logged_hooks = ctx.get(KEY_PT_HOOKS, [])
    assert KEY_PT_HOOKS in logged_hooks, f'(assert_hook_function) ... didn\'t find "{KEY_PT_HOOKS}" in {ctx_name}!'


def assert_hook_function2() -> None:
    assert KEY_PT_HOOKS in TEST_CONTEXT, f'(if hock-func) ... didn\'t find "{KEY_PT_HOOKS}" in TEST_CONTEXT**!'
    hooks = TEST_CONTEXT.get(KEY_PT_HOOKS, [])
    assert (hooks.count(func_name) > 0), f"Didn't find '{func_name}' in key \"{KEY_PT_HOOKS}\" in {TEST_CONTEXT[KEY_PT_HOOKS]}!"
    assert False, 'Function not finished yet! (if hoock-func)'

    logged_hooks = TEST_CONTEXT.get(KEY_PT_HOOKS, [])
    assert KEY_PT_HOOKS in logged_hooks, f'(if hock-function) ... didn\'t find "{KEY_PT_HOOKS}" in TEST_CONTEXT!'

    assert len(logged_hooks) > 0, 'No hooks have been logged in TEST_CONTEXT!'


@then(parsers.parse('"{ctx_name}" should show that the {about} "{func_name}" have been run'))
def then_shows_that_function_have_been_run(context: dict, ctx_name: str, about: str, func_name: str) -> None:
    assert LogHelper.assert_string(about)
    assert about in ['hook-function', 'function'], f'"{about}" is not a valid value!'
    assert func_name is not None or len(func_name) > 0, f'"{func_name}" is not a valid value!'
    assert len(func_name) > 0
    msg = f'*************> Then "{ctx_name}" should show that the {about} "{func_name}" have been run'
    logging.info(msg)
    logging.warning('[KEY_PT_HOOKS]: %s', TEST_CONTEXT.get(KEY_PT_HOOKS, []))
    logging.warning('[KEY_MY_HOOKS]: %s', TEST_CONTEXT.get(KEY_MY_HOOKS, []))
    expected_abouts = ['hook-function', 'function']
    assert about in expected_abouts, f'"{about}" is not a valid value!'
    logged_hooks = TEST_CONTEXT.get(KEY_PT_HOOKS, [])
    assert len(logged_hooks) > 0, 'No hooks have beeen logged in TEST_CONTEXT!'
    # if re.search('hook-func', about):
    # assert False, 'Stopping in func: ...function_have_been_run about=' + about.name

    # cases = {
    #     "hook-function": assert_hook_function(ctx_name, context),
    #     # assert False, 'Function not finished yet! (if hock-func)',
    #     "function": lambda: assert KEY_MY_HOOKS in logged_hooks, f'(if hock-func) ... didn\'t find "{KEY_PT_HOOKS}" in TEST_CONTEXT!'
    #     # assert False, 'Function not finished yet! (if hock-func)',
    # }
    # default_case = lambda: process_default_case()

    # # Get the function associated with the value or the default case
    # selected_case = cases.get(value, default_case)

    # # Call the selected case function
    # selected_case()


    if 'hook-function' in about:
        assert (
            KEY_PT_HOOKS in logged_hooks
        ), f'(if hock-function) ... didn\'t find "{KEY_PT_HOOKS}" in TEST_CONTEXT!'
        assert False, 'Function_not_finished_yet! (if hook-function)'
    elif 'function' in about:
        assert (
            KEY_MY_HOOKS in logged_hooks
        ), f'(if hock-func) ... didn\'t find "{KEY_PT_HOOKS}" in TEST_CONTEXT!'
        assert False, 'Function not finished yet! (if hock-func)'
    elif 'function' in about:
        assert (
            KEY_PT_HOOKS in TEST_CONTEXT
        ), f'(if hock-func) ... didn\'t find "{KEY_PT_HOOKS}" in TEST_CONTEXT**!'
        hooks = TEST_CONTEXT.get(KEY_PT_HOOKS, [])
        assert (
            hooks.count(func_name) > 0
        ), f"Didn't find '{func_name}' in key \"{KEY_PT_HOOKS}\" in {TEST_CONTEXT[KEY_PT_HOOKS]}!"
        assert False, 'Function not finished yet! (if hoock-func)'
    else:
        assert False, 'Function not finished yet! Unknown about: ' + about


# @then(parsers.parse('{name} should show that the function {func_name} have been run'))
# def then_shows_that_function_have_been_run_todo(_name: str, _func_name: str) -> None:
#     pass


@when(parsers.parse('"{name}" performs an "{action}"'))
@when(parsers.parse('"{name}" performs another "{action}"'))
def performs_an_action(name: str, action: str) -> None:
    # pylint: disable=unused-argument
    # Add Your Code Here
    # "Dummy" code
    pass
