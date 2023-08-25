# from .step_defs.all_steps import *
from pytest_bdd import scenarios

from .step_defs.all_steps import *

# from .step_defs.all_steps import *
# editor.action.commentLine
# editor.action.blockComment

# scenarios("./features/")
scenarios('./features/example.feature')
