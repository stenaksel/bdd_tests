# import pytest

from pytest_bdd import given, scenarios
from pytest_bdd.parsers import parse

# from .step_defs.current_steps import *


scenarios('./features/test_current.feature')


# Define a given step with access to current feature
@given(parse("I have a feature named '{feature_name}'"))
def given_current_feature(pytestconfig, feature_name):
    print("I have a feature named 'test_current.feature'")
    current_feature = pytestconfig.getoption('--feature')
    print(pytestconfig)
    print(current_feature)
    # assert current_feature == feature_name, f"Current feature is {current_feature}"
