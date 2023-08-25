# content of article/steps.py
import inspect

from tests.common.log_glue import log_glue, log_glue_end

from pytest_bdd import given, when, then   # isort:skip


def _step_def():
    calling_function = inspect.stack()[2][3]
    print('This function was called by: ' + calling_function)


# @given('a step without context')
# def a_step_witout_context():
#     log_glue()
#     log_glue_end()


# @given('a given step')
# def a_given_step(context, request):
#     print(f'\n==> "{request.node.parent.name}" > "{request.node.name}()"')
#     # print(context)
#     print(f'==> (article/steps.py)\n{log_glue(context, request)}')
#     # assert context['steps'], 'Found no steps key in context'
#     assert len(context['steps']) == 0, 'Dictionary steps is NOT empty'
#     log_glue_end(context)
#     # exit_step_def(context, '<\t\t ')
#     # context['steps'].append('a_given_step')
#     # print(f'<\t\t context=>{context}')


# @when('a when step')
# def a_when_step(context):
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
def a_then_step(context):
    print(f' ==> function a_then_step() (article/steps.py) --> context: {context})')
    print(f'xxx==> {inspect.currentframe().f_code.co_name}:')
    context['result'] = context['info']
    context['steps'].append('a_then_step')
    # assert context.result == context.info
    the_result = context['result']
    assert the_result == context['info']
    assert the_result == 'some info'


# @given('I have a fbar', target_fixture='fbar')
# def given_i_have_a_fbar(context):
#     print(f'\n==> Given I have a fbar (article/steps.py)\n\t==> context: {context}')
#     print(context)
#     # print(f'Step: {context.scenario.feature.name}
#     # - {context.scenario.name} - {context.step.name}')
#     return 'bar'


# @then('bar should have value "bar"')
# def then_bar_should_have_value(fbar):
#     print('==> Then bar should have value "bar" (article/steps.py)')
#     assert fbar == 'bar'


# @given('I do have a step')
@given('!I do have a step')
def given_i_do_have_a_step(context):
    print(f'Step: {context.scenario.feature.name} \n')
    print(f'\t-> {context.scenario.name} \n\t--> {context.step.name}\n')


@given('Im an author user')
@given("I'm an author user")
def author_user(context, author):
    print(f'==> author_user \n\t{context}\n\t{author}\n')
    context['user'] = author
    print(f'==> author_user \n\t{context}\n\t{author}\n')


@given('I have injecting given', target_fixture='strfoo')
def injecting_given() -> str:
    log_glue()
    log_glue_end(None)
    return 'injected strfoo'


@then('foo should be "injected foo"')
def foo_is_foo(strfoo: str):
    log_glue(strfoo=strfoo)
    assert strfoo == 'injected strfoo'
    log_glue_end(None)


# @fixture
# def author():
#     return 'sah'
#     # return 'Sten Aksel Heien'


@given('I have an article', target_fixture='farticle')
def i_have_an_article(author: str = 'Selveste') -> str:
    log_glue(author=author)
    ret = create_test_article(author_name=author)
    log_glue_end(author)
    return ret


@when('I go to the article page')
def i_go_to_the_article_page(farticle: str):
    # def _(browser, article):
    # browser.visit(urljoin(browser.url, '/articles/{0}/'.format(article.id)))
    # ---
    log_glue(farticle=farticle)
    assert farticle.islower, 'The passed article was NOT in lowercase!'
    log_glue_end(farticle)


@then('I should not see the error message')
def i_should_see():
    log_glue()
    print('I should not see the error message')
    log_glue_end()


# def _(browser):
#     with pytest.raises(ElementDoesNotExist):
#         browser.find_by_css('.message.error').first


@given('I have a beautiful article')
def _(article: str):
    log_glue(article=article)
    print(f'I have a beautiful article {article}')
    log_glue_end(None)


def create_test_article(author_name: str) -> str:
    return 'article by author: ' + author_name
