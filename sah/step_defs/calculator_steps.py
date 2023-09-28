import logging

# from tests.common.log_glue import *
from tests.common.log_glue_incl import old_ret_dict_info

from pytest_bdd import parsers, given, when, then   # isort:skip


# pylint: disable=invalid-name ## ( => sah: using "it" )


@given('I have a simple calculator')
def given_i_have_a_simple_calculator() -> None:
    logging.info('given_i_have_a_simple_calculator')


@given('I have a calculator')
def given_i_have_a_calculator(context) -> None:
    logging.info('given_i_have_a_calculator context: %s', context)
    # logging.info('dbg ----------------------------------')
    # logging.info('0. case: glue function without any parameters (no context):')
    # log_glue()
    # logging.info('1a. case: glue function with a context (but no other params):')
    # log_glue(context)
    logging.info('dbg >----------------------------------')
    # logging.info('1b. case: glue function with a context (but no other params):')
    # TODO: xlog_glue(context=context)
    logging.info('dbg <----------------------------------')
    # logging.info('2. case: glue function with a context and other params:')
    # param2 = '2some'
    # param3 = '3some'
    # log_glue(context=context, p2=param2, p3=param3)
    # logging.info('dbg ----------------------------------')
    # logging.info('Hysj4')
    # logging.info('dbg ----------------------------------')
    # for key in context:
    #     logging.info(key, ' = ', context[key])
    # logging.info('dbg ----------------------------------')
    # logging.info('Hysj5')

    # xlog_glue_end(context)


# @when('I add {int} and {int}')
@when(parsers.parse('I add {num1:d} and {num2:d}'))
def when_i_add_num1_and_num2(context, num1, num2) -> None:
    # logging.info('0. case: when_i_add_num1_and_num2 => %s & %s', num1, num2)
    # xlog_glue(context=context, num1=num1, num2=num2)
    context['sum'] = num1 + num2
    # xlog_glue_end(context)


# @then('the result should be {int}')
@then(parsers.parse('the result should be {total:d}'))
def then_result_should_be(context, total: int) -> None:
    logging.debug(old_ret_dict_info(context, 'context', '----'))

    for it in context:
        logging.info('then_result_should_be\tit=%s, value=%s', it, context[it])
        assert context['sum'] == total

    # xlog_glue_end(context)
