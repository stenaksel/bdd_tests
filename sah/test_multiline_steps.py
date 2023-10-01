from pytest_bdd import scenarios

from .step_defs.multiline_steps import *

scenarios('./features/multiline_steps.feature')


