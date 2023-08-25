import logging

from pytest_bdd import given, then, when
from pytest_bdd.parsers import parse

from tests.common.log_glue import *
from tests.common.log_glue_incl import KEY_DBG_LOG_GLUE, TEST_CONTEXT, ret_dict_info

# Some "globals":
the_when_func_was_called = False   # pylint: disable=invalid-name
stored_context = None   # pylint: disable=invalid-name
EXPECTED_NUM_PARAMS = None


@given('a glue function without any parameters')
def given_a_glue_function_no_params():
    global EXPECTED_NUM_PARAMS   # pylint: disable=global-statement
    log_glue()
    EXPECTED_NUM_PARAMS = 0
    log_glue_end()


@given('a glue function')
def given_a_glue_function(context: dict):
    log_glue(context=context, KEY_DBG_LOG_GLUE=True)
    log_glue_end(context)


# @given('at the start of the glue code "{str}" function is called')
@given(parse('at the start of the glue code "{func_name}" function is called'))
def given_step_glue_start(context: dict, func_name: str):
    log_glue(context=context, func_name=func_name, KEY_DBG_LOG_GLUE=True)
    assert func_name == 'log_glue'
    log_glue_end(context)


# @given('at the end of the glue "{str}" function is called')
@given(parse('at the end of the glue "{func_name}" function is called'))
def given_step_glue_end(context: dict, func_name: str):
    log_glue(context=context, func_name=func_name, KEY_DBG_LOG_GLUE=True)
    assert func_name == 'log_glue_end'
    log_glue_end(context)


# @given('a step definition using the {str} fixture')
@given(parse('a step definition using the "{fixture_name}" fixture'))
def given_step_definiton_using_fixture(context: dict, fixture_name: str):
    # KEY_DBG_LOG_GLUE can be added to log_glue to
    # TODO assert context.get(KEY_DBG_LOG_GLUE, False) is False
    log_glue(context=context, fixture_name=fixture_name, KEY_DBG_LOG_GLUE=False)
    assert fixture_name == 'context'
    log_glue_end(context)


# @given('the step definition is calling the log_glue function')
@given('the step definition is calling the log_glue function')
def given_scenario_step_calling_func(context: dict, func_name: str = 'log_glue'):
    log_glue(context=context, func_name=func_name)
    assert func_name == 'log_glue'
    log_glue_end(context)


# @given('a scenario step using the {str} function')
# @given('the step definition is calling the {str} function')
@given(parse('the step definition is calling the "{func_name}" function'))
def given_scenario_step_func(context: dict, func_name: str):
    log_glue(context=context, func_name=func_name)
    assert func_name == 'log_glue'
    log_glue_end(context)


@given('the variable "{variable}" is set to "{val}"')
def given_scenario_step_variable(context: dict, variable: str, val: bool):
    global DO_INCL_CURR_INFO   # pylint: disable=global-statement
    log_glue(context=context, variable=variable, val=val)
    assert variable == 'DO_INCL_CURR_INFO'
    assert val in ['True', 'False']
    assert val is True or val is False

    context['configured_value_was'] = DO_INCL_CURR_INFO
    if DO_INCL_CURR_INFO is False:
        DO_INCL_CURR_INFO = True

    assert DO_INCL_CURR_INFO == val

    # # Access the current feature attributes
    # logging.debug('Feature Name:        %s', current_feature.name)
    # logging.debug('Feature Description: %s', current_feature.description)
    # logging.debug('Feature Tags:        %s', current_feature.tags)


@given(parse('I have step definition given a {pstr} parameter'))
def given_i_have_a_step_def_with_context_param(context: dict, pstr: str):
    global stored_context   # pylint: disable=global-statement
    logging.info('Given I have step definition given a context parameter')
    assert context is not None, 'context must be provided'
    assert pstr == 'context'
    log_glue(context=context, pstr=pstr)
    stored_context = context
    log_glue_end(context)


@given('I have a glue function "{func}" without parameters')
def given_i_have_a_glue_func_no_params(context: dict, func: str):
    log_glue(context=context, func=func)
    assert func == 'glue_func_no_params', 'For this test the function name was wrong'
    glue_func_no_params_exist = True
    assert glue_func_no_params_exist

    log_glue_end(context)
    logging.info('<Given I have a glue function "glue_func_no_params" without parameters')


# @when('the step definition (aka "glue") is run')
@when('the step definition is run')
def when_glue_is_run(context: dict):
    context['dbg_log_glue'] = True
    log_glue(context=context)
    log_glue_end(context)


@when('_I run "pytest -rA -m wip"')
@when('_you run "pytest -rA -m wip"')
def when_glue_is_run_wip(context: dict):
    log_glue(context=context)
    log_glue_end(context)


@then('pytest will execute the tests tagged "@wip"')
def then_pytest_will_execute_the_tests_tagged_wip(context):
    log_glue(context=context)
    log_glue_end(context)


@then('provide a detailed summary report')
def then_provide_a_detailed_summary_report(context):
    log_glue(context=context)
    log_glue_end(context)


@then('the "log_glue" function will also display informative texts for the run')
def then_the_log_glue_function_will_also_display_informative_texts(context):
    log_glue(context=context)
    log_glue_end(context)


# @then('information about context will include {str} until log_glue_end is called')
@then(parse('information about context will include "{info}" until log_glue_end is called'))
def then_information_about_context_will_include(context: dict, info: str):
    log_glue(context=context, info=info)
    logging.info('information about context will include "%s" until log_glue_end is called', info)
    # logging.warning('===============> TEST_CONTEXT:')
    logging.info(ret_dict_info('* =====> TEST_CONTEXT', TEST_CONTEXT, '*--*'))
    # logging.warning('===============> context:')
    logging.info(ret_dict_info('* =====>  __context__', context, '*__*'))
    assert context[info] is not None
    log_glue_end(context)


@when('"glue_func_no_params" is called by pytest-bdd')
def glue_func_no_params():
    global the_when_func_was_called   # pylint: disable=global-statement
    logging.debug('When "glue_func_no_params" is calledby pytest-bdd')
    logging.debug('======================\n>glue_func_no_params()\n======================')
    log_glue()
    # log_glue(stored_context=stored_context)
    the_when_func_was_called = True
    # context['called:glue_func_no_params'] = True
    log_glue_end(stored_context)


@then('information about the called function should be logged')
def then_information_about_the_called_function_should_be_logged(context):
    log_glue(context=context)
    assert the_when_func_was_called, 'The "glue_func_no_params" was not called!'
    # assert False
    log_glue_end(context)


@then('hook {str} function execution should be logged')
@given(parse('hook "{func_name}" function execution should be logged'))
def then_hook_function_execution_should_be_logged(context, func_name: str):
    # TODO Maybe use global TEST_CONTEXT insted of context
    log_glue(context=context, func_name=func_name)
    the_when_func_was_called = context['called:glue_func_no_params']
    assert the_when_func_was_called, 'The "glue_func_no_params" was not called!'
    # assert False
    log_glue_end(context)
