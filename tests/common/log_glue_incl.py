# content of src/common/log_glue_incl.py
import inspect
import logging
from typing import Any, Callable

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_bdd.parser import Feature, Scenario, ScenarioTemplate, Step

# log_glue related constants:
COL_GLUE = '\033[1;36m'
COL_INFO = '\033[1;34m'
COL_RESET = '\033[0m'
COL_SCENARIO = '\033[1;33m'
COL_STEP = '\033[1;32m'
# TODO Use 'KEY_' Prefix for texts being keys
DBG_LOG_PARAMS = 'DBG_LOG_PARAMS'
DO_INCL_CURR_INFO = True   # Do we want to record in context the "current context"?
KEY_STEP_COUNTER = 'step_counter'
KEY_CONTEXT = 'context'
KEY_CURR_FEATURE = 'Current feature'
KEY_CURR_GLUE = 'Current glue'
KEY_CURR_SCENARIO = 'Current scenario'
KEY_CURR_STEP = 'Current step'
KEY_DBG_LOG_GLUE = 'KEY_DBG_LOG_GLUE'
KEY_FUNC = '|Func'
TEST_CONTEXT = {'unwanted_key': 'unwanted_value'}   # TODO {}


def ret_sorted(obj):
    ret = obj
    if isinstance(obj, dict):
        ret = dict(sorted(obj.items()))
    return ret


def ret_item_info(name: str, item, prefix: str = 'i') -> str:
    """
    Function ret_item_info returns a string with info
    about the named item, its type and its content
        Param 1: name: str
        Param 2: item
    """
    item_type = f'[{type(item).__name__}]'
    if len(prefix) > 0 and prefix[0] == 'p':   # p => param
        return f'{prefix}\t{name:<20} : {item_type:>10}: {item}\n'
    else:
        return f'{prefix}\t{name.rjust(20, " ")} : {item_type:>10}: {item}\n'
        # return f'{prefix}{name:>20} : {item_type:>10}: {item}\n'


def ret_dict_info(name: str, the_dict: dict, prefix: str = '::') -> str:
    """
    Function ret_dict_info returns a string with info
    about the named dictionary and its content
        Param 1: name: str
        Param 2: it: dict
    """
    assert isinstance(the_dict, dict), 'A dict was not given!'
    the_length = '--EMPTY!'
    if the_dict:
        the_length = len(the_dict)

    ret = f'{prefix} {name:<15}: [dict] (#={the_length})\n\n'

    ret += ret_item_info('____key____', '____value____', '____')
    for key, value in ret_sorted(the_dict).items():
        ret += ret_item_info(key, value)
    return ret


def ret_keys(the_dict: dict) -> str:
    assert isinstance(the_dict, dict), 'Expected a dictionary'
    assert the_dict, 'Dictionary is empty'
    return ', '.join(list(the_dict.keys()))


def log_configure(config: pytest.Config):
    # global TEST_CONTEXT     # pylint: disable=global-statement
    assert config is not None, 'config is None! "log_configure(None)" makes no sence!'
    logging.info('\n\tpytest first runs hook function "pytest_configure"')
    logging.info('\t(tests might need some custom configuration ...)')
    logging.info('\n==> pytest_configure ("root"/conftest.py)<- only show this informative message')
    logging.info('log_configure ------------------------------------------->')
    logging.debug(ret_dict_info('log_configure TEST_CONTEXT', TEST_CONTEXT, '---->'))
    logging.info('\t(Resetting TEST_CONTEXT before scenario starts)')

    # caller: str = inspect.stack()[1][3]
    # log_this_call = f'{caller}->log_configure'
    # # Reset context before scenario starts
    # TEST_CONTEXT = {}
    # TEST_CONTEXT[KEY_FUNC] = ['log_configure']


def log_scenario(scenario: Scenario) -> None:
    caller: str = inspect.stack()[1][3]
    caller_info = ''
    logging.debug('=> log_scenario(scenario) called by: %s ', caller)   # TODO debug
    if caller.endswith('before_scenario'):
        caller_info = 'Before: '

    logging.info(
        '\t%s%sScenario: %s%s (in Feature: %s) (<-- log_scenario)',  # TODO -> debug
        caller_info,
        COL_SCENARIO,
        scenario.name,
        COL_RESET,
        scenario.feature.name,
    )


def before_scenario(_request: FixtureRequest, feature: Feature, scenario: Scenario):
    global TEST_CONTEXT     # pylint: disable=global-statement
    logging.info('before_scenario ------------------------------------------->')
    logging.debug(ret_dict_info('before_scenario TEST_CONTEXT', TEST_CONTEXT, '---->'))
    logging.info('\t(Resetting TEST_CONTEXT before scenario starts)')
    # Reset context before scenario starts
    TEST_CONTEXT = {}
    TEST_CONTEXT[KEY_FUNC] = ['before_scenario']

    logging.debug(ret_dict_info('before_scenario TEST_CONTEXT', TEST_CONTEXT, '---->'))
    if feature.name is not None:
        logging.debug('\t feature : %s', feature.name)
    if scenario.name is not None:
        logging.debug('\t scenario: %s', scenario.name)

    log_scenario(scenario)
    # Inform if the Scenario is created from a Scenario Outline or not
    gherkin_scenario = scenario.feature.scenarios.get(scenario.name)
    assert isinstance(gherkin_scenario, ScenarioTemplate)

    if gherkin_scenario.templated:
        logging.debug('\tScenario is from a Scenario Outline (or Scenario Template)')
    else:
        logging.debug('\tScenario is not from a Scenario Outline')

    if DO_INCL_CURR_INFO:
        assert isinstance(TEST_CONTEXT, dict)
        logging.debug(
            '(DO_INCL_CURR_INFO=%s. Adding %s and %s)',
            DO_INCL_CURR_INFO,
            KEY_CURR_FEATURE,
            KEY_CURR_SCENARIO,
        )
        TEST_CONTEXT[KEY_CURR_FEATURE] = scenario.feature.name
        TEST_CONTEXT[KEY_CURR_SCENARIO] = scenario.name
        TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
        logging.debug(ret_dict_info('< log_scenario TEST_CONTEXT', TEST_CONTEXT))

    # logging.warning(type(scenario.feature.scenarios[0]))
    # this_info = scenario.feature.scenarios.get('Outline Add numbers <num1> & <num2>')
    # logging.warning('-------------------------------------------')
    # logging.warning(scenario)
    # logging.warning(gherkinScenario)
    # # logging.warning(ret_dict_info('XXX', scenario.feature.scenarios))
    logging.info(ret_dict_info('before_scenario TEST_CONTEXT', TEST_CONTEXT, '<----'))
    logging.info('before_scenario <-------------------------------------------')


def after_scenario(_request, _feature, scenario: Scenario):
    print_prefix = '<== '
    ctx = TEST_CONTEXT
    debug_this = ctx.get('dbg_log_glue', True)   # TODO False
    if debug_this:
        logging.debug('----> Entered log_after_scenario')

    scenario_name = scenario.name

    if ctx is None:
        logging.info('%s%s => (context: %s)', print_prefix, scenario_name, TEST_CONTEXT)
        logging.info('%s%s => (context: N/A)', print_prefix, scenario_name)
        return
    else:
        logging.info(' => %s context: %s)', scenario_name, ctx)
        logging.info(' => %s context: %s)', scenario_name, ret_dict_info('ctx', ctx))

    if ctx and ctx.get(KEY_CURR_SCENARIO, False):
        # then remove "recorded" scenario in context
        assert ctx.get(
            KEY_CURR_SCENARIO, DO_INCL_CURR_INFO
        ), f"Couldn't find {KEY_CURR_SCENARIO} in {ctx}"
        popped = ctx.pop(KEY_CURR_SCENARIO, None)
        logging.info(
            'Removed \'%s\' from context (while in "%s%s%s")',
            KEY_CURR_SCENARIO,
            COL_SCENARIO,
            popped,
            COL_RESET,
        )
    else:
        logging.info(
            "(Couldn't find %s in %s%s%s: %s)!",
            KEY_CURR_GLUE,
            COL_GLUE,
            KEY_CONTEXT,
            COL_RESET,
            ctx,
        )

    logging.debug(
        '%s%s%s%s => "end" context: %s', print_prefix, COL_GLUE, scenario_name, COL_RESET, ctx
    )


def before_step(
    _request: FixtureRequest,
    _feature: Feature,
    _scenario: Scenario,
    step: Step,
    step_func: Callable,
) -> None:
    logging.warning(
        '----> before_step(): %s ------------------------------------------->', step.name
    )
    log_step(step)

    logging.warning('glue: %s ------------------------------------------->', step_func.__name__)
    logging.warning(ret_dict_info('TEST_CONTEXT', TEST_CONTEXT, '\t---->'))
    TEST_CONTEXT[KEY_CURR_GLUE] = step_func.__name__
    log_step(step)
    logging.info(ret_dict_info('before_step TEST_CONTEXT', TEST_CONTEXT, '<----'))
    logging.warning(
        '<---- before_step(): %s <-------------------------------------------', step.name
    )


def after_step(
    _request: FixtureRequest,
    _feature: Feature,
    _scenario: Scenario,
    _step: Step,
    _step_func: Callable,
    step_func_args: dict[str, Any],
) -> None:
    """Handle cleanup after step function is successfully executed."""
    logging.warning('----> Entered after_step')
    logging.warning(ret_dict_info('step_func_args', step_func_args))


def log_step(step: Step) -> None:
    global TEST_CONTEXT     # pylint: disable=global-statement
    # logging.warning(ret_dict_info('TEST_CONTEXT', TEST_CONTEXT, '---->'))
    logging.warning('log_step ------------------------------------------->')
    # logging.info('%sStep:\t"%s"%s', COL_STEP, step.name, COL_RESET)
    logging.info('\t- name       : %s', step.name)
    logging.info('\t- type       : %s', step.type)
    logging.info('\t- keyword    : %s', step.keyword)
    # logging.info('\t- background    : %s', step.background)
    logging.info('\t- line_number: %s', step.line_number)
    logging.info('\t- lines      : %s', step.lines)
    # logging.debug('\t- lines      : %s', step.lines[0])
    # logging.warning('Step Background ------------------------------------------->')
    # logging.warning(step.background)
    # logging.warning('Step Background <-------------------------------------------')
    logging.info(ret_dict_info('> log_step TEST_CONTEXT', TEST_CONTEXT, ''))
    # Increment the step_counter
    TEST_CONTEXT[KEY_STEP_COUNTER] = TEST_CONTEXT.get(KEY_STEP_COUNTER, 0) + 1
    logging.info('-------------------------------------------')
    logging.info('Starting on step %s', TEST_CONTEXT[KEY_STEP_COUNTER])
    logging.info('-------------------------------------------')
    curr_step_text = f'{step.keyword} {step.name}'

    logging.warning(
        '\t%s%s %s%s',
        COL_STEP,
        curr_step_text,
        f'{COL_INFO}(@{step.line_number})',
        COL_RESET,
    )
    if DO_INCL_CURR_INFO:
        assert isinstance(TEST_CONTEXT, dict)
        TEST_CONTEXT[KEY_CURR_STEP] = curr_step_text
        TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
        logging.info(ret_dict_info('<before_step TEST_CONTEXT', TEST_CONTEXT, ''))

    logging.warning('log_step <-------------------------------------------')


# def after_step(request, feature, scenario, step, step_func, step_func_args):
#     logging.warning('----> Entered after_step')
#     logging.warning(ret_dict_info('step_func_args', step_func_args))


def log_glue_end(ctx: dict = None, print_prefix='<== ') -> None:
    if ctx is None:
        ctx = {'dbg_log_glue', True}
    debug_this = ctx.get('dbg_log_glue', True)   # TODO False
    if debug_this:
        logging.debug('----> Entered log_glue_end')

    glue_function = inspect.stack()[1][3]
    if ctx is None:
        logging.info('%s%s => (context: N/A)', print_prefix, glue_function)
        logging.info('%s%s => (context: %s)', print_prefix, glue_function, TEST_CONTEXT)
        return
    else:
        logging.info(' => %s context: %s)', glue_function, ctx)
        logging.info(' => %s context: %s)', glue_function, ret_dict_info('ctx', ctx))

    if ctx and ctx.get(KEY_CURR_GLUE, False):
        # then remove "recorded" function in context
        assert ctx.get(KEY_CURR_GLUE, DO_INCL_CURR_INFO), f"Couldn't find {KEY_CURR_GLUE} in {ctx}"
        popped = ctx.pop(KEY_CURR_GLUE, None)
        logging.info(
            'Removed \'%s\' from context (while in "%s%s%s")',
            KEY_CURR_GLUE,
            COL_GLUE,
            popped,
            COL_RESET,
        )
    else:
        logging.info(
            "(Couldn't find %s in %s%s%s: %s)!",
            KEY_CURR_GLUE,
            COL_GLUE,
            KEY_CONTEXT,
            COL_RESET,
            ctx,
        )

    logging.debug(
        '%s%s%s%s => "end" context: %s', print_prefix, COL_GLUE, glue_function, COL_RESET, ctx
    )
