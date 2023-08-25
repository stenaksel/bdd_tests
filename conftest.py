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
from typing import Any, Callable

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_bdd import given
from pytest_bdd.parser import Feature, Scenario, Step
from pytest_bdd.parsers import parse

from tests.common.log_glue import log_glue, log_glue_end  # TODO move to _incl?
from tests.common.log_glue_incl import (
    DBG_LOG_PARAMS,
    KEY_DBG_LOG_GLUE,
    after_scenario,
    after_step,
    before_scenario,
    before_step,
    log_configure,
    ret_dict_info,
)


# TODO ? @pytest.hookimpl
def pytest_configure(config: pytest.Config):
    """
    called once at the beginning of test execution.
    pytest_configure is a hook provided by the pytest testing framework in Python.
    It is called during pytest's initialization process and allows you to perform
    custom configuration or setup tasks before the tests are executed.
    """
    logging.info('\n==> pytest_configure ("root"/conftest.py)')
    log_configure(config)


########################
##### Pytest hooks #####
########################


@pytest.hookimpl
def pytest_bdd_before_scenario(
    request: FixtureRequest, feature: Feature, scenario: Scenario
) -> None:
    """Called before scenario is executed."""
    logging.info('hook => pytest_bdd_before_scenario\t(in "root" conftest.py)')
    before_scenario(request, feature, scenario)


@pytest.hookimpl
def pytest_bdd_after_scenario(request, feature, scenario: Scenario):
    """Called after scenario is executed."""
    logging.info('hook => pytest_bdd_after_scenario\t(in "root" conftest.py)')
    after_scenario(request, feature, scenario)


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
    logging.info('hook => pytest_bdd_after_step\t(in "root" conftest.py)')
    after_step(request, feature, scenario, step, step_func, step_func_args)


@pytest.hookimpl
def pytest_bdd_before_step(
    request: FixtureRequest,
    feature: Feature,
    scenario: Scenario,
    step: Step,
    step_func: Callable,
) -> None:
    """Called before step function is set up."""
    logging.info('hook => pytest_bdd_before_step\t(in "root" conftest.py)')
    before_step(request, feature, scenario, step, step_func)


@pytest.fixture
def context() -> dict:
    """
    context fixture (in "root" 'conftest.py')
    Returns an empty dictionary for use by glue code functions
    """
    ret = {}   # TEST_CONTEXT.copy()
    logging.debug('... returning the context fixture (in "root"/conftest.py):')
    logging.debug(ret_dict_info('context', ret, '<----'))

    return ret


########################
##### Common glue  #####
########################

# @given('a pytest-bdd test using the {module} module')
@given(parse('a pytest-bdd test using the "{module}" module'))
def given_step_using_the_module(context: dict, module: str):
    context[KEY_DBG_LOG_GLUE] = True
    context[DBG_LOG_PARAMS] = True
    log_glue(context=context, module=module)
    assert module == 'log_glue'
    log_glue_end(context)


@given('the {str} uses hooks that calls the corresponding log_glue function')
@given(parse('the "{file_name}" uses hooks that calls the corresponding log_glue function'))
def given_hooks_call_corresponding_function(context: dict, file_name: str):
    pass
