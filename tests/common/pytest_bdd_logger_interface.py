import inspect
import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Callable, Optional

from pytest import Config, FixtureRequest, Function, Item
from pytest_bdd.parser import Feature, Scenario, Step

from src.ansi_colors import ANSIColor

# TEST_CONTEXT = {'name': 'TEST_CONTEXT'}
TEST_CONTEXT = OrderedDict({'name': 'TEST_CONTEXT'})
# Constants used for items in TEST_CONTEXT:
KEY_CURR_FEATURE = 'Current feature'
KEY_CURR_GLUE = 'Current glue'
KEY_CURR_SCENARIO = 'Current scenario'
KEY_CURR_STEP = 'Current step'
KEY_LOG_GLUE = 'log_glue'    # TODO: Values: None (=False), False,  True, Hooks (=True), Feature, Scenario, Step
KEY_LOGGER = 'logger'    # TODO: Values: None (=False), False,  True


KEY_FUNC = '|Func'      # TODO Should add all glue functions that gets called
KEY_HOOKS = '|Hooks'    # TODO Should add all hooks that gets called


def xret_func_name(prev: int = 0) -> str:
    """
    Usage:
    * ret_func_name() - will return it's own func_name ("the caller of ret_func_name()")
    * ret_func_name(1) - will return the func_name of the caller
    * ret_func_name(2) - will return the func_name of the callers caller
    """
    # logging.info('ret_func_name(prev=%s)', prev)
    return inspect.stack()[1 + prev][3]

def ret_dict_info(the_dict: dict, name: str, prefix: str = '::') -> str:
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

    ret += ret_item_info('____key____', '____value____', prefix + '____') + '\n'
    # for key, value in ret_sorted(the_dict).items():   # Sorted by key
    for key, value in the_dict.items():
        ret += ret_item_info(key, value, prefix + ' i:') + '\n'

    return '\x1b[90m' + ret + '\x1b[0m'

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

    #     old_log_msg(msg=ret, show_caller=False)
    #     # old_log_msg('ret_dict_info() : ', INFO, ret)
    #     GLUE_LOGGER.info('ret_dict_info() >> %s ', ret)
    #     logging.warning('%sret_dict_info() >> %s ', COL_CONTEXT, ret)

    #     # return ret
    #     return str(COL_INFO) + ret + str(COL_RESET)

def ret_item_info(name: str, item, prefix: str = 'i') -> str:
    """
    Function ret_item_info returns a string with info
    about the named item, its type and its content
        Param 1: name: str
        Param 2: item
    """
    item_type = f'[{type(item).__name__}]' if not '_key_' in name else '_type_'
    key_info = '{name:<20}' if prefix and prefix[0] == 'p' else f'{name.rjust(20, " ")}' #TODO needed: len(prefix) > 0?
    return f'\t{prefix}\t{key_info} : {item_type:>10} : {item}'

def ret_sorted(obj) -> Any:    # tested
    ret = obj
    if isinstance(obj, dict):
        ret = dict(sorted(obj.items()))
    return ret


class PytestBddLoggerInterface(ABC):
    """
    PytestBddLoggerInterface is an abstract base class (interface)
    for logging Pytest BDD testing.
    """

    # # Constants:
    KEY_CURR_FEATURE = 'Current feature'
    # KEY_CURR_GLUE = 'Current glue'
    # KEY_CURR_SCENARIO = 'Current scenario'
    # KEY_CURR_STEP = 'Current step'

    # KEY_FUNC = '|Func'      # TODO Should add all glue functions called
    # KEY_HOOKS = '|Hooks'    # TODO Should add all hooks called

    # COL_GLUE = '\033[1;36m'
    COL_INFO = ANSIColor.BLUE.value
    COL_MSG = ANSIColor.CYAN.value
    COL_RESET = ANSIColor.RESET.value
    COL_SCENARIO = ANSIColor.YELLOW.value
    COL_STEP = ANSIColor.GREEN.value
    COL_CONTEXT = ANSIColor.GRAY.value

    @classmethod
    def ret_classname(cls) -> str:
        return cls.__name__

    def _ret_provider_info(self) -> str:
        ret =f'(<- by {self.ret_classname()}.{self.ret_func_name(1)}() with caller {self.ret_func_name(2)}())'
        return ret

    def ret_func_name(self, prev: int = 0) -> str:
        """
        Usage:
        * ret_func_name() - will return it's own func_name ("the caller of ret_func_name()")
        * ret_func_name(1) - will return the func_name of the caller
        * ret_func_name(2) - will return the func_name of the callers caller
        """
        return inspect.currentframe().f_back.f_code.co_name if prev == 0 else inspect.stack()[1 + prev][3]
        # using inspect.currentframe().f_back.f_code.co_name is generally more efficient
        # and performs better in terms of performance when retrieving the function name (than the else alternative).


    @abstractmethod
    def log_hook(self) -> None:
        raise NotImplementedError()

    def log_dict_now(self, the_dict: dict, name: str = None, prefix: str = '\t\t') -> None:

        assert isinstance(the_dict, dict), 'A dict was not given!'

        logging.info(' -------------------------------------> log_dict_now B')
        self.log_func_name()
        self.log_func_name(1)

        # logging.info(
        #     '%s%s%s: --> %s %s',
        #     self.COL_CONTEXT,
        #     prefix,
        #     name if name else 'dict',
        #     # ret_func_name(),
        #     the_dict,
        #     self._ret_provider_info()
        # )

        the_length  = len(the_dict) if the_dict else '--EMPTY!'
        # logging.info('\t%s%s #%s: %s %s', self.COL_CONTEXT, name, the_length, the_dict, self._ret_provider_info())

        # TODO Finish method: log_dict_now
        logging.info(ret_dict_info(the_dict, name, 'x'))
        # logging.info(ret_dict_info(the_dict, name, prefix))
        logging.info(' <------------------------------------- log_dict_now E')

        # log_items(the_dict, prefix)

    def log_dict(self, the_dict: dict, name: str, incl_items: bool = True) -> None:
        """
        Function log_dict will log the given dict
        and its items if incl_items=True.
            Param 1: the_dict: dict
            Param 2: name: str
            Param 3: incl_items: bool (default: True)
        """
        logging.info('%s', '_' * 100)
        # logging.info('%s', '--1' * 25)
        # temp = self.ret_dict_info(the_dict, name, 'log_dict:') #TODO ret_dict_info
        temp = self.COL_CONTEXT + name   # TODO
        # logging.info('%s', '--2' * 25)
        temp += ' : ' + str(the_dict)
        logging.info(temp)
        logging.info('%s', '_' * 100)

    def log_configuration(self) -> None:
        config: Config = TEST_CONTEXT.get('config', None)
        assert config, 'config is None! Forgot to add config to the dict TEST_CONTEXT?'

        # Get the log level from the command-line option
        log_level = config.getoption('--log-cli-level')
        logging.warning('pytest_configure config: log_level: %s (command-line option)', log_level)
        print(f'command-line option config: log_level: {log_level}')

        # Get the log level from pyproject.toml
        log_level = config.getini('log_level')
        logging.warning('config: log_level: %s (from pyproject.toml)', log_level)
        print(f'     pyproject.toml config: log_level: {log_level}')

        #TODO Set the wanted log_level here and log it in TEST_CONTEXT?

    ############################################################################

    # @abstractmethod
    def configure(self, config: Config) -> None:
        """
        Configure the logger.

        Note: We are not able to log anything here yet...!

        Args:
            config (Config): The configuration object passed to pytest_configure.

        Returns:
            None
        """
        # print('configure() called by: ', self._ret_func_name(1)) #TODO Remove

        self.log_func_name()

        TEST_CONTEXT['config'] = config
        # log_configuration() will be called later to inform about config
        # (in runtest_protocol())

    def runtest_protocol(self, item: Item, nextitem: Optional[Item])  -> bool:
        """
        perform additional actions before and after each test
        It takes a single argument, item, which represents the test item being executed.

        Args:
            item: Item: the test item being executed
            nextitem: Optional[Item]
        """
        self.log_func_name(fillchar='h:', msg=f'(item.name: {item.name})')

        assert item is not None, '(pytest) runtest_protocol: item is None'
        print('(pytest)runtest_protocol: item = ' + item.__class__.__name__)
        assert isinstance(item, Function), '(pytest) runtest_protocol: item is not a Function'
        print('(pytest)runtest_protocol:     item = ' + str(item))
        print('(pytest)runtest_protocol: nextitem = ' + str(nextitem))
        logging.warning('(pytest)runtest_protocol: test = %s', str(item))

        # xlog_msg_start()
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
        # log_msg_end()

    def _before_feature_assert_params(self, _request: FixtureRequest, feature: Feature) -> None:
        assert feature is not None, 'No feature param! (_before_feature_assert_params)'
        assert feature.name is not None, 'Feature name is empty! (_before_feature_assert_params)'
        assert (len (feature.name) > 3), 'Feature name should be longer! (_before_feature_assert_params)'
        logging.info('Feature name: %s', feature.name)

    @abstractmethod
    def before_feature(self, _request: FixtureRequest, feature: Feature) -> None:
        raise NotImplementedError()

    # @abstractmethod
    # def log_dict_now(self, the_dict: dict, name: str, prefix: str = '¤') -> None:

    @abstractmethod
    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        self.log_func_name(fillchar='  ->', msg=scenario.name)

    @abstractmethod
    def before_step(
        self,
        request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        assert False, 'Not passing before_step!'
        self.log_func_name(fillchar='    ->', msg=step.name)

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:

    @abstractmethod
    def after_scenario(self, request: FixtureRequest, feature: Feature, scenario: Scenario) -> None:
        self.log_func_name(fillchar='  <-', msg=scenario.name)
        # assert False, 'Not passing after_scenario!'

    @abstractmethod
    def after_step(
        self,
        _request: FixtureRequest,
        _feature: Feature,
        _scenario: Scenario,
        step: Step,
        _step_func: Callable,
        step_func_args: dict[str, Any],
    ) -> None:
        self.log_func_name(fillchar='    <-', msg=step.name)
        # assert False, 'Not passing after_step!'

    @abstractmethod
    def log(
        self, msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def log_func_name(self, prev: int = 0, fillchar: str = None, msg: str = '') -> None:
        raise NotImplementedError()
