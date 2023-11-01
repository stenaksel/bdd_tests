import logging
from abc import abstractmethod
from typing import Any, Callable, OrderedDict

# from common.log_glue_incl import TEST_CONTEXT

# from common.log_helper import COL_CONTEXT, KEY_CONFIG, KEY_LOG_CONFIG, TEST_CONTEXT, LogHelper
from common.log_helper import KEY_CURR_FEATURE, KEY_MY_HOOKS, KEY_PT_HOOKS, TEST_CONTEXT, LogHelper
from common.pytest_bdd_logger_interface import PytestBddLoggerInterface
from pytest import FixtureRequest
from pytest_bdd.parser import Feature, Scenario, Step

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

    ############################################################################
    ###########################   Abstract methods   ###########################
    ############################################################################

    @abstractmethod
    def log_feature(self, feature: Feature) -> None:
        LogHelper.log_func_name_with_info(feature.name, fillchar='h:\t2->\t ')
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
        LogHelper.log_func_name_with_info(scenario.name, fillchar='_')
        self.log(f'\t {self.COL_SCENARIO}Scenario: "{scenario.name}"')

    @abstractmethod
    def log_step(self, step: Step, scenario: Scenario) -> None:
        LogHelper.log_func_name_with_info(step.name, fillchar='.')

    ############################################################################
    ###   Implementaions of abstract methods from PytestBddLoggerInterface   ###
    ############################################################################

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
        logging.info(' -------------------------------------> before_feature')
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT', prefix='BFe->')
        self.log_hook('*** before_feature ***')
        LogHelper.assert_object_have_name(feature)
        # self._before_feature_assert_params(request, feature)
        caller = LogHelper.ret_func_name(1)  # TODO make better name 2
        logging.info("func 'before_feature' caller '%s'", caller)
        LogHelper.log_func_name_with_info(feature.name, fillchar='h:\t3->\t ')
        # LogHelper.log_func_name(msg=feature.name, fillchar='_')
        # self.log(f'Feature_: "{feature.name}"')
        # LogHelper.log_func_name(fillchar=' _:')

        if request is not None:
            logging.info(request.node)

        # TODO: maybe TEST_CONTEXT[self.KEY_TEST_ITEM] = request.node
        TEST_CONTEXT[KEY_CURR_FEATURE] = feature.name

        print(caller)

        # self.log_hook("pytest_bdd_before_feature - don't exist!")
        LogHelper.log_func_name_with_info(feature.name)
        self.log_feature(feature)
        # LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT-BFe<-')
        self.log_dict(TEST_CONTEXT, 'show TEST_CONTEXT')  # TODO remove. Just testing
        logging.info(' <------------------------------------- before_feature')

    # @abstractmethod #TODO?
    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        logging.info(' -------------------------------------> before_scenario4')
        LogHelper.assert_object_have_name(feature)
        LogHelper.assert_object_have_name(scenario)
        LogHelper.log_func_name_with_info(scenario.name, fillchar='h:\t->\t ')
        # LogHelper.log_func_name(fillchar='  ->', msg=scenario.name)
        LogHelper.log_func_name_with_info(scenario.name, fillchar='h:\t4->\t ')
        # assert request
        # LogHelper.log_func_name(fillchar='\t :')
        # super().before_scenario(request, feature, scenario)
        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - before_scenario'
        # logging.info(' <-------------------------------------')
        self.log_hook(scenario.name)

    def before_step(
        self,
        request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        logging.info(' -------------------------------------> before_step')
        self.log_hook(step.name)

        LogHelper.log_func_name_with_info(step.name, fillchar='h:\t->\t ')

        # assert False, 'Not supposed to pass this point! pytest_bdd_tracer.py - before_step'

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:
    #     print('-> after_feature')

    def after_scenario(self, request: FixtureRequest, feature: Feature, scenario: Scenario) -> None:
        # logging.info('after_scenario <--- %s', __file__)
        # super().after_scenario(request, feature, scenario)
        logging.info(' <------------------------------------- after_scenario')
        self.log_hook(scenario.name)
        logging.info(' <------------------------------------- after_scenario')
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT-AfSc')
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
        self.log_hook(step.name)

        LogHelper.log_func_name_with_info(step.name, fillchar='\t<-')
        logging.info(' <------------------------------------- after_step')
        # logging.info(request._pyfuncitem)

        # ctx = params.get(TXT_CONTEXT)

        # if isinstance(ctx, dict):
        #     if TXT_STEPDEFS in ctx:
        #         ctx[TXT_STEPDEFS].append(glue_function)
        #     else:
        #         ctx[TXT_STEPDEFS] = [glue_function]

    def ret_context_info(self, prev: int = 1) -> str:
        if self.show_context:
            return f' (<-by {LogHelper.ret_func_name(prev)}() in {self.ret_classname()})'
        return ''

    def log(
        self,
        msg: str,
        _log_level: int = logging.INFO,
        _pre: str = '',
        _show_caller: bool = False,
    ) -> None:
        logging.info('%s\t%s%s%s', self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info(2))

        logging.info(
            '%s%s%s_1 log: %s',
            self.COL_MSG,
            msg,
            self.COL_CONTEXT,
            self.ret_context_info(1),
        )
        logging.info('%s%s%s__ %s', self.COL_MSG, msg, self.COL_CONTEXT, self.ret_context_info())

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
        # logging.info('log <--- %s', __file__)

    def _allowed_hook_method_relation(self, from_method: str, to_method: str):
        # Implement the logic for checking if the caller is related to the hook_name
        # You can use any necessary conditions or comparisons here
        # Return True or False based on the result of the check

        return (
            (to_method in from_method)  # example: from 'pytest_bdd_before_step' to 'before_step'
            or (from_method == 'pytest_bdd_before_scenario' and to_method == 'before_feature')
            # because 'pytest_bdd_before_scenario' calls 'before_feature' when first scenario is run
            or ('test_' in from_method)  # we might tast stuff ...
        )

        return True  # Replace this with your actual implementation

    def log_hook(self, msg: str = '') -> None:
        # LogHelper.log_func_name(msg=msg)
        # ? LogHelper.log_func_name_with_info(f"{msg}", prev=1, fillchar="H:")
        # LogHelper.log_func_name(prev=0, fillchar='', msg='ø:'+msg)
        # LogHelper.log_func_name(prev=0, msg='å:'+msg)
        LogHelper.log_func_call_info()
        caller = LogHelper.ret_func_name(1)
        hook_name = LogHelper.ret_func_name(2)
        if caller.startswith('pytest_'):
            # Expected "my" function make the call
            assert False, 'log_hook called directly from a pytest_ hook!'

        assert hook_name.startswith('pytest_') or hook_name.startswith(
            'test_'
        ), f'Unknown hook: {hook_name} with caller {caller}'
        assert self._allowed_hook_method_relation(
            hook_name, caller
        ), f'Caller: {caller} should be related to hook: {hook_name}!'
        param_info = f'msg: "{msg}"'
        logging.info('H: log_hook(%s): %s%s', param_info, self.COL_MSG, caller)

        ctx = TEST_CONTEXT
        assert isinstance(ctx, OrderedDict), f'Unexpected type: {type(ctx)}'
        logging.info('log_hook 1 ------------------>')
        logging.info('[KEY_PT_HOOKS]: %s', ctx.get(KEY_PT_HOOKS, []))
        logging.info('[KEY_MY_HOOKS]: %s', ctx.get(KEY_MY_HOOKS, []))

        if KEY_PT_HOOKS in ctx:
            assert (
                type(ctx[KEY_PT_HOOKS]) == list
            ), f'Expected KEY_HOOKS to be a list, not a {type(ctx[KEY_PT_HOOKS]).__name__}'
            # assert False, f'Not supposed to pass this point! pytest_bdd_tracer.py - log_hook (Caller: {caller})'
            ctx[KEY_PT_HOOKS].append(hook_name)
            ctx[KEY_MY_HOOKS].append(caller)
        else:
            logging.warning('log_hook 2 ------------------>')
            ctx[KEY_PT_HOOKS] = [hook_name]
            ctx[KEY_MY_HOOKS] = [caller]

        logging.warning('log_hook 3 ------------------>')
        logging.warning('[KEY_PT_HOOKS]: %s', ctx.get(KEY_PT_HOOKS, []))
        logging.warning('[KEY_MY_HOOKS]: %s', ctx.get(KEY_MY_HOOKS, []))

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
    #     # logging.info('Called by %s', self._ret_func_name(1 + prev))
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
