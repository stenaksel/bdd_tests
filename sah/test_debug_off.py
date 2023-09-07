# content of test_debug_hooks.py
"""
Test file running "debug_hooks.feature"
All steps are in file: debug_hooks_steps.py
"""

from pytest_bdd import scenarios

from .step_defs.debug_off_steps import *

scenarios('./features/debug_off.feature')
