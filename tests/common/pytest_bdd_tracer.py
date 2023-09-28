import logging
import os
from abc import ABC, abstractmethod
from logging import INFO
from typing import Any, Callable

from pytest import Config, FixtureRequest
from pytest_bdd.parser import Feature, Scenario, ScenarioTemplate, Step

# from tests.common.bdd_logger import PytestBddLogger
# from tests.common.log_glue_incl import ret_func_name  # TODO Move to interface?
from tests.common.log_glue_incl import TEST_CONTEXT
from tests.common.pytest_bdd_logger_interface import PytestBddLoggerInterface

# BbbLogger related constants:

# DO_INCL_CURR_INFO = True
#
# KEY_CURR_FEATURE = 'Current feature'
# KEY_CURR_GLUE = 'Current glue'
# KEY_CURR_SCENARIO = 'Current scenario'
# KEY_CURR_STEP = 'Current step'
#
# KEY_CONTEXT = 'context'
KEY_DBG_FUNC_NAME = 'dbg:func_name'  # Last function that called log_func_name()

#
# KEY_FUNC = '|Func'      # TODO Should add all glue functions called
# KEY_HOOKS = '|Hooks'    # TODO Should add all hooks called

# TODO Use 'KEY_' Prefix for texts being keys
# KEY_STEP_COUNTER = 'step_counter'

# TODO: switch "log_glue" to "bdd_logger" (?? and "log_msg" to "log")


# def log_msg_start(log_level: int = logging.INFO) -> None:
#     # logging.info('***log_msg_start***')
#     TEST_CONTEXT[KEY_DBG_FUNC_NAME] = ret_func_name()   # TODO remove line
#     # log_msg(ret_func_name() + ' -> ' + TEST_CONTEXT)
#     log_msg(ret_func_name(1), show_caller=not True)
#     # logging.log(log_level, 'Heisann!')

#     # log_msg(TEST_CONTEXT)
#     # log_dict(TEST_CONTEXT, 'TEST_CONTEXT', False)
#     # log_func_call_info(log_level, 1, 'INFO')


# def log_msg_end(log_level: int = logging.INFO) -> None:
#     # logging.info('***log_msg_end***')
#     log_func_call_info(log_level, 1)

################################################################################


class PytestBddTracer(PytestBddLoggerInterface):
    """
    PytestBddTracer is a abstract class helpful for logging Pytest BDD testing.
    It implements many of the abstract PytestBddLoggerInterface methods.
    A subclass that implements its abstract methods can be used by conftest.py
    to log messages from Pytest BDD hooks.
    You may pass a False value to the constructor to disable "context logging".
    """
    #TODO: You may pass a False value to the constructor to disable "context logging".

    def __init__(self, show_context: bool = True):
        self.show_context = show_context

    # def get_test_context(self) -> dict:
    #     return TEST_CONTEXT

    # @abstractmethod #TODO
    def log_feature(self, feature: Feature) -> None:
        self.log_func_name(msg=feature.name, fillchar='_')
        self.log(f'\t {self.COL_MSG}Feature: "{feature.name}"')
        # logging.info(
        #     f'%sFeature: "%s" %s',
        #     self.COL_MSG,
        #     feature.name,
        #     self.ret_context_info(1)
        # )
        # ret_context = self.get_context_info()


    # @abstractmethod #TODO
    def log_scenario(self, scenario: Scenario) -> None:
        self.log_func_name(msg=scenario.name, fillchar='_')
        self.log(f'\t {self.COL_MSG}Scenario: "{scenario.name}"')



    def before_feature(self, _request: FixtureRequest, feature: Feature) -> None:
        """
        Pytest-BDD don't have a seperate hook "pytest_bdd_before_feature".
        This function will be called because of pytest_bdd_before_scenario,
        and before the first scenario is run the before_feature is called.

        Args:
            _request (FixtureRequest): unused
            feature (Feature): The feature object be executed

        Returns:
            None
        """
        # self.log(f'Feature_: "{feature.name}"')
        # self.log_func_name(fillchar=' _:')

        self._before_feature_assert_params(_request, feature)
        TEST_CONTEXT[self.KEY_CURR_FEATURE] = feature.name

        self.log_func_name(msg=feature.name)
        self.log_feature(feature)

        self.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT')

    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        # self.log_func_name(fillchar='\t :')
        super().before_scenario(_request, feature, scenario)
        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - before_scenario'
        # logging.warning(' <-------------------------------------')

    def before_step(
        self,
        _request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        self.log_func_name(fillchar='h:\t->\t ', msg=step.name)

        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - before_step'

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:
    #     print('-> after_feature')

    def after_scenario(self, request: FixtureRequest, feature: Feature, scenario: Scenario) -> None:
        # logging.warning('after_scenario <--- %s', __file__)
        super().after_scenario(request, feature, scenario)
        logging.info(' <------------------------------------- after_scenario')
        self.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT')
        logging.info(' <------------------------------------- after_scenario')
        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - after scenario'

    def after_step(
        self,
        _request: FixtureRequest,
        _feature: Feature,
        _scenario: Scenario,
        _step: Step,
        _step_func: Callable,
        step_func_args: dict[str, Any],
    ) -> None:
        self.log_func_name(fillchar='\t<-')
        logging.info(' <------------------------------------- after_step')
        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - after step'


    def ret_context_info(self, prev: int = 1) -> str:
        if self.show_context:
            return f' (<-by {self.ret_func_name(prev)}() in {self.ret_classname()})'
        else:
            return ''

    def log(
        self, msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False
    ) -> None:
        # logging.info('%s\t%s%s%s', self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info(2))

        # logging.info('%s%s%s_1 log: %s', self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info(1))
        # logging.info('%s%s%s__ %s', self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info())

        # context_info = (
        #     ''
        #     if not self.show_context
        #     else f' (<-by {ret_func_name()}() in {self.ret_classname()})'
        # )
        # logging.info(
        #     '%s %s%s%s %s',
        #     fillchar != None and fillchar or '->',
        #     self.COL_INFO,
        #     ret_func_name(1 + prev),
        #     self.COL_CONTEXT,
        #     self.ret_context_info(),
        # )
        # super().log(msg, log_level, pre, show_caller)
        # logging.warning('log <--- %s', __file__)
        pass

    def log_hook(self, msg: str = '') -> None:
        self.log_func_name(prev=1, fillchar='H:', msg='æ:'+msg)
        self.log_func_name(prev=0, fillchar='', msg='ø:'+msg)
        self.log_func_name(prev=0, msg='å:'+msg)
        caller = self.ret_func_name(2)
        logging.info('H: log_hook(): %s%s', self.COL_MSG, caller)



    def log_func_name(self, prev: int = 0, fillchar: str = None, msg: str = '') -> None:
        caller = self.ret_func_name(1)
        indent = 1 if fillchar and 'H:' in fillchar else 4
        if caller != 'after_scenario':
            TEST_CONTEXT[KEY_DBG_FUNC_NAME] = caller    # TODO remove line?
        # print('BddTracer -> log_func_name():')
        # print('BddTracer -> log_func_name() called from ', ret_func_name(1 + prev))
        # super().log(msg, log_level, pre, show_caller)

        assert self.show_context, 'No context logging!'
        # assert fillchar == ":"
        context_info = (
            '' if not self.show_context
            else self.ret_context_info(2)
            # else f"(<-by {self._ret_func_name(prev)}() in {self.ret_classname()} (it's caller: {self._ret_func_name(prev + 2)}() ))"
        )
        # logging.warning('Called by %s', self._ret_func_name(1 + prev))
        if fillchar == "H:":
            context_info += 'SAH'

        logging.info(
            '%s%s%s %s%s %s %s',
            indent * ' ',
            self.COL_INFO,
            # fillchar != None and fillchar or '->',
            fillchar if fillchar else '->',
            self.ret_func_name(1 + prev),
            self.COL_CONTEXT,
            '' if msg == '' else msg,
            context_info,
        )

    # def ret_filename(self, filepath:str) -> str:
    # assert filepath != None and filepath.find('\\') != -1, 'No filepath! (Got: %s)'
    # filename = os.path.basename(__file__)
    # assert filename != None and filename == "pytest_bdd_tracer.py", 'No filename! (Got: %s)'
    # return filename
    # return filepath.split("\\")[-1] # Retrieve the last part after the last '\' character
