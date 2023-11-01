import logging

from common.log_helper import (
    COL_CONTEXT,
    COL_INFO,
    COL_SCENARIO,
    COL_STEP,
    DO_INCL_CURR_INFO,
    KEY_CURR_STEP,
    KEY_STEP_COUNTER,
    TEST_CONTEXT,
    LogHelper,
)
from common.pytest_bdd_tracer import PytestBddTracer
from pytest_bdd.parser import Feature  # , Scenario, ScenarioTemplate, Step
from pytest_bdd.parser import Scenario, Step

############################################################################


class PytestBddLogger(PytestBddTracer):
    """
    PytestBddLogger is a concrete class for logging Pytest BDD testing.
    It implements abstract PytestBddTracer methods.
    #TODO: You may pass a False value to the constructor to disable "context logging".
    """

    # TODO: You may pass a False value to the constructor to disable "context logging".

    def __init__(self, show_context: bool = True):
        super().__init__(show_context)  # This should be OK....?
        # TODO self.show_context = show_context

    ############################################################################
    ### Implementaions of abstract methods from PytestBddTracer
    ############################################################################
    def xlog_feature(self, feature: Feature) -> None:
        LogHelper.log_func_name_with_info(feature.name, fillchar='@')
        super().log_feature(feature)  # TODO: don't use super()
        LogHelper.assert_object_have_name(feature)
        # logging.info('|%s', '=' * 75)
        # logging.info('| Feature: %s', feature.name)
        # logging.info('|%s', '=' * 75)
        feature_name = f'Feature: {feature.name}'
        LogHelper.log_func_call_info(logging.INFO, -1, feature_name)
        logging.info('%s', '/' * 75)
        logging.info('|%s|', ' ' * 73)
        logging.info('|%s|', feature_name.center(73))
        logging.info('|%s|', ' ' * 73)
        logging.info('%s', '\\' * 75)
        # log_msg_end()

    def log_feature(self, feature: Feature) -> None:
        LogHelper.log_func_name_with_info(feature.name, fillchar='F:')
        # super().log_feature(feature)  # TODO: don't use super() ?
        LogHelper.assert_object_have_name(feature)
        self.log(f'\t {self.COL_MSG}Feature: "{feature.name}"')
        # logging.info(
        #     f'%sFeature: "%s" %s',
        #     self.COL_MSG,
        #     feature.name,
        #     self.ret_context_info(1)
        # )
        # ret_context = self.get_context_info()

        # self.assert_object_have_name(feature)
        # self.assert_object_have_name(scenario)
        # self._assert_objassert_object_have_name_named(step)

    def log_scenario(self, scenario: Scenario) -> None:
        LogHelper.log_func_name_with_info(scenario.name, fillchar='Sc:')
        self.log(f'\t {self.COL_SCENARIO}Scenario: "{scenario.name}"')

    def log_step(self, step: Step, scenario: Scenario) -> None:
        LogHelper.log_func_name_with_info(step.name, fillchar='St:')
        LogHelper.assert_object_have_name(step)
        LogHelper.assert_object_have_name(scenario)
        caller: str = LogHelper.ret_func_name(1)
        logging.info('=> log_step(step, scenario) (<< "%s") ', caller)  # TODO debug
        logging.info(
            '\t%s Scenario: %s%s%s (in Feature: "%s") (<< log_step)',  # TODO -> debug
            LogHelper.ret_before_or_after(caller),
            COL_SCENARIO,
            scenario.name,
            COL_CONTEXT,
            scenario.feature.name,
        )
        logging.info(
            '\t%s%s Step: %s %s(<< log_step)',  # TODO -> debug
            LogHelper.ret_before_or_after(caller),
            COL_STEP,
            step.name,
            COL_CONTEXT,
        )

        global TEST_CONTEXT  # pylint: disable=global-statement

        # logging.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT5', '---->'))
        logging.info('log_step ------------------------------------------->')
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT5', '---->')

        step_no = TEST_CONTEXT.get(KEY_STEP_COUNTER, 0)
        if step_no == 0:
            logging.info('\t- %s: %s', KEY_STEP_COUNTER, step_no)

        # logging.info('%sStep:\t"%s"', X_COL_STEP, step.name)
        logging.info('\t- %s: %s', KEY_STEP_COUNTER, step_no)
        logging.info('\t- step_no     : %s', step_no)
        logging.info('\t- name        : %s', step.name)
        logging.info('\t- type        : %s', step.type)
        logging.info('\t- keyword     : %s', step.keyword)
        if step.background:
            # logging.info('\t- background  : %s', step.background)
            logging.info('\t- background  : -yes-')
        else:
            logging.info('\t- background  : -NO-')
        logging.info('\t- line_number : %s', step.line_number)
        logging.info('\t- lines       : %s', step.lines)
        # logging.debug('\t- lines      : %s', step.lines[0])
        logging.info('Step Background >>#######################################>>')
        # ? logging.info(step.background)
        logging.info('Step Background <<#######################################<<')
        assert isinstance(TEST_CONTEXT, dict)
        LogHelper.log_dict_now(TEST_CONTEXT, 'TEST_CONTEXT', '---->')
        step_no += 1
        step_text = f'{step.keyword} {step.name}'
        line = '-' * (20 + len(step_text))
        logging.info(line)
        logging.info(LogHelper.ret_before_or_after(caller))
        logging.info('step_no=%s', step_no)
        # logging.info('step_no=%s', step_no)
        # logging.warning('step_no=%s', step_no)
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

        logging.info(
            '\t%s) %s%s %s',
            step_no,
            COL_STEP,
            step_text,
            f'{COL_INFO}(@{step.line_number})',
        )
        logging.info('DO_INCL_CURR_INFO=%s', DO_INCL_CURR_INFO)
        if DO_INCL_CURR_INFO:
            assert isinstance(TEST_CONTEXT, dict)
            TEST_CONTEXT[KEY_CURR_STEP] = step_text
            TEST_CONTEXT = dict(sorted(TEST_CONTEXT.items()))
            logging.info(LogHelper.ret_dict_info(TEST_CONTEXT, '< TEST_CONTEXT', ''))

        logging.info('log_step <-------------------------------------------')

    # def after_step(request, feature, scenario, step, step_func, step_func_args) -> None:
    #     logging.info('----> Entered after_step')
    #     logging.info(ret_dict_info(step_func_args, 'step_func_args'))
