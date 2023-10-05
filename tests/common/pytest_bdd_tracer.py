import logging
from abc import abstractmethod
from typing import Any, Callable

from pytest import FixtureRequest
from pytest_bdd.parser import Feature, Scenario, Step

from tests.common.log_glue_incl import TEST_CONTEXT
from tests.common.pytest_bdd_logger_interface import PytestBddLoggerInterface
from tests.common.log_helper import LogHelper

# TODO: switch "log_glue" to "bdd_logger" (?? and "log_msg" to "log")

################################################################################


class PytestBddTracer(PytestBddLoggerInterface):
    """
    PytestBddTracer is a abstract class helpful for logging Pytest BDD testing.
    It implements many of the abstract PytestBddLoggerInterface methods.
    A subclass that implements its abstract methods can be used by conftest.py
    to log messages from Pytest BDD hooks.
    You may pass a False value to the constructor to disable "context logging".
    """

    # TODO: You may pass a False value to the constructor to disable "context logging".

    def __init__(self, show_context: bool = True):
        self.show_context = show_context

    # def get_test_context(self) -> dict:
    #     return TEST_CONTEXT

    @abstractmethod
    def log_feature(self, feature: Feature) -> None:
        LogHelper.log_func_name_with_info(feature.name, fillchar="h:\t->\t ")
        self.log(f'\t {self.COL_MSG}Feature: "{feature.name}"')
        # logging.info(
        #     f'%sFeature: "%s" %s',
        #     self.COL_MSG,
        #     feature.name,
        #     self.ret_context_info(1)
        # )
        # ret_context = self.get_context_info()

    @abstractmethod
    def log_scenario(self, scenario: Scenario) -> None:
        LogHelper.log_func_name_with_info(scenario.name, fillchar="_")
        self.log(f'\t {self.COL_SCENARIO}Scenario: "{scenario.name}"')

    @abstractmethod
    def log_step(self, step: Step, scenario: Scenario) -> None:
        LogHelper.log_func_name_with_info(step.name, fillchar=".")
        pass

    def before_feature(self, request: FixtureRequest, feature: Feature) -> None:
        """
        Pytest-BDD don't have a seperate hook "pytest_bdd_before_feature".
        This function will be called by pytest_bdd_before_scenario
        before the first scenario is run.

        Args:
            request (FixtureRequest): unused
            feature (Feature): The feature object be executed

        Returns:
            None
        """
        caller = LogHelper.ret_func_name(1)
        assert "pytest_bdd_before_scenario" == caller or caller.startswith("test_"), (
            "Unknown caller: " + caller
        )
        self._assert_obj_named(feature)
        # self._before_feature_assert_params(request, feature)
        logging.info(" -------------------------------------> before_feature")
        caller = LogHelper.ret_func_name(1)  # TODO make better name 2
        logging.warning(caller)
        LogHelper.log_func_name_with_info(feature.name, fillchar="h:\t->\t ")
        # LogHelper.log_func_name(msg=feature.name, fillchar='_')
        # self.log(f'Feature_: "{feature.name}"')
        # LogHelper.log_func_name(fillchar=' _:')

        logging.info(request.node)
        # TODO: maybe TEST_CONTEXT[self.KEY_TEST_ITEM] = request.node
        TEST_CONTEXT[self.KEY_CURR_FEATURE] = feature.name

        print(caller)

        assert "pytest_bdd_before_" in caller or caller.startswith("test_"), (
            "Unknown caller: " + caller
        )
        self.log_hook("pytest_bdd_before_feature - don't exist!")
        LogHelper.log_func_name_with_info(feature.name)
        self.log_feature(feature)

        LogHelper.log_dict_now(TEST_CONTEXT, "TEST_CONTEXT")

    # @abstractmethod #TODO
    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        logging.info(" -------------------------------------> before_scenario")
        LogHelper.log_func_name_with_info(scenario.name, fillchar="h:\t->\t ")
        # assert request
        # LogHelper.log_func_name(fillchar='\t :')
        # super().before_scenario(request, feature, scenario)
        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - before_scenario'
        # logging.warning(' <-------------------------------------')

    def before_step(
        self,
        request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        logging.info(" -------------------------------------> before_step")
        LogHelper.log_func_name_with_info(step.name, fillchar="h:\t->\t ")

        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - before_step'

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:
    #     print('-> after_feature')

    def after_scenario(
        self, request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        # logging.warning('after_scenario <--- %s', __file__)
        super().after_scenario(request, feature, scenario)
        logging.info(" <------------------------------------- after_scenario")
        LogHelper.log_dict_now(TEST_CONTEXT, "TEST_CONTEXT")
        logging.info(" <------------------------------------- after_scenario")
        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - after scenario'

    def after_step(
        self,
        _request: FixtureRequest,
        _feature: Feature,
        _scenario: Scenario,
        step: Step,
        _step_func: Callable,
        _step_func_args: dict[str, Any],
    ) -> None:
        LogHelper.log_func_name_with_info(step.name, fillchar="\t<-")
        logging.info(" <------------------------------------- after_step")
        # logging.info(request._pyfuncitem)

    def ret_context_info(self, prev: int = 1) -> str:
        if self.show_context:
            return f" (<-by {LogHelper.ret_func_name(prev)}() in {self.ret_classname()})"
        return ""

    def log(
        self,
        msg: str,
        _log_level: int = logging.INFO,
        _pre: str = "",
        _show_caller: bool = False,
    ) -> None:
        logging.info(
            "%s\t%s%s%s", self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info(2)
        )

        logging.info(
            "%s%s%s_1 log: %s",
            self.COL_MSG,
            msg,
            self.COL_CONTEXT,
            self.ret_context_info(1),
        )
        logging.info(
            "%s%s%s__ %s", self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info()
        )

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

    def log_hook(self, msg: str = "") -> None:
        # LogHelper.log_func_name(msg=msg)
        LogHelper.log_func_name_with_info(f"{msg}", prev=1, fillchar="H:")
        # LogHelper.log_func_name(prev=0, fillchar='', msg='ø:'+msg)
        # LogHelper.log_func_name(prev=0, msg='å:'+msg)
        caller = LogHelper.ret_func_name(2)
        logging.info("H: log_hook(): %s%s", self.COL_MSG, caller)

    # def log_func_name(self, prev: int = 0, fillchar: str = None, msg: str = '') -> None:
    #     caller = self.ret_func_name(1)
    #     indent = 1 if fillchar and 'H:' in fillchar else 4
    #     if caller != 'after_scenario':
    #         TEST_CONTEXT[KEY_DBG_FUNC_NAME] = caller    # TODO remove line?
    #     # print('BddTracer -> log_func_name():')
    #     # print('BddTracer -> log_func_name() called from ', ret_func_name(1 + prev))
    #     # super().log(msg, log_level, pre, show_caller)

    #     assert self.show_context, 'No context logging!'
    #     # assert fillchar == ":"
    #     context_info = self.ret_context_info(1 + prev)
    #     # logging.warning('Called by %s', self._ret_func_name(1 + prev))
    #     if fillchar == "H:":
    #         context_info += ' <- with H!'

    #     logging.info(
    #         '%s%s%s %s%s %s %s',
    #         indent * ' ',
    #         self.COL_INFO,
    #         # fillchar != None and fillchar or '->',
    #         fillchar if fillchar else '->',
    #         self.ret_func_name(1 + prev),
    #         self.COL_CONTEXT,
    #         # '' if msg == '' else msg,
    #         msg,
    #         context_info,
    #     )

    # # def ret_filename(self, filepath:str) -> str:
    # # assert filepath != None and filepath.find('\\') != -1, 'No filepath! (Got: %s)'
    # # filename = os.path.basename(__file__)
    # # assert filename != None and filename == "pytest_bdd_tracer.py", 'No filename! (Got: %s)'
    # # return filename
    # # return filepath.split("\\")[-1] # Retrieve the last part after the last '\' character
