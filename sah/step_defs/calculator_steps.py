import logging

from pytest_bdd import given, then, when
from pytest_bdd.parsers import parse

from tests.common.log_glue import *
from tests.common.log_glue_incl import DBG_LOG_PARAMS

# pylint: disable=invalid-name ## ( => sah: using "it" )


@given('I have a simple calculator')
def given_i_have_a_simple_calculator():
    logging.info('given_i_have_a_simple_calculator')


@given('I have a calculator')
def given_i_have_a_calculator(context):
    # context[KEY_DBG_LOG_GLUE] = True
    context[DBG_LOG_PARAMS] = True
    # logging.info('dbg ----------------------------------')
    # logging.info('0. case: glue function without any parameters (no context):')
    # log_glue()
    # logging.info('1a. case: glue function with a context (but no other params):')
    # log_glue(context)
    logging.info('dbg >----------------------------------')
    # logging.info('1b. case: glue function with a context (but no other params):')
    TODO: log_glue(context=context)
    # log_glue(context=context, KEY_DBG_LOG_GLUE=True, DBG_LOG_PARAMS=True)
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

    log_glue_end(context)
    # logging.info('. case: context end:')
    # logging.info(context)
    # for key in context:
    #     logging.info(key, ' =: ', context[key])

    # log_glue_end(context)


# @when('I add {int} and {int}')
@when(parse('I add {num1:d} and {num2:d}'))
def when_i_add_num1_and_num2(context, num1, num2):
    # logging.info('0. case: when_i_add_num1_and_num2 => %s & %s', num1, num2)
    # # log_glue(context=context, num1=num1, num2=num2, KEY_DBG_LOG_GLUE=True, DBG_LOG_PARAMS=True)
    log_glue(context=context, num1=num1, num2=num2)
    context['sum'] = num1 + num2
    # context.update({'sum': (num1 + num2)})
    # logging.info('sum now: %s', context['sum'])
    log_glue_end(context)
    # logging.info('. case: context end:')
    # logging.info(context)


# @then('the result should be {int}')
@then(parse('the result should be {total:d}'))
def then_result_should_be(context, total: int):
    # log_glue(context=context, total=total, KEY_DBG_LOG_GLUE=True, DBG_LOG_PARAMS=True)
    log_glue(context=context, total=total, DBG_LOG_PARAMS=True)
    logging.debug(ret_dict_info('context', context, '----'))

    for it in context:
        logging.info('then_result_should_be\tit=%s, value=%s', it, context[it])
        assert context['sum'] == total

    log_glue_end(context)
    # logging.info('. case: context end:')
    # logging.info(context)