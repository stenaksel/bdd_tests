import logging
from logging import DEBUG, INFO, WARN
from typing import Any, Callable

from pytest import Config, FixtureRequest
from pytest_bdd.parser import Feature, Scenario, ScenarioTemplate, Step

from tests.common.log_glue_incl import (  # log_func_name,; log_func_call_info,; ret_before_or_after,; ret_sorted,
    COL_GRAY,
    KEY_CURR_GLUE,
    TEST_CONTEXT,
    assert_object,
    log_feature,
    log_msg_end,
    log_msg_start,
    log_scenario,
    log_step,
    ret_dict_info,
    ret_func_name,
)

# BbbLogger related constants:

# COL_GLUE = '\033[1;36m'
# COL_INFO = '\033[1;34m'
# COL_GRAY = '\033[90m'   # \x1b[90m
# COL_RESET = '\033[0m'   # TODO Remove reset at log end (in normal logging)
# COL_SCENARIO = '\033[1;33m'
# COL_STEP = '\033[1;32m'
# COL_ info:
# ANSI escapes always start with \x1b , or \e , or \033 .
# These are all the same thing: they're just various ways
# of inserting the byte 27 into a string.
# If you look at an ASCII table, 0x1b is literally called ESC.

DO_INCL_CURR_INFO = True

KEY_CURR_FEATURE = 'Current feature'
KEY_CURR_GLUE = 'Current glue'
KEY_CURR_SCENARIO = 'Current scenario'
KEY_CURR_STEP = 'Current step'

KEY_CONTEXT = 'context'
KEY_DBG_FUNC_NAME = 'dbg:func_name'

KEY_FUNC = '|Func'      # TODO Should add all glue functions called
KEY_HOOKS = '|Hooks'    # TODO Should add all hooks called

# TODO Use 'KEY_' Prefix for texts being keys
KEY_STEP_COUNTER = 'step_counter'

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


class BddLogger:
    """
    BddLogger can be used by your conftest.py to log messages from Pytest BDD hooks
    """

    def configure(config: Config) -> None:
        print('configure BddLogger')

    def before_feature(self, _request: FixtureRequest, feature: Feature) -> None:
        """
        Pytest-BDD don't have a seperate hook "pytest_bdd_before_feature".
        So this function will be called by pytest_bdd_before_scenario,
        when the first scenario in the feature is run.
        """
        assert feature and feature.name, 'No feature param!1'
        assert feature is not None and feature.name != '', 'No feature param!2'
        # log_msg('Found feature: ') # + feature.name)
        log_msg_start()
        log_feature(feature)
        log_msg_end()

    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
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

        self.log_msg('-' * 55)

        logging.info('|%s', '_' * 65)
        log_scenario(scenario)
        # assert False, 'Stopping in func: before_scenario'

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
        self.log_msg('----')
        self.log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT0'))
        self.log_msg('----')
        self.log_msg('Resetting TEST_CONTEXT before scenario starts')
        # Reset TEST_CONTEXT before scenario starts
        TEST_CONTEXT = {}
        TEST_CONTEXT[KEY_FUNC] = [
            'before_scenario (always first)'
        ]   # TODO remove: " (always first)"
        TEST_CONTEXT['dbg_log_glue'] = True   # TODO remove line

        logging.info('| TEST_CONTEXT: |')
        self.log_msg('|TEST_CONTEXT 1: |')
        self.log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT1'), INFO, '-1-')
        # logging.info(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT1'))
        self.log_msg('|TEST_CONTEXT 2: |')
        self.log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT2'), INFO, '-2-')
        self.log_msg(ret_dict_info(TEST_CONTEXT, 'TEST_CONTEXT2'))
        self.log_msg('| TEST_CONTEXT _: |')

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

    def before_step(
        self,
        request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        print('-> before_step')
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
        # self.log_msg_end()

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:
    #     print('-> after_feature')

    def after_scenario(self, request: FixtureRequest, feature: Feature, scenario: Scenario) -> None:
        print('-> after_scenario')

    def after_step(
        self,
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

    def log_msg(  # TODO Maybe rename to just "log"
        self, _msg: str, _log_level: int = logging.INFO, _pre: str = '', _show_caller: bool = False
    ) -> None:
        print('-> log_msg')
        #
