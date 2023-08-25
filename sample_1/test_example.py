from pytest_bdd import scenarios

from .step_defs.example_steps import *

# from .step_defs.kladd_steps import *

scenarios('./features/')
# scenarios("./features/kladd.feature")
# scenarios("./features/another.feature")
