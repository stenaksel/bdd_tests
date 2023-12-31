from pytest_bdd import when
from pytest_bdd.parsers import parse


@when(parsers.parse('{name} performs an {action}'))
def step_function(name, action):
    # pylint: disable=unused-argument
    print(f'step_function({name}, {action})')
    # Add Your Code Here
    pass
