# Content of sah\step_defs\all_steps.py
# from .step_defs.example_steps import *
from pytest_bdd import parsers, when


# @when(parsers.parse('"{name}" performs an "{action}"'))
# @when(parsers.parse('"{name}" performs another "{action}"'))
# def performs_an_action(name, action):
#     # pylint: disable=unused-argument
#     # Add Your Code Here
#     pass


@when(parsers.parse('{name} performs an illegal {action}'))
@when(parsers.parse('{name} performs another illegal {action}'))
def performs_an_illegal_action(name, action):
    # pylint: disable=unused-argument
    assert False
