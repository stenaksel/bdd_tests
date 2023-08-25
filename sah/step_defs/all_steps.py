# Content of sah\step_defs\all_steps.py
# from .step_defs.example_steps import *
from pytest_bdd import when
from pytest_bdd.parsers import parse

# from .calculator_steps import *

# from .step_defs.user_details_steps import *


# @given("I have no calculator")
# def given_email_message():
#     print("==> given_email_message <-- I have no calculator")

# from .step_defs.docstring_steps import *

# scenarios("./features/example.feature")

# @given("I have no calculator")
# def given_email_message(context: dict):
#     print("given_email_message " + type(context))
#     assert isinstance(context, dict)
#     for it in context:
#         print(it, context[it])


# @when(parse('{str} performs an {str}'))
# @when(parse('{str} performs another {str}'))
@when(parse('{name} performs an {action}'))
@when(parse('{name} performs another {action}'))
def performs_an_action(name, action):
    # pylint: disable=unused-argument
    # Add Your Code Here
    pass


@when(parse('{name} performs an illegal {action}'))
@when(parse('{name} performs another illegal {action}'))
def performs_an_illegal_action(name, action):
    # pylint: disable=unused-argument
    assert False
