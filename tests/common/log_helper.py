# log_helper.py
import inspect
import logging
from collections import OrderedDict
from typing import Any, List

from pytest import FixtureRequest
from pytest_bdd.parser import Feature, Scenario, Step

from src.ansi_colors import ANSIColor

# from tests.common.pytest_bdd_logger_interface import (
#     TEST_CONTEXT
# )


# COL_GLUE = '\033[1;36m'
COL_INFO = ANSIColor.BLUE.value
COL_MSG = ANSIColor.CYAN.value
COL_RESET = ANSIColor.RESET.value
COL_SCENARIO = ANSIColor.YELLOW.value
COL_STEP = ANSIColor.GREEN.value
COL_CONTEXT = ANSIColor.GRAY.value
COL_DBG = ANSIColor.DBG.value  # TODO Remove DBG color

DO_INCL_CURR_INFO = True

# TEST_CONTEXT = {'name': 'TEST_CONTEXT'}
TEST_CONTEXT = OrderedDict(
    {'name': 'TEST_CONTEXT', 'LOG_CONFIG': False, '|Hooks': []}
)   # TODO "LOG_CONFIG": True
# Constants used for items in TEST_CONTEXT:
KEY_CURR_FEATURE = 'Current feature'
KEY_CURR_GLUE = 'Current glue'
KEY_CURR_SCENARIO = 'Current scenario'
KEY_CURR_STEP = 'Current step'
KEY_STEP_COUNTER = 'step_counter'
KEY_DBG_FUNC_NAME = 'dbg:func_name'
KEY_LOG_GLUE = 'log_glue'  # TODO: Values:False, True, Hooks (=True), Feature, Scenario, Step
KEY_DBG_LOGGING = 'dbg_logging'  # TODO: Values: None, False,  True, Hooks, Feature, Scenario, Step
KEY_DBG_LOG_GLUE = 'KEY_DBG_LOG_GLUE'
KEY_LOGGER = 'logger'  # TODO: Values: False,  True

KEY_LOG_CONFIG = 'LOG_CONFIG'   # Boolean for calling log_configuration or not (default true)
KEY_CONFIG = 'config'
KEY_FUNC = '|Func'  # TODO Should add all glue functions that gets called
KEY_HOOKS = '|Hooks'  # TODO Should add all hooks that gets called
KEY_FEATURES = '|Features'  # TODO Should add features in play and reported (by before_feature)


def _ret_item_info(name: str, item, prefix: str = 'i') -> str:
    """
    Function ret_item_info returns a string with info
    about the named item, its type and its content
        Param 1: name: str
        Param 2: item
    """
    item_type = f'[{type(item).__name__}]' if not '_key_' in name else '_type_'
    key_info = (
        '{name:<20}' if prefix and prefix[0] == 'p' else f'{name.rjust(20, " ")}'
    )  # TODO needed: len(prefix) > 0?
    return f'\t{prefix}\t{key_info} : {item_type:>10} : {item}'


def _ret_items(the_dict: dict, prefix: str = '::') -> str:
    ret = ''
    ret += _ret_item_info('____key____', '____value____', prefix + '____') + '\n'
    # for key, value in ret_sorted(the_dict).items():   # Sorted by key
    for key, value in the_dict.items():
        ret += _ret_item_info(key, value, prefix + ' i:') + '\n'
    return ret


# def ret_keys(the_dict: dict) -> str:    # tested
#     assert isinstance(the_dict, dict), 'Expected a dictionary'
#     assert the_dict, 'Dictionary is empty'
#     return ', '.join(list(the_dict.keys()))


class LogHelper:
    @staticmethod
    def ret_dict_info(
        the_dict: dict, name: str, prefix: str = '::', incl_items: bool = True
    ) -> str:
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
        caller: str = inspect.stack()[1][3]

        ret = f'{prefix} {name:<15}: [dict] (#={the_length}) (<< "{caller}") {TEST_CONTEXT} \n\n'
        if incl_items:
            ret += _ret_items(the_dict) + '\n'

        return COL_CONTEXT + ret + COL_RESET
        # return  COL_DBG + ret + COL_RESET

        # def _ret_dict_info(self, the_dict: dict, name: str, prefix: str = '') -> str:
        #     """
        #     Function ret_dict_info returns a string with info
        #     about the named dictionary and its content
        #         Param 1: it: dict
        #         Param 2: name: str
        #         Param 3: prefix: str (optional)
        #     """
        #     assert isinstance(the_dict, dict), 'A dict was not given!'

        #     the_length = '--EMPTY!' if not the_dict else len(the_dict)

        #     ret = f'{prefix} {name:<15}: [dict] (#={the_length})\n'
        #     # the_dict['temp'] = 'hallo'
        #     show_items = True
        #     if show_items and the_dict and the_length != 0:   # Include the items in the_dict
        #         ret += ret_item_info('____key____', '____value____', '_item_') + '\n'
        #         inum = 1

        #     for key, value in ret_sorted(the_dict).items():
        #             # ret += ret_item_info(key, value, prefix) + '\n'
        #             ret += ret_item_info(key, value, f'i {inum}') + '\n'
        #             inum = inum + 1

        #     xlog_msg(msg=ret, show_caller=False)
        #     # xlog_msg('ret_dict_info() : ', INFO, ret)
        #     GLUE_LOGGER.info('ret_dict_info() >> %s ', ret)
        #     logging.warning('%sret_dict_info() >> %s ', COL_CONTEXT, ret)

        #     # return ret
        #     return str(COL_INFO) + ret + str(COL_RESET)

    @staticmethod
    def ret_func_name(prev: int = 0) -> str:
        """
        Usage:
        * _ret_func_name() - will return it's own func_name ("the caller of ret_func_name()")
        * _ret_func_name(1) - will return the func_name of the caller
        * _ret_func_name(2) - will return the func_name of the callers caller
        """
        # LogHelper.log_func_call()
        return inspect.stack()[1 + prev][3]

    @staticmethod
    def ret_provider_info() -> str:
        ret = f'{COL_CONTEXT}(<- by {LogHelper.ret_func_name(1)}() with caller {LogHelper.ret_func_name(2)}())'
        return ret

    @staticmethod
    def ret_keys(the_dict: dict) -> str:  # tested
        assert isinstance(the_dict, dict), 'Expected a dictionary'
        assert the_dict, 'Dictionary is empty'
        return ', '.join(list(the_dict.keys()))

    @staticmethod
    def ret_sorted(obj) -> Any:  # tested
        """
        A generic sorting function, taking into account the type of object passed.
        """
        ret = obj
        if isinstance(obj, dict):
            ret = dict(sorted(obj.items()))
        return ret

    @staticmethod
    def log_dict_now(the_dict: dict, name: str = None, prefix: str = '\t\t') -> None:
        assert isinstance(the_dict, dict), 'A dict was not given!'
        assert prefix is not None, 'Prefix was not given!'

        logging.warning(the_dict.get(KEY_HOOKS, 'N/A'))
        return

        logging.info(' -------------------------------------> log_dict_now Begin')
        LogHelper.log_func_name(prev=0, informative=True)
        LogHelper.log_func_name(prev=1, informative=True)
        # LogHelper.log_func_name(prev=1, informative=True)
        LogHelper.log_func_name(prev=1, informative=True)  # TODO delete one

        # logging.info(
        #     '%s%s%s: --> %s %s',
        #     COL_CONTEXT,
        #     prefix,
        #     name if name else 'dict',
        #     # ret_func_name(),
        #     the_dict,
        #     self._ret_provider_info()
        # )

        # the_length = len(the_dict) if the_dict else "--EMPTY!"
        # logging.info('\t%s%s #%s: %s %s', \
        # COL_CONTEXT, name, the_length, the_dict, self._ret_provider_info())

        logging.info(LogHelper.ret_dict_info(the_dict, name, 'x'))
        # logging.info(ret_dict_info(the_dict, name, prefix))
        # log_items(the_dict, prefix)
        logging.info(' <------------------------------------- _log_dict_now End')

    @staticmethod
    def process_value(value):
        switch = {
            1: 'Value is either 1 or 2',
            2: 'Value is either 1 or 2',
            3: 'Value is 3',
        }
        print(switch.get(value, 'Value is not 1, 2, or 3'))

    @staticmethod
    def quoted_string_from(value: Any, quote: str = "'") -> Any:

        if hasattr(value, 'name'):
            return f'{quote}{value.name}{quote}'
        # else:
        #     return '+?+'

        if isinstance(value, FixtureRequest):
            return '+++'

        if isinstance(value, str):
            return f'{quote}{value}{quote}'

        return repr(value)   # no quotes here yet

    @staticmethod
    def log_func_call(
        _log_level: int = logging.INFO,
    ) -> None:
        """
        Logs the calling function along with its arguments.
        """
        # Get the calling function's frame
        frame = inspect.currentframe().f_back
        caller = LogHelper.ret_func_name(1)
        assert isinstance(caller, str), 'Not a str'
        calling_args = inspect.getargvalues(frame)
        # print(calling_args) # This is noisy
        args = ', '.join(
            [
                f'{arg}={LogHelper.quoted_string_from(value)}'
                for arg, value in calling_args.locals.items()
                if arg != 'self'
            ]
        )
        wanted_logged = f'{COL_MSG}{caller}{COL_INFO}({args}){LogHelper.ret_provider_info()}'
        logging.info(wanted_logged)  # TODO: use log_level
        # logging.info("-> %s(%s)", calling_function, args)  # TODO: use log_level
        # ==> "-> func_name(param1='val1, param2:'val2', param3=3 ...)"

    @staticmethod  # TODO Is this func really needed
    def log_func_name_with_info(
        msg: str, prev: int = 0, fillchar: str = '', informative=True
    ) -> None:
        LogHelper.log_func_name(prev + 1, informative)
        logging.info("%smsg:\t%s%s'%s'", COL_CONTEXT, fillchar, COL_MSG, msg)

    @staticmethod
    def log_func_name(prev: int = 0, informative=True) -> None:  # tested
        """
        Logs the function name of the calling function.
        """
        logging.info(
            '%s%s%s%s',
            COL_INFO if not informative else COL_CONTEXT,
            COL_MSG,
            LogHelper.ret_func_name(prev + 1),
            '' if not informative else f'{COL_INFO}(prev={prev}) {LogHelper.ret_provider_info()}',
        )
        # logging.info(caller)
        # logging.info(
        #     '%s->%s  %s(prev=%s) << %s %s',
        #     COL_INFO if not informative else COL_CONTEXT,
        #     _ret_func_name(1),
        #     COL_MSG,
        #     prev,
        #     caller,
        #     _ret_provider_info(),
        # )
        # logging.info(
        #     '\t%s->%s  %s(prev=%s) << %s %s',
        #     COL_INFO if not informative else COL_CONTEXT,
        #     _ret_func_name(1),
        #     COL_MSG,
        #     prev,
        #     caller,
        #     _ret_provider_info(),
        # )
        logging.debug('(using prev %s)', 1 + prev)

        # caller = xret_func_name(1 + prev)
        # log_headline(caller, prev, inRow, fillchar)

    @staticmethod
    def log_func_call_info(info: str = '??', log_level: int = logging.INFO, prev: int = 0) -> None:
        # TODO info -> msg? and first param?
        # GLUE_LOGGER.info(LogHelper.ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT'))
        caller = LogHelper.ret_func_name(1 + prev)
        # xlog_msg(LogHelper.ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT', caller + '--> log_func_call_info---->'))
        its_caller = LogHelper.ret_func_name(2 + prev)

        if caller.startswith('pytest_bdd_'):
            its_caller = 'Pytest-BDD'  # TODO Hint: Comment to see the actual function
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
            logging.debug('Not overriding the info: %s', info)

        if '==' in info:  # a hook
            logging.log(
                log_level,
                '|%s%-19s %s%s| %s',
                COL_CONTEXT,
                its_caller,
                info,
                COL_RESET,
                caller,
            )
            TEST_CONTEXT['dbg:TEST_CONTEXT'] = True  # TODO explain need for this
            # log_msg('dbg:TEST_CONTEXT = True')
        elif '--' in info:  # a hook
            logging.log(log_level, '|%s%-25s %s| %s', COL_CONTEXT, its_caller, info, caller)
        else:
            logging.log(
                log_level,
                '|%30s| %s %s(.<< %s)',
                caller,
                info,
                COL_CONTEXT,
                its_caller,
            )

    @staticmethod
    def ret_before_or_after(func_name: str) -> str:  # tested
        assert func_name is not None and len(func_name) > 0, 'No param "func_name"'
        # assert '_' in func_name, 'No _ char found in "func_name". (Expects _)'
        if 'before' in func_name:
            return 'Before'
        elif 'after' in func_name:
            return 'After'

        return ''

    @staticmethod
    def assert_messages(caplog, level, messages: List, in_sequence: bool = False) -> None:
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
