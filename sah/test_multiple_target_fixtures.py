from pytest_bdd import scenarios

from .step_defs.multiple_target_fixtures_steps import *

scenarios('./features/multiple_target_fixtures.feature')
