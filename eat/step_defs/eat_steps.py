# pylint: disable=wrong-import-order
from pytest_bdd.parsers import parse

from tests.common.log_glue import *

# from tests.common.log_glue import log_glue, log_glue_end

from pytest_bdd import given, when, then   # isort:skip


# @given('there are {int} cucumbers')
@given(parse('there are {start:d} cucumbers'), target_fixture='cucumbers')
def given_there_are_num_cucumbers(context, start):
    log_glue(context=context, start=start)

    cucumbers = {'start': start, 'eat': 0}
    print(f"\n==> function given_there_are_num_cucumbers({start}) (target_fixture='cucumbers')")
    print(f" => 'cucumbers': {cucumbers}")
    log_glue_end(context)
    return cucumbers


# @when('I eat {int} cucumbers')
@when(parse('I eat {eat:d} cucumbers'))
def when_i_eat_num_cucumbers(context, cucumbers, eat):
    log_glue(context=context, cucumbers=cucumbers, eat=eat)
    print(f'==> function when_i_eat_num_cucumbers({eat})')
    print(f" => 'cucumbers': {cucumbers}")
    cucumbers['eat'] += eat
    print(f" => 'cucumbers': {cucumbers}")
    log_glue_end(context)


# @then('I should have {int} cucumbers')
@then(parse('I should have {left:d} cucumbers'))
def then_i_should_have_num_cucumbers(context, cucumbers, left):
    log_glue(context=context, cucumbers=cucumbers, left=left)
    print(f' ==> function then_i_should_have_num_cucumbers({left})')
    print(f"  => 'cucumbers': {cucumbers}")
    assert cucumbers['start'] - cucumbers['eat'] == left
    log_glue_end(context)
