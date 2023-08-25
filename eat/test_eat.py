# content of test_eat.py
"""
Test file running "eating.feature"
All steps are in file: eat_steps.py
"""
from pytest_bdd import scenarios

from .step_defs.eat_steps import *

scenarios('./features/eating.feature')
