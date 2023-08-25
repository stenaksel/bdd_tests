# content of test_calculator.py
"""
Test file running "calculator.feature"
All steps are in file: calculator_steps.py
"""

from pytest_bdd import scenarios

from .step_defs.calculator_steps import *

scenarios('./features/calculator.feature')
