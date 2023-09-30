# content of src/common/log_glue_incl.py
import inspect
import logging
from logging import DEBUG, INFO, WARN, Logger
from typing import Any, Callable, List

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_bdd.parser import Feature, Scenario, ScenarioTemplate, Step

from src.ansi_colors import ANSIColor

# TODO: Create this as a template class

COL_INFO = ANSIColor.BLUE.value
X_COL_RESET = ANSIColor.RESET.value   # TODO Remove reset at log end (in normal logging)
X_COL_SCENARIO = ANSIColor.YELLOW.value
X_COL_STEP = ANSIColor.GREEN.value
COL_CONTEXT = ANSIColor.GRAY.value


# COL_ info:
# ANSI escapes always start with \x1b , or \e , or \033 .
# These are all the same thing: they're just various ways
# of inserting the byte 27 into a string.
# If you look at an ASCII table, 0x1b is literally called ESC.

DO_INCL_CURR_INFO = True   # Do we want to record in context the "current context"?

# TODO Use 'KEY_' Prefix for texts being keys
KEY_CURR_FEATURE = 'Current feature'
KEY_CURR_GLUE = 'Current glue'
KEY_CURR_SCENARIO = 'Current scenario'
KEY_CURR_STEP = 'Current step'
KEY_CONTEXT = 'context'
KEY_DBG_FUNC_NAME = 'dbg:func_name'
KEY_LOG_GLUE = 'log_glue'    # TODO: Values: None (=False), False,  True, Hooks (=True), Feature, Scenario, Step
KEY_LOGGER = 'logger'    # TODO: Values: None (=False), False,  True
KEY_STEP_COUNTER = 'step_counter'
# TEST_CONTEXT = {'unwanted_key': 'unwanted_value'}   # TODO {}
# TEST_CONTEXT = {'name': 'TEST_CONTEXT', KEY_LOGGER: True}
TEST_CONTEXT = {'name': 'TEST_CONTEXT'}
# TEST_CONTEXT = {'name': 'TEST_CONTEXT', 'dbg:TEST_CONTEXT': True, 'dbg_logging': False, KEY_LOGGER: logging.getLogger(KEY_LOG_GLUE)}
GLUE_LOGGER = logging.getLogger(KEY_LOG_GLUE)


def get_logger(name=KEY_LOG_GLUE) -> Logger:    # TODO Is this needed
    """
    Return the configured instances of the Logger class for the passed named logging channel.
    Default = 'log_glue' (KEY_LOG_GLUE)
    """
    return logging.getLogger(name)


def log_headline(
    msg: str, prev: int = 0, inRow: bool = not True, fillchar: str = '#'
) -> None:  # tested
    assert msg != None, f'No message! (Got: None)'
    assert fillchar != None, f'No fillchar! (Got: None)'
    assert fillchar and len(fillchar) == 1, f"No fillchar (len 1)! (Got: '{fillchar}')"
    caller = xret_func_name(1)
    logging.debug(
        "log_headline(msg='%s', prev=%s, inRow=%s, fillchar='%s') << %s",
        msg,
        prev,
        inRow,
        fillchar,
        caller,
    )
    logging.debug('(using prev %s)', 1 + prev)

    caller = xret_func_name(1 + prev)
    if inRow:
        xlog_msg(msg, show_caller=True)
        xlog_msg('', show_caller=True)
    else:
        name_info = f'  {msg}  '
        # TODO debug:
        logging.debug('Found "%s" (Used prev %s)', name_info, 1 + prev)
        ###########################################################################
        ###########################################################################
        logging.info('\t%s', fillchar * 75)
        logging.info('\t%s', name_info.center(75, fillchar))
        logging.info('\t%s', fillchar * 75)


def xlog_func_name(prev: int = 0, inRow: bool = True, fillchar: str = '#') -> None:  # tested
    assert fillchar != None, f'No fillchar! (Got: None)'
    assert fillchar and len(fillchar) != 0, f"No fillchar! (Got '{fillchar}' <- empty)"
    assert fillchar and len(fillchar) == 1, f"No fillchar! (Got string '{fillchar}')"
    caller = xret_func_name(1)
    logging.info(
        "%slog_func_name(prev=%s, inRow=%s, fillchar='%s') %s<< %s",
        COL_INFO,
        prev,
        inRow,
        fillchar,
        COL_CONTEXT,
        caller,
    )
    logging.debug('(using prev %s)', 1 + prev)

    caller = xret_func_name(1 + prev)
    log_headline(caller, prev, inRow, fillchar)


def xlog_msg_start(log_level: int = logging.INFO) -> None:
    # logging.info('>> ***xlog_msg_start***')
    # print('***xlog_msg_start***')
    # print(__name__)
    # print('***xlog_msg_start***')
    GLUE_LOGGER.warning('***xlog_msg_start*** - %s', __name__)
    GLUE_LOGGER.log(log_level, '***xlog_msg_start*** - %s', __name__)
    TEST_CONTEXT[KEY_DBG_FUNC_NAME] = xret_func_name()   # TODO remove line
    # xlog_msg(xret_func_name() + ' -> ' + TEST_CONTEXT)
    xlog_msg(xret_func_name(1), show_caller=True)
    # GLUE_LOGGER.log(log_level, 'Heisann!')

    # xlog_msg(TEST_CONTEXT)
    # log_dict(TEST_CONTEXT, 'TEST_CONTEXT', False)
    # log_func_call_info(log_level, 1, 'INFO')
    logging.warning('<< ***xlog_msg_start***')


def log_msg_end(log_level: int = logging.INFO) -> None:
    # GLUE_LOGGER.info('***log_msg_end***')
    log_func_call_info(log_level, 1)


# |           |


def log_func_call_info(
    log_level: int = logging.INFO, prev: int = 0, info: str = '????'
) -> None:   # TODO prev: int = 1
    # TODO info -> msg? and first param?
    # GLUE_LOGGER.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT'))
    caller = xret_func_name(1 + prev)
    # xlog_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT', caller + '--> log_func_call_info---->'))
    its_caller = xret_func_name(2 + prev)

    if caller.startswith('pytest_bdd_'):
        its_caller = 'Pytest-BDD'   # TODO Hint: Comment to see the actual function
        if '_before_' in caller:
            info = '==> hook: '
        elif '_after_' in caller:
            info = '<== hook: '
        else:
            assert False, f'Stopping in func: log_func_call_info, unhandled hook! ({caller})'
    elif caller.startswith('pytest_'):
        its_caller = 'Pytest'
        info = '(== p.t.hook)'
    elif caller.startswith('before_'):
        info = '-->'
    elif caller.startswith('after_'):
        info = '<--'
    else:
        GLUE_LOGGER.debug('Not overriding the info: %s', info)

    if '==' in info:   # a hook
        GLUE_LOGGER.log(
            log_level, '|%s%-19s %s%s| %s', COL_CONTEXT, its_caller, info, X_COL_RESET, caller
        )
        TEST_CONTEXT['dbg:TEST_CONTEXT'] = True
        xlog_msg('dbg:TEST_CONTEXT = True')
    elif '--' in info:   # a hook
        GLUE_LOGGER.log(log_level, '|%s%-25s %s| %s', COL_CONTEXT, its_caller, info, caller)
    else:
        GLUE_LOGGER.log(
            log_level, '|%30s| %s %s(.<< %s)%s', caller, info, COL_CONTEXT, its_caller, X_COL_RESET
        )


def xlog_msg(
    msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False
) -> None:
    caller = xret_func_name(1)
    # logging.info('-> xlog_msg -> ' + msg)
    logging.info('xlog:|%s %s  %s(<< %s)', pre, msg, COL_CONTEXT, caller)
    # print('-> xlog_msg <- ' + caller)

    GLUE_LOGGER.debug('>> xlog_msg')
    if len(msg) == 0:   # only show_caller in first column
        caller = xret_func_name(2)
        msg = f'{pre}{caller}'
        GLUE_LOGGER.log(log_level, '|%s%30s%s|', X_COL_SCENARIO, '─' * 30, X_COL_RESET)
        GLUE_LOGGER.log(
            log_level,
            '|%s%30s%s|%s << xlog_msg',
            X_COL_SCENARIO,
            msg.center(30),
            X_COL_RESET,
            COL_CONTEXT,
        )
        GLUE_LOGGER.log(log_level, '|%s%30s%s|', X_COL_SCENARIO, '─' * 30, X_COL_RESET)
    elif show_caller:
        caller = xret_func_name(1)
        GLUE_LOGGER.log(
            log_level, '|%s%21s xlog_msg:| %s  (<< %s)', COL_CONTEXT, pre, msg, caller
        )
    else:
        GLUE_LOGGER.log(log_level, '%s|%21s xlog_msg:| %s  ', COL_CONTEXT, pre, msg)

    if len(msg) == 0 and 'dbg:TEST_CONTEXT' in TEST_CONTEXT:
        GLUE_LOGGER.info(
            'dbg:TEST_CONTEXT was found in xlog_msg. Reporting TEST_CONTEXT:'
        )  # TODO: debug
        GLUE_LOGGER.info(old_ret_dict_info(TEST_CONTEXT, '* => TEST_CONTEXT'))
        # log_dict(TEST_CONTEXT, 'TEST_CONTEXT')
        del TEST_CONTEXT['dbg:TEST_CONTEXT']

    GLUE_LOGGER.debug('<< xlog_msg')


def xret_sorted(obj) -> Any:    # tested
    ret = obj
    if isinstance(obj, dict):
        ret = dict(sorted(obj.items()))
    return ret


# def ret_func_name(prev: int = 0) -> str:    # tested
#     """
#     Usage:
#     * ret_func_name() - will return it's own func_name ("the caller of ret_func_name()")
#     * ret_func_name(1) - will return the func_name of the caller
#     * ret_func_name(2) - will return the func_name of the callers caller
#     """
#     GLUE_LOGGER.debug('>> ret_func_name')
#     return inspect.stack()[1 + prev][3]


def xret_func_name(prev: int = 0) -> str:    # tested
    """
    Usage:
    * xret_func_name() - will return it's own func_name ("the caller of xret_func_name()")
    * xret_func_name(1) - will return the func_name of the caller
    * xret_func_name(2) - will return the func_name of the callers caller
    """
    assert isinstance(prev, int), f'Not a valid prev! (Got: {prev})'
    # assert prev >= 0, f'Not a valid prev! (Got: {prev})'
    # assert prev < 2, f'Not a valid prev! (Got: {prev})' # TODO: fix this
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    assert isinstance(prev, int), f'Not a valid prev from {caller_name}! (Got: {prev})'
    if prev == 0:
        return caller_name

    caller_frame = caller_frame.f_back
    caller_name = caller_frame.f_code.co_name
    if prev == 1:
        return caller_name

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
        return f'{prefix:>8}-{name:<20}-: {item_type:>10}: {item}'
    else:
        return f'{"." * 8}{prefix:>8}{name.rjust(25, " ")}_ : {item_type:>10}: {item}'
        # return f'{prefix}\t{name.rjust(20, " ")} : {item_type:>10}: {item}'
        # return f'{prefix}{name:>20} : {item_type:>10}: {item}'


def old_ret_dict_info(the_dict: dict, name: str, prefix: str = '') -> str:  # tested
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

    ret = f'{prefix} {name:<15}: [dict] (#={the_length})\n'
    # the_dict['temp'] = 'hallo'
    show_items = True
    if show_items and the_dict and the_length != 0:   # Include the items in the_dict
        ret += ret_item_info('____key____', '____value____', '_item_') + '\n'
        inum = 1

    for key, value in xret_sorted(the_dict).items():
        # ret += ret_item_info(key, value, prefix) + '\n'
        ret += ret_item_info(key, value, f'i {inum}') + '\n'
        inum = inum + 1

    xlog_msg(msg=ret, show_caller=False)
    # xlog_msg('ret_dict_info() : ', INFO, ret)
    GLUE_LOGGER.info('ret_dict_info() >> %s ', ret)
    logging.warning('%sret_dict_info() >> %s ', COL_CONTEXT, ret)

    # return ret
    return str(COL_INFO) + ret + str(X_COL_RESET)


def log_list(the_list: list, name: str = 'a list') -> None:
    """
    Function log_list will log the items in the list
        Param 1: the_list: list
        Param 2: name: str (optional, default='a list')
    """
    GLUE_LOGGER.info(name)
    counter = 1
    for element in the_list:
        info = ret_item_info(name=str(counter), item=name) + '\n'
        counter += 1
        GLUE_LOGGER.info(info)


def ret_keys(the_dict: dict) -> str:    # tested
    assert isinstance(the_dict, dict), 'Expected a dictionary'
    assert the_dict, 'Dictionary is empty'
    return ', '.join(list(the_dict.keys()))


def ret_before_or_after(func_name: str) -> str:   # tested
    assert func_name is not None and len(func_name) > 0, 'No param "func_name"'
    # assert '_' in func_name, 'No _ char found in "func_name". (Expects _)'
    if 'before' in func_name:
        return 'Before'
    elif 'after' in func_name:
        return 'After'

    return ''


def assert_object(obj, msg: str) -> None:
    assert obj, msg
    if not obj:
        GLUE_LOGGER.warning('param was not given to assert_object func for msg: %s', msg)
        assert False, msg
    GLUE_LOGGER.warning('assert_object func with obj: %s', obj)
    GLUE_LOGGER.warning('assert_object func with msg: %s', msg)
    if 'name!' in msg:
        if not isinstance(obj, str) and obj.hasattr('name'):
            assert len(obj.hasattr('name')) > 0, "No 'name' provided!"
        else:
            if isinstance(obj, str) and len(obj) == 0:
                GLUE_LOGGER.warning("%s (name = '%s')", msg, obj)
            assert isinstance(obj, str) and len(obj) > 0, msg
        #
    elif 'param!' in msg:
        GLUE_LOGGER.warning(msg)
        assert not obj, msg
    else:
        GLUE_LOGGER.warning(f'No check in assert_object for message %s', msg)
        assert False, f'No check in assert_object for message {msg}'


def xlog_feature(feature: Feature) -> None:
    xlog_msg_start()
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


def xlog_scenario(scenario: Scenario) -> None:
    caller: str = xret_func_name(1)
    GLUE_LOGGER.info('|%s', '-' * 55)
    xlog_msg('-' * 55)
    xlog_msg_start()
    xlog_msg('-' * 55)
    GLUE_LOGGER.info('|%s', '"' * 55)

    GLUE_LOGGER.debug('=> xlog_scenario(scenario) (<< "%s") ', caller)
    GLUE_LOGGER.info('|%s', '-' * 75)
    GLUE_LOGGER.debug('| Feature: %s', scenario.feature.name)
    GLUE_LOGGER.info(
        '|%s%30s:|%s Scenario: %s%s (in Feature: "%s") (<< xlog_scenario)',  # TODO -> debug
        COL_CONTEXT,
        ret_before_or_after(caller),
        X_COL_SCENARIO,
        scenario.name,
        COL_CONTEXT,
        scenario.feature.name,
    )
    GLUE_LOGGER.debug('-> scenario.feature.name: %s', scenario.feature.name)
    GLUE_LOGGER.info('|%s', '-' * 75)


def log_step(step: Step, scenario: Scenario) -> None:
    caller: str = xret_func_name(1)
    GLUE_LOGGER.info('=> log_step(step, scenario) (<< "%s") ', caller)   # TODO debug
    xlog_msg_start()
    GLUE_LOGGER.info('=> log_step(step, scenario) (<< "%s") ', caller)   # TODO debug
    GLUE_LOGGER.info(
        '\t%s Scenario: %s%s%s (in Feature: "%s") (<< log_step)',  # TODO -> debug
        ret_before_or_after(caller),
        X_COL_SCENARIO,
        scenario.name,
        COL_CONTEXT,
        scenario.feature.name,
    )
    GLUE_LOGGER.info(
        '\t%s%s Step: %s %s(<< log_step)',  # TODO -> debug
        ret_before_or_after(caller),
        X_COL_STEP,
        step.name,
        COL_CONTEXT,
    )

    global TEST_CONTEXT     # pylint: disable=global-statement

    # GLUE_LOGGER.warning(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT5', '---->'))
    GLUE_LOGGER.warning('log_step ------------------------------------------->')
    GLUE_LOGGER.info(old_ret_dict_info(TEST_CONTEXT, '> log_step TEST_CONTEXT5', ''))

    step_no = TEST_CONTEXT.get(KEY_STEP_COUNTER, 0)
    if step_no == 0:
        GLUE_LOGGER.warning('\t- %s: %s', KEY_STEP_COUNTER, step_no)

    # GLUE_LOGGER.info('%sStep:\t"%s"', X_COL_STEP, step.name)
    GLUE_LOGGER.info('\t- %s: %s', KEY_STEP_COUNTER, step_no)
    GLUE_LOGGER.info('\t- step_no     : %s', step_no)
    GLUE_LOGGER.info('\t- name        : %s', step.name)
    GLUE_LOGGER.info('\t- type        : %s', step.type)
    GLUE_LOGGER.info('\t- keyword     : %s', step.keyword)
    if step.background:
        # GLUE_LOGGER.info('\t- background  : %s', step.background)
        GLUE_LOGGER.info('\t- background  : -yes-')
    else:
        GLUE_LOGGER.info('\t- background  : -NO-')
    GLUE_LOGGER.info('\t- line_number : %s', step.line_number)
    GLUE_LOGGER.info('\t- lines       : %s', step.lines)
    # GLUE_LOGGER.debug('\t- lines      : %s', step.lines[0])
    GLUE_LOGGER.warning('Step Background >>#######################################>>')
    GLUE_LOGGER.warning(step.background)
    GLUE_LOGGER.warning('Step Background <<#######################################<<')
    GLUE_LOGGER.info(old_ret_dict_info(TEST_CONTEXT, '> log_step TEST_CONTEXT', ''))
    assert isinstance(TEST_CONTEXT, dict)
    step_no += 1
    step_text = f'{step.keyword} {step.name}'
    line = '-' * (20 + len(step_text))
    GLUE_LOGGER.info(line)
    GLUE_LOGGER.info(ret_before_or_after(caller))
    GLUE_LOGGER.warning('step_no=%s', step_no)
    GLUE_LOGGER.info('step_no=%s', step_no)
    GLUE_LOGGER.warning('step_no=%s', step_no)
    GLUE_LOGGER.info('step_text=%s', step_text)
    # GLUE_LOGGER.info(TEST_CONTEXT[KEY_CURR_STEP])
    # Increment the step_counter
    TEST_CONTEXT[KEY_STEP_COUNTER] = step_no
    # Update the step text
    TEST_CONTEXT[KEY_CURR_STEP] = step_text
    TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
    line = '-' * (20 + len(step_text))
    GLUE_LOGGER.info(line)
    GLUE_LOGGER.info('Starting on step %s: %s', step_no, step_text)
    GLUE_LOGGER.info(line)

    GLUE_LOGGER.warning(
        '\t%s) %s%s %s',
        step_no,
        X_COL_STEP,
        step_text,
        f'{COL_INFO}(@{step.line_number})',
    )
    GLUE_LOGGER.info('DO_INCL_CURR_INFO=%s', DO_INCL_CURR_INFO)
    if DO_INCL_CURR_INFO:
        assert isinstance(TEST_CONTEXT, dict)
        TEST_CONTEXT[KEY_CURR_STEP] = step_text
        TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
        GLUE_LOGGER.info(old_ret_dict_info(TEST_CONTEXT, '< TEST_CONTEXT', ''))

    GLUE_LOGGER.warning('log_step <-------------------------------------------')


# def after_step(request, feature, scenario, step, step_func, step_func_args) -> None:
#     GLUE_LOGGER.warning('----> Entered after_step')
#     GLUE_LOGGER.warning(ret_dict_info(step_func_args, 'step_func_args'))


def assert_messages(caplog, level, messages: List = [], in_sequence: bool = False) -> None:
    print('#### messages:')
    for msg in messages:
        print(msg)
    # Access the captured log records based on log level
    filtered_records = [record for record in caplog.records if record.levelno == level]
    messages_found = []
    lines: List[int] = []
    rest = messages.copy()

    for record in filtered_records:
        assert isinstance(record, logging.LogRecord)
        # Inspect and assert the log records as needed
        for msg in rest:
            print('\nmsg: ' + msg)
            assert record.levelno == level, f'record.levelname = {record.levelname}'
            if msg in record.message:
                print('\nSeeked&found: ' + msg)
                messages_found += [msg]
                lines += [record.lineno]
                print('#### found messages:')
                print(messages_found)
                break
            else:
                print("\n Didn't find: " + msg)

            print('#### found message lines:')
            print(lines)
            #
        #
        print('#### rest messages before:')
        print(rest)
        print('#### messages_found messages before:')
        print(messages_found)
        rest = [message for message in rest if message not in messages_found]
        # print("#### found messages:")
        # print(messages_found)
        print('#### rest messages after:')
        print(rest)
    #

    # print("#### rest messages (in end):")
    print(rest)
    level_name = logging.getLevelName(level)
    assert len(rest) == 0, f"Couldn't find wanted {level_name} log messages: {rest}"
    assert not rest, f"Couldn't find wanted {level_name} log messages: {rest}"
