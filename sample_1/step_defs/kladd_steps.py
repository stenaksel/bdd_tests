import inspect
import sys
from pprint import pprint

from pytest_bdd import given

# @pytest.mark.hookwrapper
# def pytest_bdd_before_step(request, feature, scenario, step, step_func):
#     print(f"\n ===> Executing step: {step}")


@given('I have na step')
def given_i_have_na_step():
    # caller = sys._getframe().f_back.f_code.co_name
    caller = inspect.currentframe().f_code.co_name   # type: ignore
    # caller = step
    function_name = sys._getframe().f_code.co_name   # pylint: disable=protected-access
    print(f'\n{function_name} ===> I have a step (print) called by: {caller}')
    pprint('{function_name} ===> I have a step (print) called by: {caller}')
