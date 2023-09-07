import logging

from tests.common.log_glue import *
from tests.common.log_glue_incl import KEY_DBG_LOG_GLUE, TEST_CONTEXT, ret_dict_info

from pytest_bdd import parsers, given, when, then   # isort:skip


# Some "globals":
the_when_func_was_called = False   # pylint: disable=invalid-name
stored_context = None   # pylint: disable=invalid-name
EXPECTED_NUM_PARAMS = None


@given('a glue function without any parameters')
def given_a_glue_function_no_params():
    global EXPECTED_NUM_PARAMS   # pylint: disable=global-statement
    xlog_glue()
    EXPECTED_NUM_PARAMS = 0
    xlog_glue_end()


@given('some glue function')
def given_some_glue_function(context: dict):
    xlog_glue(context=context, KEY_DBG_LOG_GLUE=True)
    xlog_glue_end(context)


@given(parsers.parse('at the start of the glue code "{func_name}" function is called'))
def given_step_glue_start(context: dict, func_name: str):
    xlog_glue(context=context, func_name=func_name, KEY_DBG_LOG_GLUE=True)
    assert func_name == 'log_glue'
    xlog_glue_end(context)


# @given('at the end of the glue "{str}" function is called')
@given(parsers.parse('at the end of the glue "{func_name}" function is called'))
def given_step_glue_end(context: dict, func_name: str):
    xlog_glue(context=context, func_name=func_name, KEY_DBG_LOG_GLUE=True)
    assert func_name == 'xlog_glue_end'
    xlog_glue_end(context)


# @given('a step definition using the {str} fixture')
@given(parsers.parse('a step definition using the "{fixture_name}" fixture'))
def given_step_definiton_using_fixture(context: dict, fixture_name: str):
    # KEY_DBG_LOG_GLUE can be added to log_glue to
    # TODO assert context.get(KEY_DBG_LOG_GLUE, False) is False
    xlog_glue(context=context, fixture_name=fixture_name, KEY_DBG_LOG_GLUE=False)
    assert fixture_name == 'context'
    xlog_glue_end(context)


# @given('the step definition is calling the log_glue function')
@given('the step definition is calling the log_glue function')
def given_scenario_step_calling_func(context: dict, func_name: str = 'log_glue'):
    xlog_glue(context=context, func_name=func_name)
    assert func_name == 'log_glue'
    xlog_glue_end(context)


# @given('a scenario step using the {str} function')
# @given('the step definition is calling the {str} function')
@given(parsers.parse('the step definition is calling the "{func_name}" function'))
def given_scenario_step_func(context: dict, func_name: str):
    xlog_glue(context=context, func_name=func_name)
    assert func_name == 'log_glue'
    xlog_glue_end(context)


@given(parsers.parse('I have glue function without any parameters'))
def given_i_have_glue_function_without_any_parameters(context: dict):
    assert context is not None, 'context must be provided'


@given(parsers.parse('I have step definition given a {pstr} parameter'))
def given_i_have_a_step_def_with_context_param(context: dict, pstr: str):
    global stored_context   # pylint: disable=global-statement
    logging.info('Given I have step definition given a context parameter')
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
    logging.info('<Given I have a glue function "glue_func_no_params" without parameters')


@when('the step definition is run')
def when_glue_is_run(context: dict):
    context['dbg_log_glue'] = True
    xlog_glue(context=context)
    xlog_glue_end(context)


@when('_I run "pytest -rA -m wip"')
@when('_you run "pytest -rA -m wip"')
def when_glue_is_run_wip(context: dict):
    xlog_glue(context=context)
    xlog_glue_end(context)


# @then('information about context will include {str} until xlog_glue_end is called')
@then(
    parsers.parse('information about context will include "{info}" until xlog_glue_end is called')
)
def then_information_about_context_will_include(context: dict, info: str):
    xlog_glue(context=context, info=info)
    logging.info('information about context will include "%s" until xlog_glue_end is called', info)
    # logging.warning('===============> TEST_CONTEXT:')
    logging.info(ret_dict_info(TEST_CONTEXT, '* =====> TEST_CONTEXT', '*--*'))
    # logging.warning('===============> context:')
    logging.info(ret_dict_info(context, '* =====>  __context__', '*__*'))
    assert context[info] is not None
    xlog_glue_end(context)


@when('"glue_func_no_params" is called by Pytest-BDD')
def glue_func_no_params():
    global the_when_func_was_called   # pylint: disable=global-statement
    logging.debug('When "glue_func_no_params" is calledby Pytest-BDD')
    logging.debug('======================\n>glue_func_no_params()\n======================')
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


# @then('_hook {str} function execution should be logged')
# @given(parsers.parse('_hook "{func_name}" function execution should be logged'))
# def then_hook_function_execution_should_be_logged(context, func_name: str):
#     # TODO Maybe use global TEST_CONTEXT insted of context
#     global the_when_func_was_called   # pylint: disable=global-statement
#     xlog_glue(context=context, func_name=func_name)
#     the_when_func_was_called = context['called:glue_func_no_params']
#     assert the_when_func_was_called, 'The "glue_func_no_params" was not called!'
#     # assert False
#     xlog_glue_end(context)
