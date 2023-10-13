import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

import pytest
from pytest import Config, FixtureRequest, Function, Item
from pytest_bdd.parser import Feature, Scenario, Step

from tests.common.ansi_colors import ANSIColor
from tests.common.log_helper import COL_CONTEXT, KEY_CONFIG, KEY_LOG_CONFIG, TEST_CONTEXT, LogHelper


class PytestBddLoggerInterface(ABC):
    """
    PytestBddLoggerInterface is an abstract base class (interface)
    for logging Pytest BDD testing.
    """

    # # Constants:
    # KEY_CURR_FEATURE = 'Current feature'

    # COL_GLUE = '\033[1;36m'
    COL_INFO = ANSIColor.BLUE.value
    COL_MSG = ANSIColor.CYAN.value
    COL_RESET = ANSIColor.RESET.value
    COL_SCENARIO = ANSIColor.YELLOW.value
    COL_STEP = ANSIColor.GREEN.value
    COL_CONTEXT = ANSIColor.GRAY.value

    @classmethod
    def ret_classname(cls) -> str:
        """
        Return the name of the class.

        :param cls: The class object.
        :return: The name of the class as a string.
        :rtype: str
        """
        return cls.__name__

    def _m_ret_provider_info(self) -> str:
        ret = f'(<- by {self.ret_classname()}.{LogHelper.ret_func_name(1)}() \
            with caller {LogHelper.ret_func_name(2)}())'
        return ret

    # def ret_func_name(self, prev: int = 0) -> str:
    #     """
    #     Usage:
    #     * ret_func_name() - will return it's own func_name ("the caller of ret_func_name()")
    #     * ret_func_name(1) - will return the func_name of the caller
    #     * ret_func_name(2) - will return the func_name of the callers caller
    #     """
    #     return (
    #         inspect.currentframe().f_back.f_code.co_name
    #         if prev == 0
    #         else inspect.stack()[1 + prev][3]
    #     )
    #     # using inspect.currentframe().f_back.f_code.co_name is generally more efficient
    #     # and performs better in terms of performance when retrieving the function name
    #     # (than the else alternative).

    def log_dict(self, the_dict: dict, name: str) -> None:   # ? + incl_items: bool = True
        """
        Function log_dict will log the given dict
        and its items if incl_items=True.
            Param 1: the_dict: dict
            Param 2: name: str
            Param 3: incl_items: bool (default: True)
        """
        logging.info('%s', '_' * 100)
        logging.info('%s', '--1' * 25)
        temp = COL_CONTEXT + name  # TODO
        logging.info('%s', '--2' * 25)
        temp += ' : ' + str(the_dict)
        temp += LogHelper.ret_dict_info(the_dict, name)
        logging.info(temp)
        logging.info('%s', '_' * 100)
        #

    def maybe_log_configuration(self) -> None:
        LogHelper.log_func_name()
        if TEST_CONTEXT.get(KEY_LOG_CONFIG, True):
            # No need to store the config in TEST_CONTEXT any more
            config = TEST_CONTEXT.pop(KEY_CONFIG, None)
            assert config, 'config is None! Forgot to add config to the dict TEST_CONTEXT?'
            self.log_configuration(config)
            TEST_CONTEXT[KEY_LOG_CONFIG] = False

    def log_configuration(self, config: pytest.Config) -> None:

        LogHelper.log_func_name()
        assert config, 'config is None!'

        config: Config = TEST_CONTEXT.get('config', None)
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT', '---->')

        # Get the log level from the command-line option
        log_level = config.getoption('--log-cli-level')
        logging.warning('pytest_configure config: log_level: %s (command-line option)', log_level)
        print(f'command-line option config: log_level: {log_level}')

        # Get the log level from pyproject.toml
        log_level = config.getini('log_level')
        logging.warning('config: log_level: %s (from pyproject.toml)', log_level)
        print(f'     pyproject.toml config: log_level: {log_level}')

    ############################################################################
    ###########################   Abstract methods   ###########################
    ############################################################################

    @abstractmethod
    def log_hook(self, msg: str = '') -> None:
        LogHelper.log_func_name(1)

        # TODO: skal alle andre log_-metodene legges her eller alle være i tracer
        raise NotImplementedError()

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
        logging.warning(TEST_CONTEXT)
        self.log_hook(f'***configure*** (config.hook: {str(config.hook)})')
        logging.warning(TEST_CONTEXT)
        # print('configure() called by: ', self._ret_func_name(1)) #TODO Remove

        TEST_CONTEXT['config'] = config   # TODO Needed?
        # log_configuration() will be called later to inform about config
        # (in runtest_protocol())

    def runtest_protocol(self, item: Item, _nextitem: Optional[Item]) -> bool:
        """
        perform additional actions before and after each test
        It takes a single argument, item, which represents the test item being executed.

        Args:
            item: Item: the test item being executed
            nextitem: Optional[Item]
        """
        assert 'pytest_runtest_protocol' == LogHelper.ret_func_name(1)
        assert item
        # assert nextitem
        self.log_hook(f'(item.name: {item.name})')

        LogHelper.log_func_name_with_info(msg=f'(item.name: {item.name})', fillchar='h:')

        assert item is not None, '(pytest) runtest_protocol: item is None'
        # print('(pytest)runtest_protocol: item = ' + item.__class__.__name__)
        assert isinstance(item, Function), '(pytest) runtest_protocol: item is not a Function'
        print('(pytest)runtest_protocol: item.name = ' + item.name)
        # print('(pytest)runtest_protocol: nextitem = ' + str(nextitem))
        logging.info('(pytest)runtest_protocol: test => %s', item.name)
        # log_headline(msg=item.name)

        # xlog_msg_start()
        # # Check if the test is a Pytest-BDD step
        # if item.parent and item.parent.name.startswith("Scenario:") -> None:
        #     GLUE_LOGGER.info('hook => pytest_runtest_protocol\t(in "root" conftest.py)')
        #     # Get the step function from the pytest item
        #    GLUE_LOGGER.warning('Get the step function from the pytest item\
        #       (<< pt._runtest_protocol)')
        #     step_func = item.obj
        #     def patched_step_func(*args, **kwargs) -> None:
        #         GLUE_LOGGER.warning('"Monkey patched" step function (<< pytest_runtest_protocol)')
        #         print("Parameters:", args, kwargs)
        #         return step_func(*args, **kwargs)
        #     item.obj = patched_step_func
        # log_msg_end()

    @abstractmethod
    def before_feature(self, _request: FixtureRequest, feature: Feature) -> None:
        raise NotImplementedError()

    @abstractmethod
    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def before_step(
        self,
        request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        LogHelper.log_func_name_with_info(step.name, fillchar='    ->')
        assert False, 'Not passing before_step!'

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:

    @abstractmethod
    def after_scenario(self, request: FixtureRequest, feature: Feature, scenario: Scenario) -> None:
        LogHelper.log_func_name_with_info(scenario.name, fillchar='  <-')
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
        LogHelper.log_func_name_with_info(step.name, fillchar='    <-')
        # LogHelper.log_dict_now
        self.log_dict(step_func_args, 'step_func_args')
        # assert False, 'Not passing after_step!'

    @abstractmethod
    def log(
        self,
        msg: str,
        log_level: int = logging.INFO,
        pre: str = '',
        show_caller: bool = False,
    ) -> None:
        raise NotImplementedError()
