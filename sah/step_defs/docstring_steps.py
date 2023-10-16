import inspect
import logging
import pprint
from pprint import pprint

from pytest_bdd.utils import dump_obj

from pytest_bdd import parsers, given, when, then   # isort:skip


# pytest --fixtures
# TODO Investigate fixtures cache, caplog doctest_namespace,
# TODO Investigate pytestbdd fixtures: pytestbdd_stepdef_given_trace, ++


@given(parsers.parse('I have no message:'))
def given_i_have_a_message0(context) -> None:
    assert context is not None, 'context must be provided!'


# @given('I have a message:')
@given(parsers.parse('I have a message:\n{doc_string}'))
# def given_i_have_a_message(context, doc_string: str = None) -> None:
def given_i_have_a_message(context, doc_string: str) -> None:
    assert context is not None, 'context must be provided!'
    # log_glue(context=context, scenario=given_i_have_a_message.scenario)
    # dok_str = given_i_have_a_message.scenario.feature.scenarios[0].docstring
    # xlog_glue(context=context, dok_str=dok_str)
    # context['message'] = doc_string
    if doc_string is not None:
        pprint(doc_string)
        num_lines = len(doc_string.split('\n'))
        pprint(num_lines)
        print(f'\n\tdok_str:  {doc_string}\n')
        assert '"""' not in doc_string, 'The dok_str contains: """'
        print(f'\tthe context: {context}\n\tdok_str:  {doc_string}\n')
        pprint(doc_string)
        context['message'] = doc_string   # .text
    # endif


def print_function_name() -> None:
    print(inspect.currentframe().f_code.co_name)


@given('I have a step without a doc string:')
def given_i_have_step_without_a_doc_string(context, doc_string: str = None) -> None:

    print('==> given_i_have_step_without_a_doc_string:\n')
    logging.info('given_i_have_step_without_a_doc_string:\n\t context:')
    logging.info('----------')
    dump_obj(doc_string)
    logging.info('----------')
    assert doc_string is None, 'Not supposed to be handed a DocString, but got one!' + doc_string
    print(f'\tthe context: {context}\n\tdoc_string:  {doc_string}\n')


# @given('I have a step with a doc string:')
@given(parsers.parse('I have a step with a doc string:\n{doc_string}'))
def given_i_have_step_with_a_docstring(context, doc_string: str) -> None:
    print('==> given_i_have_step_with_a_docstring:\n')
    assert doc_string is not None, 'doc_string must be provided!'
    print(f'\tthe context: {context}\n\tdoc_string:  {doc_string}\n')
    # xlog_glue(context=context)
    pprint(doc_string)
    # assert 'This is a test message.' in doc_string
    # Put doc_string into context.doc_string
    context['message'] = doc_string   # .text
    # xlog_glue_end(context)
    # assert False, 'Not supposed to pass this point! bdd_tracer.py - docstring_steps.py - given_i_have_step_with_a_docstring'

@given('the doc string don\'t contain any lines')
def the_doc_string_dont_contain_any_lines(context) -> None:
    pass


@when('I ask for how many lines the doc string have')
@when('I ask for how many lines the message have')
def when_i_ask_for_how_many_lines_the_message_have(context) -> None:
    print('==> when_i_ask_for_how_many_lines_the_message_have:\n')
    print(f'\tthe context: {context}\n')
    return
    # xlog_glue(context=context)
    num_lines = 0
    try:
        message = context.get('message', None)
        # assert message is not None, 'No message in the context!'
        if message is not None:   # Found a message in the context!
            logging.info(message)
            # logging.info(message.splitlines())
            # num_lines = len(message.splitlines())
            print('message have %s lines', message.count('\n'))
            num_lines = 1 + message.count('\n')
        # endif

        logging.info('message have %d lines', num_lines)
    except KeyError as err:
        print('KeyError exception occurred:', err)
        message = None

    # Put result into context.num_lines
    context['num_lines'] = num_lines
    print(f'\tnum_lines: {num_lines}')
    # xlog_glue_end(context)


# @then('I should be told it was {int} line')
# @then('I should be told it was {int} lines')
@then('I should be told it was no lines (because the doc string was missing)')
@then(parsers.parse('I should be told it was {expected_num:d} line'))
@then(parsers.parse('I should be told it was {expected_num:d} lines'))
def then_i_should_be_told_it_was_n_lines(context, expected_num: int = -1) -> None:
    num_lines = context.get('num_lines', -1)
    logging.info('expected_num: %s (%s)', expected_num, type(expected_num).__name__)
    logging.info('num_lines: %s', num_lines)
    assert num_lines is not None, 'No num_lines in the context!'
    assert isinstance(num_lines, int)
    assert isinstance(expected_num, int)
    assert num_lines == expected_num, f'num_lines ({num_lines}) != expected_num ({expected_num})'


# @then(parsers.parse('Details related to incident will be returned:\n{content}'))
# # def the_incident_returns(response, content) -> None:
# def the_incident_returns(content) -> None:
#     print(f'Feature file content: {content}')   # Prints the thing from the feature file
#     log_glue(content=content)
#     # assert response.status_code == status.HTTP_200_OK
#     # xlog_glue_end()


@given('I have an email address "{email_address}"')
def given_email_address(context, email_address: str) -> None:
    # xlog_glue(context=context)
    context['email_address'] = email_address
    # xlog_glue_end(context)


@when('I send the message to the email address')
def when_send_message_to_email(context) -> None:
    # xlog_glue(context=context)
    email_address = context['email_address']
    message = context['message']
    pprint("\n'{email_address}' gets sent the message:\n {message}\n")
    pprint(email_address)
    pprint(message)
    # TO DO: do something to send the message to the email address
    # xlog_glue_end(context)


@then('the message should be delivered successfully')
def then_message_delivered_successfully(context) -> None:
    # xlog_glue(context=context)
    # xlog_glue_end(context)
    pass
