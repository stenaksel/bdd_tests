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
from logging import WARN
from typing import Any, Callable, Optional

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Item
from pytest_bdd.parser import Feature, Scenario, Step

from tests.common.bdd_logger import BddLogger
from tests.common.log_glue_incl import (  # GLUE_LOGGER,
    KEY_CURR_FEATURE,
    KEY_LOG_GLUE,
    KEY_LOGGER,
    TEST_CONTEXT,
    get_logger,
    log_configure,
    log_dict,
    log_func_name,
    log_msg_end,
    log_msg_start,
    old_log_msg,
    ret_dict_info,
    ret_func_name,
)

from pytest_bdd import parsers, given, when, then  # isort:skip


GLUE_LOGGER = logging.getLogger(KEY_LOG_GLUE)

bdd_logger = BddLogger()    # The wanted PytestBddLogger

########################
##### Pytest hooks #####
########################


@pytest.hookimpl
def pytest_configure(config: pytest.Config) -> None:
    """
    called once at the beginning of test execution.
    pytest_configure is a hook provided by the pytest testing framework in Python.
    It is called during pytest's initialization process and allows you to perform
    custom configuration or setup tasks before the tests are executed.
    """
    print('\n==> pytest_configure ("root"/conftest.py)')
    logging.info('\n==> pytest_configure ("root"/conftest.py)')
    logging.warning('\n==> pytest_configure ("root"/conftest.py)')

    # bdd_logger.configure(config)    #TODO Copy content below to bdd_logger

    # Get the log level from the command-line option
    log_level = config.getoption('--log-cli-level')
    logging.warning('pytest_configure config: log_level: %s (command-line option)', log_level)
    print(f'command-line option config: log_level: {log_level}')

    # Get the log level from pyproject.toml
    log_level = config.getini('log_level')
    logging.warning('config: log_level: %s (from pyproject.toml)', log_level)
    print(f'     pyproject.toml config: log_level: {log_level}')

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
        logging.getLogger(KEY_LOG_GLUE).addHandler(null_handler)   # TODO Is both needed?
        # GLUE_LOGGER.setHandlers(null_handler)
        # the_logger = default_logger
    # #
    # TEST_CONTEXT[KEY_LOGGER] = the_logger

    # assert the_logger.name == KEY_LOG_GLUE
    log_msg_start(log_level=WARN)

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
    log_configure(config)
    # log_msg_end()


# @pytest.hookimpl(tryfirst=True)
# def pytest_before_test(test) -> None:
#     print("Before test:", test)


# @pytest.hookimpl(trylast=True)
# def pytest_after_test(test) -> None:
#     print("After test:", test)


# TODO: Is it possible to "monkey patch" step_func and log it's parameters?
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item: Item, nextitem: Optional[Item]) -> bool:
    print('pytest_runtest_protocol: item = ' + str(item))
    print('pytest_runtest_protocol: nextitem = ' + str(nextitem))
    # GLUE_LOGGER.warning('pytest_runtest_protocol: test = %s', str(item))
    log_msg_start()

    # # Check if the test is a Pytest-BDD step
    # if item.parent and item.parent.name.startswith("Scenario:") -> None:
    #     GLUE_LOGGER.info('hook => pytest_runtest_protocol\t(in "root" conftest.py)')

    #     # Get the step function from the pytest item
    #    GLUE_LOGGER.warning('Get the step function from the pytest item (<< pt._runtest_protocol)')
    #     step_func = item.obj

    #     def patched_step_func(*args, **kwargs) -> None:
    #         GLUE_LOGGER.warning('"Monkey patched" step function (<< pytest_runtest_protocol)')
    #         print("Parameters:", args, kwargs)
    #         return step_func(*args, **kwargs)

    #     item.obj = patched_step_func

    log_msg_end()
    return None


@pytest.hookimpl
def pytest_bdd_before_scenario(
    request: FixtureRequest, feature: Feature, scenario: Scenario
) -> None:
    """Called before scenario is executed."""
    logging.info('%s', '0.' * 50)
    log_func_name(inRow=False)
    logging.info('%s', '0.' * 50)
    bdd_logger.log_context_now(TEST_CONTEXT, '* ==> TEST_CONTEXT', 'start1')
    logging.info('%s', '0.' * 50)
    # logging.info('%s', '1.' * 50)
    # log_func_name(1)
    # logging.info('%s', '2.' * 50)
    # log_func_name(2)
    # logging.info('%s', '3.' * 50)
    # log_func_call_info()
    # logging.info('%s', '4.' * 50)

    # log_msg_start()
    # temp = '--temp--'
    # TEST_CONTEXT[KEY_DBG_FUNC_NAME] = 'pytest_bdd_before_scenario'   # TODO remove line
    logging.info('%s', '1.' * 50)
    log_dict(TEST_CONTEXT, 'TEST_CONTEXT')
    logging.info('%s', '2.' * 50)
    temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    # # temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    # print(temp)
    # print(TEST_CONTEXT)
    # temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    logging.info('%s', '3.' * 50)
    logging.info('%s', '¤.' * 50)
    GLUE_LOGGER.warning(temp)
    # temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    old_log_msg(temp, show_caller=True)
    TEST_CONTEXT['dbg:func_name'] = ret_func_name()   # TODO remove line
    # GLUE_LOGGER.info(ret_dict_info(TEST_CONTEXT, '* ==> TEST_CONTEXT', 'start2'))
    bdd_logger.log_context_now(TEST_CONTEXT, '* ==> TEST_CONTEXT', 'end_c')

    if KEY_CURR_FEATURE not in TEST_CONTEXT:
        bdd_logger.before_feature(request, feature)

    bdd_logger.before_scenario(request, feature, scenario)
    # assert feature.name == 'Debug Off'
    # assert scenario.feature.name == 'Debug Off'
    log_msg_end()
    GLUE_LOGGER.info(ret_dict_info(TEST_CONTEXT, '* =====> TEST_CONTEXT'))
    GLUE_LOGGER.info('%s', '¤' * 50)
    bdd_logger.log_context_now(TEST_CONTEXT, '* ==> TEST_CONTEXT', 'end')


@pytest.hookimpl
def pytest_bdd_after_scenario(
    request: FixtureRequest, feature: Feature, scenario: Scenario
) -> None:
    """Called after scenario is executed."""
    log_msg_start()

    bdd_logger.after_scenario(request, feature, scenario)
    GLUE_LOGGER.info('hook <== %s', ret_func_name())
    log_msg_end()


@pytest.hookimpl
def pytest_bdd_before_step(
    request: FixtureRequest,
    feature: Feature,
    scenario: Scenario,
    step: Step,
    step_func: Callable,
) -> None:
    """Called before step function is set up."""
    log_msg_start()   # TODO Move call into BddLogger
    bdd_logger.before_step(request, feature, scenario, step, step_func)
    # # "Monkey patching" the glue code
    # GLUE_LOGGER.info('Monkey patching" the glue code')
    # def patched_step_func(*args, **kwargs) -> None:
    #     # Perform any desired actions before the original step function is called
    #     GLUE_LOGGER.info('Parameters:', args, kwargs)
    #     return step_func(*args, **kwargs)

    # return patched_step_func
    log_msg_end()   # TODO Move call into BddLogger


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
    log_msg_start()   # TODO Move call into BddLogger
    GLUE_LOGGER.info('hook => pytest_bdd_after_step\t(in "root" conftest.py)')
    bdd_logger.after_step(request, feature, scenario, step, step_func, step_func_args)
    log_msg_end()   # TODO Move call into BddLogger


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
@pytest.fixture(name='caplog_fixture')   # Using name='caplog_fixture'.
def func_caplog_fixture(caplog) -> None:
    # print("cap_log_fixture(caplog) called!")
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
    ret = {}   # TEST_CONTEXT.copy()
    GLUE_LOGGER.debug('... returning the context fixture (in "root"/conftest.py):')
    GLUE_LOGGER.debug(ret_dict_info(ret, 'context', '<----'))
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
    return
    assert module == KEY_LOG_GLUE
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
    assert context is not None
    assert file_name is not None or len(file_name) > 0, 'A value for "file_name" was not supplied!'
    assert file_name == 'conftest.py'


# Then information in context "TEST_CONTEXT", will include "Current glue"
# Then information in TEST_CONTEXT will not include "Current glue"
@then(parsers.parse('information in {info_in}, {will} include "{info}"'))
def then_information_about_context_will_include(
    context: dict, info_in: str, will: str, info: str
) -> None:
    assert context is not None
    assert info_in is not None, 'A value for "info_in" was not supplied!'
    assert info_in in ['context', 'TEST_CONTEXT'], f'Unknown value for "info_in": "{info_in}"'
    assert will is not None
    assert will in ['will', 'will not'], f'"{will}" is not a valid value! (Only "will"/"will not")'
    assert info is not None
    logging.info('_______________________then_information_about_context_will_include _____________')
    logging.info('information in %s, %sinclude "%s"  ', info_in, will, info)
    logging.warning('information in %s, %sinclude "%s"  ', info_in, will, info)
    # logging.warning('Stopping in func: then_information_about_context_will_include: will=' + will)
    # assert False, 'Stopping in func: then_information_about_context_will_include: will=' + will

    assert will in ['will', 'will not'], f'"{will}" is not a valid value! (Only "will"/"will not")'
    logging.info('information about context ["%s"] %s include "%s"', info_in, will, info)
    the_context = context if info_in == 'context' else TEST_CONTEXT
    bdd_logger.log_context_now(the_context, info_in)
    logging.info(ret_dict_info(the_context, f'* =====> {info_in}', '*__*'))
    # assert context[info] is not None if will == 'will' else None  #TODO


#

# @then(parsers.parse('"{name}" should show that the function "{func_name}" have been run'))
@then(parsers.parse('{name} should show that the function {func_name} have been run'))
def then_shows_that_function_have_been_run_todo(_name: str, _func_name: str) -> None:
    pass


# @then(parsers.parse('{name} should show that the function {func_name} have been run'))
# def then_shows_that_function_have_been_run_todo(_name: str, _func_name: str) -> None:
#     pass


@when(parsers.parse('"{name}" performs an "{action}"'))
@when(parsers.parse('"{name}" performs another "{action}"'))
def performs_an_action(name: str, action: str) -> None:
    # pylint: disable=unused-argument
    # Add Your Code Here
    pass
