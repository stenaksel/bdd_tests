# content of test_debug_glue.py
"""
Test file running "debug_glue.feature"
All steps are in file: debug_glue_steps.py
"""

from pytest_bdd import scenarios

from .step_defs.debug_glue_steps import *

scenarios('./features/debug_glue.feature')
