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
from pytest_bdd import parsers, given, when, then  # isort:skip
from typing import Any, Callable, List, Optional

import pytest

# import pytest_bdd.parsers
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Item
from pytest_bdd.parser import Feature, Scenario, Step

# import tomli

from tests.common.log_glue_incl import (
    DBG_LOG_PARAMS,
    KEY_CURR_FEATURE,
    KEY_DBG_LOG_GLUE,
    KEY_LOGGER,
    TEST_CONTEXT,
    after_scenario,
    after_step,
    before_feature,
    before_scenario,
    before_step,
    log_configure,
    log_dict,
    log_func_name,
    log_msg,
    log_msg_end,
    log_msg_start,
    ret_dict_info,
    ret_func_name,
)

NO_LOGGING = True
# from pytest_bdd.parsers import parse




def no_logging() -> bool:
    # return NO_LOGGING  #TODO find out where to find this setting
    return TEST_CONTEXT.get(KEY_DBG_LOG_GLUE, False)


########################
##### Pytest hooks #####
########################

@pytest.hookimpl
def pytest_configure(config: pytest.Config):
    """
    called once at the beginning of test execution.
    pytest_configure is a hook provided by the pytest testing framework in Python.
    It is called during pytest's initialization process and allows you to perform
    custom configuration or setup tasks before the tests are executed.
    """
    print('\n==> pytest_configure ("root"/conftest.py)')
    logging.warning('\n==> pytest_configure ("root"/conftest.py)')
    TEST_CONTEXT[KEY_DBG_LOG_GLUE] = False
    logger = logging.getLogger('log_glue')
    assert logger.name == 'log_glue'

    # if no_logging():
    #     logging.warning('--> no logging !!!')
    #     return

    log_msg_start(log_level=WARN)

    # # Load the logging configuration from the TOML file
    # with open('logging_config.toml', 'r') as config_file:
    #     config = tomli.load(config_file)

    # logging.config.dictConfig(config)

    # Now you can log messages in your module and other modules
    logger = logging.getLogger(__name__)  # Use this logger in your module
    # logger.info('\n==> pytest_configure ("root"/conftest.py) ' + __name__)

    # Example log messages
    logger.debug('This is a DEBUG message from your module.')
    logger.warning(__name__)
    logging.warning(__name__)
    logging.warning('This is a WARNING message from another module.')

    log_configure(config)
    log_msg_end()


# @pytest.hookimpl(tryfirst=True)
# def pytest_before_test(test):
#     print('Before test:', test)


# @pytest.hookimpl(trylast=True)
# def pytest_after_test(test):
#     print('After test:', test)

#

# @hookimpl(wrapper=True)
# def pytest_runtest_protocol(item: Item) -> Generator[None, object, object]:


# TODO: Is it possible to "monkey patch" step_func and log it's parameters?
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item: Item, nextitem: Optional[Item]) -> bool:
    logging.warning(str(item))
    log_msg_start()

    # # Check if the test is a Pytest-BDD step
    # if item.parent and item.parent.name.startswith("Scenario:"):
    #     logging.info('hook => pytest_runtest_protocol\t(in "root" conftest.py)')

    #     # Get the step function from the pytest item
    #    logging.warning('Get the step function from the pytest item (<< pytest_runtest_protocol)')
    #     step_func = item.obj

    #     def patched_step_func(*args, **kwargs):
    #         logging.warning('"Monkey patched" step function (<< pytest_runtest_protocol)')
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
    logging.info('%s', '0' * 50)
    log_func_name(inRow=False)
    # logging.info('%s', '1' * 50)
    # log_func_name(1)
    # logging.info('%s', '2' * 50)
    # log_func_name(2)
    # logging.info('%s', '3' * 50)
    # log_func_call_info()
    # logging.info('%s', '4' * 50)

    log_msg_start()
    # temp = '--temp--'
    # TEST_CONTEXT[KEY_DBG_FUNC_NAME] = 'pytest_bdd_before_scenario'   # TODO remove line
    logging.info('%s', '1' * 50)
    log_dict(TEST_CONTEXT, 'TEST_CONTEXT')
    logging.info('%s', '2' * 50)
    temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    # # temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    # print(temp)
    # print(TEST_CONTEXT)
    # temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    logging.info('%s', '3' * 50)
    logging.info('%s', '¤' * 50)
    logging.warning(temp)
    # temp = ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT')
    log_msg(temp, show_caller=True)
    TEST_CONTEXT['dbg:func_name'] = ret_func_name()   # TODO remove line
    logging.info(ret_dict_info(TEST_CONTEXT, '* ==> TEST_CONTEXT', ' start2'))
    if KEY_CURR_FEATURE not in TEST_CONTEXT:
        before_feature(request, feature)

    before_scenario(request, feature, scenario)
    assert feature.name == 'Debug Off'
    assert scenario.feature.name == 'Debug Off'
    log_msg_end()
    logging.info(ret_dict_info(TEST_CONTEXT, '* =====> TEST_CONTEXT'))
    logging.info('%s', '¤' * 50)


@pytest.hookimpl
def pytest_bdd_after_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario):
    """Called after scenario is executed."""
    log_msg_start()

    after_scenario(request, feature, scenario)
    logging.info('hook <== %s', ret_func_name())
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
    log_msg_start()
    before_step(request, feature, scenario, step, step_func)
    # # "Monkey patching" the glue code
    # logging.info('Monkey patching" the glue code')
    # def patched_step_func(*args, **kwargs):
    #     # Perform any desired actions before the original step function is called
    #     logging.info('Parameters:', args, kwargs)
    #     return step_func(*args, **kwargs)

    # return patched_step_func
    log_msg_end()


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
    log_msg_start()
    logging.info('hook => pytest_bdd_after_step\t(in "root" conftest.py)')
    after_step(request, feature, scenario, step, step_func, step_func_args)
    log_msg_end()


###########################
##### Pytest fixtures #####
###########################

# @pytest.fixture
# def mock_logger():
#     """
#     mock_logger fixture (in "root" 'conftest.py')
#     Used by tests when needed.
#     """
#     # Fixture setup logic
#     yield logging
#     # Fixture teardown logic

# Using name='cap_log' here instead of just function name "cap_log_fixture".
@pytest.fixture(name='caplog_fixture')   # Using name='caplog_fixture'.
def cap_log_fixture(caplog):
    print('cap_log_fixture(caplog) called!')
    yield caplog
    # Perform any necessary cleanup after the test


# Using name='context' here instead of just function name "context_fixture".
# Fixes glue warning: "Redefining name 'context' from outer scope".
@pytest.fixture(name='context')
def context_fixture() -> dict:
    """
    context fixture (in "root" 'conftest.py')
    Returns an empty dictionary for use by glue code functions
    """
    ret = {}   # TEST_CONTEXT.copy()
    logging.debug('... returning the context fixture (in "root"/conftest.py):')
    logging.debug(ret_dict_info(ret, 'context', '<----'))
    return ret


########################
##### Common glue  #####
########################


@given(parsers.parse('a Pytest-BDD test using the "{module}" module'))
def given_step_using_the_module(context: dict, module: str):
    logging.warning('Given a Pytest-BDD test using the "%s" module', module)
    assert module == 'log_glue'
    context[KEY_DBG_LOG_GLUE] = True
    context[DBG_LOG_PARAMS] = True
    logger = logging.getLogger('log_glue')
    context[KEY_LOGGER] = logger

    # Set default logger to module name
    logging.getLogger(module)

    # logger = logging.getLogger(module) #TODO
    logger = logging.getLogger('log_glue')
    logger_name = logger.name
    print(f"The logger name is: {logger_name}")
    logging.warning(f"The logger name is: '%s'", logger_name)


@given(
    parsers.parse(
        'the "{file_name}" uses Pytest-BDD hooks that calls the corresponding "{module}" functions'
    )
)
def given_file_uses_hooks_that_calls_corresponding_module_func(context: dict, file_name: str):
    assert context is not None
    assert file_name is not None or len(file_name) > 0, 'A value for "file_name" was not supplied!'
    assert file_name == 'conftest.py'


# Then information in context "TEST_CONTEXT", will include "Current glue"
# Then information in TEST_CONTEXT will not include "Current glue"
@then(parsers.parse('information in {info_in},{will} include "{info}"'))
def then_information_about_context_will_include(context: dict, info_in: str, will: str, info: str):
    assert context is not None
    assert info_in is not None
    assert will is not None
    assert info is not None
    logging.info('_______________________then_information_about_context_will_include _____________')
    logging.info('information in %s, %sinclude "%s"  ', info_in, will, info)
    assert False, 'Stopped in then_information_about_context_will_include'
    assert will in ['will', 'will not']
    ctx_name = info_in
    if not ctx_name:
        ctx_name = 'context'
    logging.info(
        'information about context ["%s"] %s include "%s"',
        ctx_name,
        will,
        info,
    )
    logging.info(ret_dict_info(context, '* =====>  __context__', '*__*'))
    logging.info(ret_dict_info(TEST_CONTEXT, '* =====> TEST_CONTEXT', '*--*'))
    assert context[info] is not None


# @then(parsers.parse('"{name}" should show that the function "{func_name}" have been run'))
@then(parsers.parse('{name} should show that the function {func_name} have been run'))
def then_shows_that_function_have_been_run_todo(name: str, func_name: str):
    pass


# @then(parsers.parse('{name} should show that the function {func_name} have been run'))
# def then_shows_that_function_have_been_run_todo(_name: str, _func_name: str):
#     pass


@when(parsers.parse('"{name}" performs an "{action}"'))
@when(parsers.parse('"{name}" performs another "{action}"'))
def performs_an_action(name: str, action: str):
    # pylint: disable=unused-argument
    # Add Your Code Here
    pass
