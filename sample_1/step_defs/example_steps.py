from pytest_bdd import parsers, when


@when(parsers.parse('{name} performs an {action}'))
def step_function(name, action) -> None:
    # pylint: disable=unused-argument
    print(f'step_function({name}, {action})')
    # Add Your Code Here
    pass
