import logging

logger = logging.getLogger(__name__)

from logging import DEBUG, INFO, WARNING

from tests.common.log_glue import *
from tests.common.log_glue_incl import (  # log_msg_end,
    KEY_DBG_LOG_GLUE,
    TEST_CONTEXT,
    log_msg,
    ret_dict_info,
)

from pytest_bdd import parsers, given, when, then  # isort:skip

# from pytest_bdd.parsers import parse


# Some "globals":
the_when_func_was_called = False   # pylint: disable=invalid-name
stored_context = None   # pylint: disable=invalid-name
EXPECTED_NUM_PARAMS = None  # TODO Implement scenario "Then" step for checking?

##########


@given(parsers.parse('this scenario is tagged with "{tag}"'))
def given_this_scenario_is_tagged_with_wip(tag: str):
    assert tag == 'wip'


@given(parsers.parse('a "{func_name}" Pytest-BDD hook function in conftest.py'))
def pytest_bdd_hook_function_in_conftest_py(context, func_name: str):
    # TODO use TEST_CONTEXT and check if the func_name is in KEY_FUNC
    # log_glue(context=context, func_name=func_name)
    logger.info(func_name)
    logger.info(__file__)
    logger.info(func_name)
    logger.info(ret_dict_info(TEST_CONTEXT, 'dbg =====> TEST_CONTEXT', '*--*'))
    assert func_name == '_pytest_bdd_before_scenario'   ##TODO remove
    called_functions = TEST_CONTEXT.get(KEY_FUNC, False)
    logger.info(called_functions)
    logger.info(called_functions)
    logger.info(called_functions)
    # TODO assert called_functions
    # TODO assert func_name in called_functions
    # xlog_glue_end(context)


@then('I have the hook function {str} declared')
@then('I have the hook function "{hook_function}" declared')
def then_hook_function_declared(context, hook_function):
    pass


@then('it calls the function {str}')
@then('it calls the function "{func_name}"')
def then_function_called(context: dict, func_name: str):
    pass


@given('a glue function without any parameters')
def given_a_glue_function_no_params():
    global EXPECTED_NUM_PARAMS   # pylint: disable=global-statement
    xlog_glue()
    EXPECTED_NUM_PARAMS = 0
    xlog_glue_end()


# @given('a step definition using the {str} fixture')
@given(parsers.parse('a step definition using the "{fixture_name}" fixture'))
def given_step_definiton_using_fixture(context: dict, fixture_name: str):
    # KEY_DBG_LOG_GLUE can be added to log_glue to
    # TODO assert context.get(KEY_DBG_LOG_GLUE, False) is False
    assert fixture_name == 'context'
    xlog_glue(context=context, fixture_name=fixture_name, KEY_DBG_LOG_GLUE=True)
    xlog_glue_end(context)


# @given('a scenario step using the {str} function')
# @given('the step definition is calling the {str} function')
@given(parsers.parse('the step definition is calling the "{func_name}" function'))
def given_scenario_step_func(context: dict, func_name: str):
    xlog_glue(context=context, func_name=func_name)
    assert func_name == 'log_glue'
    xlog_glue_end(context)


@given('the variable "{variable}" is set to "{val}"')
def given_scenario_step_variable(context: dict, variable: str, val: bool):
    global DO_INCL_CURR_INFO   # pylint: disable=global-statement
    xlog_glue(context=context, variable=variable, val=val)
    assert variable == 'DO_INCL_CURR_INFO'
    assert val in ['True', 'False']
    assert val is True or val is False

    context['configured_value_was'] = DO_INCL_CURR_INFO
    if DO_INCL_CURR_INFO is False:
        DO_INCL_CURR_INFO = True

    assert DO_INCL_CURR_INFO == val

    # # Access the current feature attributes
    # logger.debug('Feature Name:        %s', current_feature.name)
    # logger.debug('Feature Description: %s', current_feature.description)
    # logger.debug('Feature Tags:        %s', current_feature.tags)


@given(parsers.parse('I have step definition given a {pstr} parameter'))
def given_i_have_a_step_def_with_context_param(context: dict, pstr: str):
    global stored_context   # pylint: disable=global-statement
    logger.info('Given I have step definition given a context parameter')
    assert context is not None, 'context must be provided'
    assert pstr == 'context'
    xlog_glue(context=context, pstr=pstr)
    stored_context = context
    xlog_glue_end(context)


@given('I have a glue function "{func}" without parameters')
def given_i_have_a_glue_func_no_params(context: dict, func: str):
    xlog_glue(context=context, func=func)
    assert func == 'glue_func_no_params', 'For this test the function name was wrong'
    glue_func_no_params_exist = True
    assert glue_func_no_params_exist

    xlog_glue_end(context)
    logger.info('<Given I have a glue function "glue_func_no_params" without parameters')


@when('I run "pytest -rA -m wip"')
def when_pytest_is_run_wip(context: dict):
    xlog_glue(context=context)
    xlog_glue_end(context)


@then('pytest will execute the tests tagged "@wip"')
def then_pytest_will_execute_the_tests_tagged_wip(context):
    xlog_glue(context=context)
    xlog_glue_end(context)


@then('provide a detailed summary report')
def then_provide_a_detailed_summary_report(context):
    xlog_glue(context=context)
    xlog_glue_end(context)


@then('the "log_glue" function will also display informative texts for the run')
def then_the_log_glue_function_will_also_display_informative_texts(context):
    xlog_glue(context=context)
    xlog_glue_end(context)


@when('"glue_func_no_params" is called by Pytest-BDD')
def glue_func_no_params():
    global the_when_func_was_called   # pylint: disable=global-statement
    logger.debug('When "glue_func_no_params" is calledby Pytest-BDD')
    logger.debug('======================\n>glue_func_no_params()\n======================')
    xlog_glue()
    # log_glue(stored_context=stored_context)
    the_when_func_was_called = True
    # context['called:glue_func_no_params'] = True
    xlog_glue_end(stored_context)


@then('information about the called function should be logged')
def then_information_about_the_called_function_should_be_logged(context):
    xlog_glue(context=context)
    assert the_when_func_was_called, 'The "glue_func_no_params" was not called!'
    # assert False
    xlog_glue_end(context)


@then('hook {str} function execution should be logged')
@given(parsers.parse('hook "{func_name}" function execution should be logged'))
def then_hook_function_execution_should_be_logged(func_name: str):
    assert func_name in TEST_CONTEXT[KEY_HOOKS], f'Hook not called: "{func_name}"'


##################
# from unittest.mock import patch

# def function_to_mock():
#     # Your implementation of the function

# def function_to_test():
#     # Call the function you want to test
#     function_to_mock()

# def test_function_to_test():
#     with patch("__main__.function_to_mock") as mock_function:
#         # Run the test
#         function_to_test()

#         # Assert that the mock function was called
#         mock_function.assert_called_once()
