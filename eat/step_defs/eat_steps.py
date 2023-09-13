# pylint: disable=wrong-import-order

from pytest_bdd import parsers, given, when, then  # isort:skip


# @given('there are {int} cucumbers')
@given(parsers.parse('there are {start:d} cucumbers'), target_fixture='cucumbers')
def given_there_are_num_cucumbers(start) -> None:

    cucumbers = {'start': start, 'eat': 0}
    print(f"\n==> function given_there_are_num_cucumbers({start}) (target_fixture='cucumbers')")
    print(f" => 'cucumbers': {cucumbers}")
    return cucumbers


# @when('I eat {int} cucumbers')
@when(parsers.parse('I eat {eat:d} cucumbers'))
def when_i_eat_num_cucumbers(cucumbers, eat) -> None:
    print(f'==> function when_i_eat_num_cucumbers({eat})')
    print(f" => 'cucumbers': {cucumbers}")
    cucumbers['eat'] += eat
    print(f" => 'cucumbers': {cucumbers}")


# @then('I should have {int} cucumbers')
@then(parsers.parse('I should have {left:d} cucumbers'))
def then_i_should_have_num_cucumbers(cucumbers, left) -> None:
    print(f' ==> function then_i_should_have_num_cucumbers({left})')
    print(f"  => 'cucumbers': {cucumbers}")
    assert cucumbers['start'] - cucumbers['eat'] == left
