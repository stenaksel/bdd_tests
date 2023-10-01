from pytest_bdd import parsers, given, when, then   # isort:skip

# @given('I have a step with:\n{str}'), target_fixture="text")
@given('I have a step with:', target_fixture="text")
# @given(parsers.parse("I have a step with:\n{content}"), target_fixture="text")
def given_text(content):
    assert content is not None, 'content must be provided!'
    return content


@then("the text should be parsed with correct indentation")
def text_should_be_correct(text):
    assert text == "Some\nExtra\nLines"
