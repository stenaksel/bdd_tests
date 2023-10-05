import logging
from pytest_bdd import parsers, given, when, then   # isort:skip

@given(parsers.parse('I have a step with:\n{content}'), target_fixture='text')
def given_text(content: str = None):
    logging.info(f'==> given_text: Given I have a step with:\n{content}')
    assert not content is None, 'content must be provided!'
    # assert content is not None, 'content must be provided!'
    return content


@then('the text should be parsed with correct indentation')
def text_should_be_correct(text: str):
    logging.info(f'==> The text : {text}')
    assert text == 'Some\nExtra\nLines', 'Got: ' + text
