# content of article/steps.py
import inspect

from pytest_bdd import given, when, then   # isort:skip


def _step_def() -> None:
    calling_function = inspect.stack()[2][3]
    print('This function was called by: ' + calling_function)


# @given('a step without context')
# def a_step_witout_context() -> None:
#     pass


# @given('a given step')
# def a_given_step(context, request) -> None:
#     print(f'\n==> "{request.node.parent.name}" > "{request.node.name}()"')
#     # print(context)
#     print(f'==> (article/steps.py)\n{log_glue(context, request)}')
#     # assert context['steps'], 'Found no steps key in context'
#     assert len(context['steps']) == 0, 'Dictionary steps is NOT empty'
#     # exit_step_def(context, '<\t\t ')
#     # context['steps'].append('a_given_step')
#     # print(f'<\t\t context=>{context}')


# @when('a when step')
# def a_when_step(context) -> None:
#     print(f'==> (article/steps.py)\n{log_glue(context)}')
#     assert context['steps'], 'Dictionary "steps" was not found in context!'
#     assert len(context['steps']) == 1   # Dictionary is empty
#     assert 'a_given_step' in context['steps'], "Key 'a_given_step' not found in steps"
#     context['when_info'] = 'some info'
#     assert context['info'] == 'some info'

#     context['steps'].append('a_when_step')
#     print(f'<\t\t context=>{context}')
#     print(f'<-- a_given_step\n\tcontext = {context}')


@then('a then step')
@then('some then step')
def a_then_step(context) -> None:
    print(f' ==> function a_then_step() (article/steps.py) --> context: {context})')
    print(f'xxx==> {inspect.currentframe().f_code.co_name}:')
    context['result'] = context['info']
    context['steps'].append('a_then_step')
    # assert context.result == context.info
    the_result = context['result']
    assert the_result == context['info']
    assert the_result == 'some info'


# @given('I have a fbar', target_fixture='fbar')
# def given_i_have_a_fbar(context) -> None:
#     print(f'\n==> Given I have a fbar (article/steps.py)\n\t==> context: {context}')
#     print(context)
#     # print(f'Step: {context.scenario.feature.name}
#     # - {context.scenario.name} - {context.step.name}')
#     return 'bar'


# @then('bar should have value "bar"')
# def then_bar_should_have_value(fbar) -> None:
#     print("==> Then bar should have value "bar" (article/steps.py)")
#     assert fbar == 'bar'


# @given('I do have a step')
@given('!I do have a step')
def given_i_do_have_a_step(context) -> None:
    print(f'Step: {context.scenario.feature.name} \n')
    print(f'\t-> {context.scenario.name} \n\t--> {context.step.name}\n')


@given('Im an author user')
@given("I'm an author user")    # TODO Find out why this isn't working
def author_user(context, author) -> None:
    print(f'==> author_user \n\t{context}\n\t{author}\n')
    context['user'] = author
    print(f'==> author_user \n\t{context}\n\t{author}\n')


@given('I have injecting given', target_fixture='strfoo')
def injecting_given() -> str:
    return 'injected strfoo'


@then('foo should be "injected foo"')
def foo_is_foo(strfoo: str) -> None:
    assert strfoo == 'injected strfoo'


@given('I have an article', target_fixture='farticle')
def i_have_an_article(author: str = 'Selveste') -> str:
    ret = create_test_article(author_name=author)
    return ret


@when('I go to the article page')
def i_go_to_the_article_page(farticle: str) -> None:
    # def _(browser, article):
    # browser.visit(urljoin(browser.url, '/articles/{0}/'.format(article.id)))
    # ---
    assert farticle.islower, 'The passed article was NOT in lowercase!'


@then('I should not see the error message')
def i_should_see() -> None:
    print('I should not see the error message')


def create_test_article(author_name: str) -> str:
    return 'article by author: ' + author_name
