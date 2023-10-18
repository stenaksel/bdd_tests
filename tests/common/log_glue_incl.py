# content of src/common/log_glue_incl.py
import inspect
import logging
from logging import DEBUG, INFO, WARN
from typing import Any, Callable

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_bdd.parser import Feature, Scenario, ScenarioTemplate, Step

# log_glue related constants:
COL_GLUE = '\033[1;36m'
COL_INFO = '\033[1;34m'
COL_GRAY = '\033[90m'   # \x1b[90m
COL_RESET = '\033[0m'   # TODO Remove reset at log end (in normal logging)
COL_SCENARIO = '\033[1;33m'
COL_STEP = '\033[1;32m'
# COL_ info:
# ANSI escapes always start with \x1b , or \e , or \033 .
# These are all the same thing: they're just various ways
# of inserting the byte 27 into a string.
# If you look at an ASCII table, 0x1b is literally called ESC.

# TODO Use 'KEY_' Prefix for texts being keys
DBG_LOG_PARAMS = 'DBG_LOG_PARAMS'
DO_INCL_CURR_INFO = True   # Do we want to record in context the "current context"?
KEY_STEP_COUNTER = 'step_counter'
KEY_CONTEXT = 'context'
KEY_CURR_FEATURE = 'Current feature'
KEY_CURR_GLUE = 'Current glue'
KEY_CURR_SCENARIO = 'Current scenario'
KEY_CURR_STEP = 'Current step'
KEY_DBG_FUNC_NAME = 'dbg:func_name'
KEY_DBG_LOG_GLUE = 'KEY_DBG_LOG_GLUE'
KEY_DBG_LOGGING = 'dbg_logging'   # TODO: Values: None (=False), False,  True, Hooks (=True), Feature, Scenario, Step
KEY_LOGGER = 'logger'    # TODO Shoujld add all hooks called
KEY_HOOKS = '|Hooks'    # TODO Shoujld add all hooks called
KEY_FUNC = '|Func'      # TODO Shoujld add all glue functions called
# TEST_CONTEXT = {'name': 'TEST_CONTEXT'}
TEST_CONTEXT = {'name': 'TEST_CONTEXT', 'dbg:TEST_CONTEXT': True, 'dbg_logging': False, KEY_LOGGER: logging.getLogger('log_glue')}
test_logger = logging.getLogger('log_glue')
# TEST_CONTEXT = {'unwanted_key': 'unwanted_value'}   # TODO {}


def log_func_name(prev: int = 0, inRow: bool = True, fillchar: str = '#'):  # tested
    assert fillchar != None, f'No fillchar! (Got: None)'
    assert fillchar and len(fillchar) != 0, f"No fillchar! (Got '{fillchar}' <- empty)"
    assert fillchar and len(fillchar) == 1, f"No fillchar! (Got '{fillchar}')"
    caller = ret_func_name(1)
    logging.info(
        "log_func_name(prev=%s, inRow=%s, fillchar='%s') << %s", prev, inRow, fillchar, caller
    )
    logging.debug('(using prev %s)', 1 + prev)

    caller = ret_func_name(1 + prev)
    if inRow:
        log_msg(caller, show_caller=True)
        log_msg('', show_caller=True)
    else:
        name_info = f'  {caller}  '
        # TODO debug:
        logging.debug('Found "%s" (Used prev %s)', name_info, 1 + prev)
        logging.info('%s', fillchar * 75)
        logging.info('%s', name_info.center(75, fillchar))
        logging.info('%s', fillchar * 75)


def log_msg_start(log_level: int = logging.INFO):
    # logging.info('***log_msg_start***')
    TEST_CONTEXT[KEY_DBG_FUNC_NAME] = ret_func_name()   # TODO remove line
    # log_msg(ret_func_name() + ' -> ' + TEST_CONTEXT)
    log_msg(ret_func_name(1), show_caller=not True)
    # logging.log(log_level, 'Heisann!')

    # log_msg(TEST_CONTEXT)
    # log_dict(TEST_CONTEXT, 'TEST_CONTEXT', False)
    # log_func_call_info(log_level, 1, 'INFO')


def log_msg_end(log_level: int = logging.INFO):
    # logging.info('***log_msg_end***')
    log_func_call_info(log_level, 1)


# |           |


def log_func_call_info(
    log_level: int = logging.INFO, prev: int = 0, info: str = '????'
):   # TODO prev: int = 1
    # TODO info -> msg? and first param?
    # logging.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT'))
    caller = ret_func_name(1 + prev)
    log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT', caller + '--> log_func_call_info---->'))
    its_caller = ret_func_name(2 + prev)

    if caller.startswith('pytest_bdd_'):
        its_caller = 'Pytest-BDD'   # TODO Hint: Comment to see the actual function
        if '_before_' in caller:
            info = '==> hook: '
        elif '_after_' in caller:
            info = '<== hook: '
        else:
            assert False, 'Unhandled hook! : ' + caller
    elif caller.startswith('pytest_'):
        its_caller = 'Pytest'
        info = '(== p.t.hook)'
    elif caller.startswith('before_'):
        info = '-->'
    elif caller.startswith('after_'):
        info = '<--'
    else:
        logging.debug('Not overriding the info: %s', info)

    if '==' in info:   # a hook
        logging.log(log_level, '|%s%-19s %s%s| %s', COL_GRAY, its_caller, info, COL_RESET, caller)
        TEST_CONTEXT['dbg:TEST_CONTEXT'] = True
        log_msg('dbg:TEST_CONTEXT:')
    elif '--' in info:   # a hook
        logging.log(log_level, '|%s%-25s %s| %s', COL_GRAY, its_caller, info, caller)
    else:
        logging.log(
            log_level, '|%30s| %s %s(.<< %s)%s', caller, info, COL_GRAY, its_caller, COL_RESET
        )


def log_msg(msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False):
    logging.debug('>> log_msg')
    # DBG_LOG_PARAMS
    if len(msg) == 0:   # only show_caller in first column
        caller = ret_func_name(2)
        msg = f'{pre}{caller}'
        logging.log(log_level, '|%s%30s%s|', COL_SCENARIO, '─' * 30, COL_RESET)
        logging.log(
            log_level, '|%s%30s%s|%s << log_msg', COL_SCENARIO, msg.center(30), COL_RESET, COL_GRAY
        )
        logging.log(log_level, '|%s%30s%s|', COL_SCENARIO, '─' * 30, COL_RESET)
    elif show_caller:
        caller = ret_func_name(1)
        logging.log(log_level, '|%s%21s log_msg:| %s  (<< %s)', COL_GRAY, pre, msg, caller)
    else:
        logging.log(log_level, '%s|%21s log_msg:| %s  ', COL_GRAY, pre, msg)

    if len(msg) == 0 and 'dbg:TEST_CONTEXT' in TEST_CONTEXT:
        logging.info(
            'dbg:TEST_CONTEXT was found in log_msg. Reporting TEST_CONTEXT:'
        )  # TODO: debug
        logging.info(ret_dict_info(TEST_CONTEXT, '* => TEST_CONTEXT'))
        log_dict(TEST_CONTEXT, 'TEST_CONTEXT')
        del TEST_CONTEXT['dbg:TEST_CONTEXT']

    logging.debug('<< log_msg')


def ret_sorted(obj):    # tested
    ret = obj
    if isinstance(obj, dict):
        ret = dict(sorted(obj.items()))
    return ret


def ret_func_name(prev: int = 0) -> str:    # tested
    """
    Usage:
    * ret_func_name() - will return it's own func_name ("the caller of ret_func_name()")
    * ret_func_name(1) - will return the func_name of the caller
    * ret_func_name(2) - will return the func_name of the callers caller
    """
    logging.debug('>> ret_func_name')
    return inspect.stack()[1 + prev][3]


def ret_item_info(name: str, item, prefix: str = 'i') -> str:   # tested
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
        return f'{" " * 8}_{prefix}_{name.rjust(20, " ")} : {item_type:>10}: {item}\n'
        # return f'{prefix}\t{name.rjust(20, " ")} : {item_type:>10}: {item}\n'
        # return f'{prefix}{name:>20} : {item_type:>10}: {item}\n'


def ret_dict_info(the_dict: dict, name: str, prefix: str = '') -> str:  # tested
    """
    Function ret_dict_info returns a string with info
    about the named dictionary and its content
        Param 1: it: dict
        Param 2: name: str
        Param 3: prefix: str (optional)
    """
    assert isinstance(the_dict, dict), 'A dict was not given!'
    the_length = '--EMPTY!'
    if the_dict:   # Some items in the_dict
        the_length = len(the_dict)

    ret = f'{prefix} {name:<15}: [dict] (#={the_length})'
    # the_dict['temp'] = 'hallo'
    show_items = not True
    if show_items and the_dict and the_length != 0:   # Include the items in the_dict
        ret += ret_item_info('____key____', '____value____', prefix)
        ret += ret_item_info('____key____', '____value____', '____')
        for key, value in ret_sorted(the_dict).items():
            ret += ret_item_info(key, value, prefix)
            ret += ret_item_info(key, value)

    log_msg(msg=ret, show_caller=False)
    # log_msg('ret_dict_info() : ', INFO, ret)
    logging.info('ret_dict_info() >> %s ', ret)

    return ret
    # return COL_GRAY + ret + COL_RESET


def log_list(the_list: list, name: str = 'a list') -> None:
    """
    Function log_list will log the items in the list
        Param 1: the_list: list
        Param 2: name: str (optional, default='a list')
    """
    logging.info(name)
    counter = 1
    for element in the_list:
        info = ret_item_info(name=str(counter), item=name)
        counter += 1
        logging.info(info)


def log_dict(the_dict: dict, name: str, incl_items: bool = True) -> None:
    """
    Function log_dict will log the given dict
    and its items when incl_items=True.
        Param 1: the_dict: dict
        Param 2: name: str
        Param 3: incl_items: bool (default: True)
    """
    logging.info('%s', '_' * 50)
    temp = ret_dict_info(the_dict, name, 'log_dict:')
    temp += ' : ' + str(the_dict)
    logging.info(temp)
    logging.info('%s', '_' * 50)


def ret_keys(the_dict: dict) -> str:    # tested
    assert isinstance(the_dict, dict), 'Expected a dictionary'
    assert the_dict, 'Dictionary is empty'
    return ', '.join(list(the_dict.keys()))


def log_configure(config: pytest.Config):
    assert config is not None, 'config is None! "log_configure(None)" makes no sence!'
    logging.info('\n\tpytest first runs hook function "pytest_configure"')
    logging.info('\t(tests might need some custom configuration ...)')
    logging.info('\n==> pytest_configure ("root"/conftest.py)<- only show this informative message')
    logging.info('log_configure ------------------------------------------->')
    # logging.debug(ret_dict_info(TEST_CONTEXT, 'log_configure TEST_CONTEXT', '---->'))


def ret_before_or_after(func_name: str) -> str:   # tested
    assert func_name is not None and len(func_name) > 0, 'No param "func_name"'
    # assert '_' in func_name, 'No _ char found in "func_name". (Expects _)'
    if 'before' in func_name:
        return 'Before'
    elif 'after' in func_name:
        return 'After'

    return ''


def before_feature(_request: FixtureRequest, feature: Feature):
    """
    Pytest-BDD don't have a seperate hook "pytest_bdd_before_feature".
    So this function will be called by pytest_bdd_before_scenario,
    when the first scenario in the feature is run.
    """
    assert feature and feature.name, 'No feature param!'
    assert feature is not None and feature.name != '', 'No feature param!'
    # log_msg('Found feature: ') # + feature.name)
    log_msg_start()
    log_feature(feature)
    log_msg_end()


def assert_object(obj, msg: str):
    assert obj, msg
    if not obj:
        logging.warning('param was not given to assert_object func for msg: %s', msg)
        assert False, msg
    logging.warning('assert_object func with obj: %s', obj)
    logging.warning('assert_object func with msg: %s', msg)
    if 'name!' in msg:
        if not isinstance(obj, str) and obj.hasattr('name'):
            assert len(obj.hasattr('name')) > 0, "No 'name' provided!"
        else:
            if isinstance(obj, str) and len(obj) == 0:
                logging.warning("%s (name = '%s')", msg, obj)
            assert isinstance(obj, str) and len(obj) > 0, msg
        #
    elif 'param!' in msg:
        logging.warning(msg)
        assert not obj, msg
    else:
        logging.warning(f'No check in assert_object for message %s', msg)
        assert False, f'No check in assert_object for message {msg}'


def before_scenario(_request: FixtureRequest, feature: Feature, scenario: Scenario):
    assert feature, 'No feature!'
    logging.info('in before_scenario with feature: %s', feature)
    # assert_object(feature, 'No feature param!4')
    assert_object(feature.name, 'No feature name!')
    assert scenario, 'No scenario param!'
    assert feature is not None and feature.name != '', 'Feature name empty!'
    assert feature and feature.name, 'Feature name empty!'
    global TEST_CONTEXT     # pylint: disable=global-statement
    caller: str = ret_func_name(1)
    log_msg_start()
    assert (
        feature.name and len(feature.name) > 0
    ), 'Det finnes ikke noe feature navn!'    # TODO English
    assert (
        scenario.feature.name and len(scenario.feature.name) > 0
    ), 'Det finnes ikke noe feature navn!'
    assert scenario.name and len(scenario.name) > 0, 'Det finnes ikke noe scenario navn!'
    logging.debug('->          feature.name: %s', feature.name)
    logging.debug('-> scenario.feature.name: %s', scenario.feature.name)

    logging.log(INFO, '|%30s| %s %s(<< %s)', caller, '-' * 55, COL_GRAY, caller)

    log_msg('-' * 55)

    logging.info('|%s', '_' * 65)
    log_scenario(scenario)
    # assert False, 'Stopping!'

    logging.debug('| Feature: %s', scenario.feature.name)
    # logging.info(
    #     '\t%s%s Scenario: %s%s (in Feature: "%s") (<< log_scenario)',  # TODO -> debug
    #     ret_before_or_after(caller),
    #     COL_SCENARIO,
    #     scenario.name,
    #     COL_RESET,
    #     scenario.feature.name,
    # )
    logging.debug('-> scenario.feature.name: %s', scenario.feature.name)
    logging.info('|%s', '-' * 65)

    # log_scenario(scenario)
    log_msg_start()
    log_msg_start()
    # logging.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT'))
    log_msg('----')
    log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT0'))
    log_msg('----')
    log_msg('Resetting TEST_CONTEXT before scenario starts')
    # Reset TEST_CONTEXT before scenario starts
    TEST_CONTEXT = {}
    TEST_CONTEXT[KEY_FUNC] = ['before_scenario (always first)']   # TODO remove: " (always first)"
    TEST_CONTEXT['dbg_log_glue'] = True   # TODO remove line

    logging.info('| TEST_CONTEXT: |')
    log_msg('|TEST_CONTEXT 1: |')
    log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT1'), INFO, '-1-')
    # logging.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT1'))
    log_msg('|TEST_CONTEXT 2: |')
    log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT2'), INFO, '-2-')
    log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT2'))
    log_msg('| TEST_CONTEXT _: |')

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
        logging.debug(ret_dict_info(TEST_CONTEXT, '< log_scenario TEST_CONTEXT'))

    # logging.warning(type(scenario.feature.scenarios[0]))
    # this_info = scenario.feature.scenarios.get('Outline Add numbers <num1> & <num2>')
    # logging.warning('-------------------------------------------')
    # logging.warning(scenario)
    # logging.warning(gherkinScenario)
    # # logging.warning(ret_dict_info('XXX', scenario.feature.scenarios))
    logging.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT3', '<----'))
    logging.info('before_scenario <-------------------------------------------')
    log_msg_end()


def after_scenario(_request: FixtureRequest, _feature: Feature, scenario: Scenario):
    caller: str = ret_func_name(1)
    logging.info(' 1)after_scenario -------------------------------------------> (<< %s)', caller)
    logging.info(ret_dict_info(TEST_CONTEXT, ' 2) TEST_CONTEXT', '---->'))
    logging.info(
        ' 3)\t(after_scenario: TEST_CONTEXT cleanup after scenario ends)'
    )   # TODO information?

    print_prefix = '<== '
    ctx = TEST_CONTEXT
    debug_this = ctx.get('dbg_log_glue', True)   # TODO False
    if debug_this:
        logging.debug('----> Entered after_scenario')

    scenario_name = scenario.name

    if ctx is None:
        logging.info('%s%s => (context: %s)', print_prefix, scenario_name, TEST_CONTEXT)
        logging.info('%s%s => (context: N/A)', print_prefix, scenario_name)
        return
    else:
        logging.info(' => %s context: %s)', scenario_name, ctx)
        logging.info(' => %s context: %s)', scenario_name, ret_dict_info(ctx, 'ctx'))

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
    log_msg_end()


def before_step(
    _request: FixtureRequest,
    _feature: Feature,
    scenario: Scenario,
    step: Step,
    step_func: Callable,
) -> None:
    log_msg_start()
    step_text = f'{step.keyword} {step.name}'
    logging.info('|b.f.step|\t----> before_step(): %s', step_text)
    logging.info('|\t|\tCallable: step_func.__name__ => glue: "%s" ', step_func.__name__)
    logging.info(ret_dict_info(TEST_CONTEXT, 'before_step TEST_CONTEXT', '|\t|\t---->'))
    TEST_CONTEXT[KEY_CURR_GLUE] = step_func.__name__
    log_step(step, scenario)
    logging.info(ret_dict_info(TEST_CONTEXT, 'before_step TEST_CONTEXT', '<----'))
    logging.warning(
        '<---- before_step(): %s <-------------------------------------------', step_text
    )
    log_msg_end()


def after_step(
    _request: FixtureRequest,
    _feature: Feature,
    _scenario: Scenario,
    _step: Step,
    _step_func: Callable,
    step_func_args: dict[str, Any],
) -> None:
    """Handle cleanup after step function is successfully executed."""
    log_msg_start()
    logging.warning('----> Entered after_step')
    logging.warning(ret_dict_info(step_func_args, 'step_func_args'))
    log_msg_end()


def log_feature(feature: Feature) -> None:
    log_msg_start()
    log_func_call_info(WARN, -1, 'HUMBUG')
    # log_func_call_info(info='HUMBUG2')
    # logging.info('|%s', '=' * 75)
    # logging.info('| Feature: %s', feature.name)
    # logging.info('|%s', '=' * 75)
    feature_name = f'Feature: {feature.name}'
    log_func_call_info(WARN, -1, feature_name)
    logging.info('%s', '/' * 75)
    logging.info('|%s|', ' ' * 73)
    logging.info('|%s|', feature_name.center(73))
    logging.info('|%s|', ' ' * 73)
    logging.info('%s', '\\' * 75)
    log_msg_end()


def log_scenario(scenario: Scenario) -> None:
    caller: str = ret_func_name(1)
    logging.info('|%s', '-' * 55)
    log_msg('-' * 55)
    log_msg_start()
    log_msg('-' * 55)
    logging.info('|%s', '"' * 55)

    logging.debug('=> log_scenario(scenario) (<< "%s") ', caller)
    logging.info('|%s', '-' * 75)
    logging.debug('| Feature: %s', scenario.feature.name)
    logging.info(
        '|%s%30s:|%s Scenario: %s%s (in Feature: "%s") (<< log_scenario)%s',  # TODO -> debug
        COL_GRAY,
        ret_before_or_after(caller),
        COL_SCENARIO,
        scenario.name,
        COL_GRAY,
        scenario.feature.name,
        COL_RESET,
    )
    logging.debug('-> scenario.feature.name: %s', scenario.feature.name)
    logging.info('|%s', '-' * 75)


def log_step(step: Step, scenario: Scenario) -> None:
    caller: str = ret_func_name(1)
    logging.info('=> log_step(step, scenario) (<< "%s") ', caller)   # TODO debug
    log_msg_start()
    logging.info('=> log_step(step, scenario) (<< "%s") ', caller)   # TODO debug
    logging.info(
        '\t%s Scenario: %s%s%s (in Feature: "%s") (<< log_step)',  # TODO -> debug
        ret_before_or_after(caller),
        COL_SCENARIO,
        scenario.name,
        COL_RESET,
        scenario.feature.name,
    )
    logging.info(
        '\t%s%s Step: %s %s(<< log_step)%s',  # TODO -> debug
        ret_before_or_after(caller),
        COL_STEP,
        step.name,
        COL_GRAY,
        COL_RESET,
    )

    global TEST_CONTEXT     # pylint: disable=global-statement

    # logging.warning(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT5', '---->'))
    logging.warning('log_step ------------------------------------------->')
    logging.info(ret_dict_info(TEST_CONTEXT, '> log_step TEST_CONTEXT5', ''))

    step_no = TEST_CONTEXT.get(KEY_STEP_COUNTER, 0)
    if step_no == 0:
        logging.warning('\t- %s: %s', KEY_STEP_COUNTER, step_no)

    # logging.info('%sStep:\t"%s"%s', COL_STEP, step.name, COL_RESET)
    logging.info('\t- %s: %s', KEY_STEP_COUNTER, step_no)
    logging.info('\t- step_no     : %s', step_no)
    logging.info('\t- name        : %s', step.name)
    logging.info('\t- type        : %s', step.type)
    logging.info('\t- keyword     : %s', step.keyword)
    logging.info('\t- background  : %s', step.background)
    logging.info('\t- line_number : %s', step.line_number)
    logging.info('\t- lines       : %s', step.lines)
    # logging.debug('\t- lines      : %s', step.lines[0])
    logging.warning('Step Background ------------------------------------------->')
    logging.warning(step.background)
    logging.warning('Step Background <-------------------------------------------')
    logging.info(ret_dict_info(TEST_CONTEXT, '> log_step TEST_CONTEXT', ''))
    assert isinstance(TEST_CONTEXT, dict)
    step_no += 1
    step_text = f'{step.keyword} {step.name}'
    line = '-' * (20 + len(step_text))
    logging.info(line)
    logging.info(ret_before_or_after(caller))
    logging.warning('step_no=%s', step_no)
    logging.info('step_no=%s', step_no)
    logging.warning('step_no=%s', step_no)
    logging.info('step_text=%s', step_text)
    # logging.info(TEST_CONTEXT[KEY_CURR_STEP])
    # Increment the step_counter
    TEST_CONTEXT[KEY_STEP_COUNTER] = step_no
    # Update the step text
    TEST_CONTEXT[KEY_CURR_STEP] = step_text
    TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
    line = '-' * (20 + len(step_text))
    logging.info(line)
    logging.info('Starting on step %s: %s', step_no, step_text)
    logging.info(line)

    logging.warning(
        '\t%s) %s%s %s%s',
        step_no,
        COL_STEP,
        step_text,
        f'{COL_INFO}(@{step.line_number})',
        COL_RESET,
    )
    logging.info('DO_INCL_CURR_INFO=%s', DO_INCL_CURR_INFO)
    if DO_INCL_CURR_INFO:
        assert isinstance(TEST_CONTEXT, dict)
        TEST_CONTEXT[KEY_CURR_STEP] = step_text
        TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
        logging.info(ret_dict_info(TEST_CONTEXT, '< TEST_CONTEXT', ''))

    logging.warning('log_step <-------------------------------------------')


# def after_step(request, feature, scenario, step, step_func, step_func_args):
#     logging.warning('----> Entered after_step')
#     logging.warning(ret_dict_info(step_func_args, 'step_func_args'))


def xlog_glue_end(ctx: dict = None, print_prefix='<== ') -> None:
    if ctx is None:
        ctx = {'dbg_log_glue', True}
    debug_this = ctx.get('dbg_log_glue', True)   # TODO False
    if debug_this:
        logging.debug('----> Entered xlog_glue_end')

    glue_function = inspect.stack()[1][3]
    if ctx is None:
        logging.info('%s%s => (context: N/A)', print_prefix, glue_function)
        logging.info('%s%s => (context: %s)', print_prefix, glue_function, TEST_CONTEXT)
        return
    else:
        logging.info(' => %s context: %s)', glue_function, ctx)
        logging.info(' => %s context: %s)', glue_function, ret_dict_info(ctx, 'ctx'))

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
