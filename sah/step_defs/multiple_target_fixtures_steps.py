from pytest_bdd import given, then, parsers
from pytest_bdd.utils import dump_obj

# scenarios("./features/multiple_target_fixtures.feature")


@given(parsers.parse('there is a foo with value "{value}"'), target_fixture='foo')
@given(parsers.parse('there is a bar with value "{value}"'), target_fixture='bar')
def _(value):
    return value


@then(parsers.parse('foo should be "{expected_value}"'))
def _(foo, expected_value):
    dump_obj(foo)
    assert foo == expected_value


@then(parsers.parse('bar should be "{expected_value}"'))
def _(bar, expected_value):
    dump_obj(bar)
    assert bar == expected_value
