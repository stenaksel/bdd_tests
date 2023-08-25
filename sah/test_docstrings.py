from pytest_bdd import scenarios
from .step_defs.docstring_steps import *

scenarios('./features/docstrings.feature')
