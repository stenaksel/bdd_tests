import inspect
import pprint
import sys
from pprint import pprint
from types import FrameType

# from parsers import parse
from pytest_bdd import parsers, given, when, then   # isort:skip

from tests.common.log_glue import xlog_glue, xlog_glue_end

# pytest --fixtures
# TODO Investigate fixtures cache, caplog doctest_namespace,
# TODO Investigate pytestbdd fixtures: pytestbdd_stepdef_given_trace, ++


@given('I have a step without a message')
def given_i_have_a_step_without_a_message(context):
    xlog_glue(context=context)
    # context['message'] = None
    xlog_glue_end(context)


# @given('I have a message:')
@then(parsers.parse('I have a message:{dok_str}'))
def given_i_have_a_message_x(context, dok_str: str):
    # log_glue(context=context, scenario=given_i_have_a_message.scenario)
    # dok_str = given_i_have_a_message.scenario.feature.scenarios[0].docstring
    xlog_glue(context=context, dok_str=dok_str)
    pprint(dok_str)
    num_lines = len(dok_str.split('\n'))
    pprint(num_lines)
    print(f'\n\tdok_str:  {dok_str}\n')
    assert '"""' not in dok_str, 'The dok_str contains: """'
    print(f'\tthe context: {context}\n\tdok_str:  {dok_str}\n')
    pprint(dok_str)
    context['message'] = dok_str   # .text


def print_function_name():
    print(inspect.currentframe().f_code.co_name)


@given('I have step with no Docstring')  # Hint: no ':' in the end => no docstring
def given_i_have_step_with_no_docstring(context):
    print('==> given_i_have_step_with_no_docstring:\n')
    print(f'==> {inspect.currentframe().f_code.co_name}:\n')
    print(f'==> {print_function_name()}:\n')
    print(f'\tthe context: {context}\n\tdoc_string:  N/A\n')
    step_info = 'I have step with no Docstring'
    caller_frame: FrameType | None = inspect.currentframe()
    assert caller_frame is not None
    caller = caller_frame.f_code.co_name

    function_name = sys._getframe().f_code.co_name   # pylint: disable=protected-access
    print(f'\n{function_name} ===> {step_info} (print) called by: {caller}\n')
    # raise NotImplementedError


# @given('I have step with a Docstring:{str}')
@given(parsers.parse('I have step with a Docstring:{doc_string}'))
def given_i_have_step_with_a_docstring(context, doc_string: str):
    print('==> given_i_have_step_with_a_docstring:\n')
    print(f'\tthe context: {context}\n\tdoc_string:  {doc_string}\n')
    xlog_glue(context=context)
    pprint(doc_string)
    assert 'This is a test message.' in doc_string
    # Put doc_string into context.doc_string
    context['message'] = doc_string   # .text
    xlog_glue_end(context)


@when('I ask for how many lines the message have')
def when_i_ask_for_how_many_lines_the_message_have(context):
    print('==> when_i_ask_for_how_many_lines_the_message_have:\n')
    print(f'\tthe context: {context}\n')
    xlog_glue(context=context)
    num_lines = 0
    try:
        message = context['message']
        num_lines = len(message.split('\n'))
    except KeyError as err:
        print('KeyError exception occurred:', err)
        message = None

    # assert message is not None, "Coundn't find a message in the context!"
    # Put result into context.num_lines
    context['num_lines'] = num_lines
    xlog_glue_end(context)


# @then('I should be told it was {int} line')
# @then('I should be told it was {int} lines')
@then(parsers.parse('I should be told it was {expected_num:d} line'))
@then(parsers.parse('I should be told it was {expected_num:d} lines'))
def then_i_should_be_told_it_was_1_line(context, expected_num: int):
    xlog_glue(context=context, expected_num=expected_num)
    assert context['num_lines'] is not None
    num_lines = context['num_lines']
    assert isinstance(num_lines, int)
    assert isinstance(expected_num, int)
    assert num_lines == expected_num, f'num_lines ({num_lines}) != expected_num ({expected_num})'
    xlog_glue_end(context)


# @then(parsers.parse('Details related to incident will be returned:\n{content}'))
# # def the_incident_returns(response, content):
# def the_incident_returns(content):
#     print(f'Feature file content: {content}')   # Prints the thing from the feature file
#     log_glue(content=content)
#     # assert response.status_code == status.HTTP_200_OK
#     xlog_glue_end()


@given('I have an email address "{email_address}"')
def given_email_address(context, email_address: str):
    xlog_glue(context=context)
    context['email_address'] = email_address
    xlog_glue_end(context)


@when('I send the message to the email address')
def when_send_message_to_email(context):
    xlog_glue(context=context)
    email_address = context['email_address']
    message = context['message']
    pprint("\n'{email_address}' gets sent the message:\n {message}\n")
    pprint(email_address)
    pprint(message)
    # TO DO: do something to send the message to the email address
    xlog_glue_end(context)


@then('the message should be delivered successfully')
def then_message_delivered_successfully(context):
    xlog_glue(context=context)
    xlog_glue_end(context)
