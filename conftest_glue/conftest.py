# content of conftest_glue/conftest.py
# import inspect
# import logging
# import pprint

import pytest

from pytest_bdd import parsers, given, when, then  # isort:skip


# conftest.py is a special file in pytest that allows you to define fixtures,
# hooks, and other shared code that can be used across multiple test files.
# So it is allowed to declare glue as shared code in conftest.py
# (The glue code here is not "shared", but just examples of the possibility)


@given(parsers.parse('I have a key {key} in the context'))
def given_i_have_a_bar_key_in(context, key) -> str:
    context[key] = 'bar-context'
    print(f'\n\t<== context: {context}')
    return 'bar'


@given('I have a target_fixture {str}', target_fixture='bar')
def given_i_have_a_target_fixture_bar(context) -> str:
    print('\n==> Given I have a target_fixture')
    print(f'\t==> context: {context}')
    print('==> given_i_have_a_target_fixture_bar  (conftest_glue/conftest.py)')
    context['bar'] = 'bar'
    # print(f'Step: {context.scenario.feature.name}
    # - {context.scenario.name} - {context.step.name}')
    return 'bar-target_fixture'


@when('I do nothing')
def _() -> None:
    print('\n==> I do nothing _  (conftest_glue/conftest.py)\n')


# @then('{str} bar should have value "{str}"')
@then(parsers.parse('{what} bar should have value "{str_value}"'))
def then_bar_should_have_value(context, what: str, str_value: str) -> None:
    print(f"==> Then '{what}' should have value '${str_value}'")
    print('==> then_bar_should_have_value  (conftest_glue/conftest.py)')
    assert what in ['context', 'target_fixture'], 'Illegal value for "what"!'
    if what == 'context':
        assert 'bar' in context
        assert context['bar'] == str_value
    # else:
    # assert bar == str_value


@then('the step name can be found')
def _() -> None:
    print('\n==> xxx  (conftest_glue/conftest.py)\n')


@given('a_given_step (glue in conftest.py)')
def a_given_step_() -> None:
    print('\n==> xxx  (conftest_glue/conftest.py)\n')


#########
#########

# @pytest.fixture
# def fcontext() -> None:
#     return {}


# @pytest.fixture
# def fcontext() -> None:
#     class Context:
#         pass

#     return Context()


#########
#########
# @pytest.fixture(scope='session')
# def fcontext() -> None:
#     """Context object to store data to be passed between steps"""
#     return Context()


#########
#########
# @pytest.fixture(autouse=True)
# def _context(request) -> dict:
#     print(f'The value of request is: {request}')
#     ret = {
#         'scenario': None,  # initialize the scenario key to None
#         'steps': [],  # steps list starts out empty
#     }
#     print(f' ==> function _context() in article/conftest.py --> returns dict: {ret})')
#     return ret


#########


# @pytest.fixture
# def fcontext() -> dict:
#     ret = {'user': '?', 'steps': []}
#     print(f' ==> function context() in article/conftest.py --> returns dict: {ret})')
#     return ret


@pytest.fixture
def author_name() -> str:
    """
    Fixture 'author_name' returns a name to be used as author in some tests
    """
    print('\n==> author_name  (conftest_glue/conftest.py)\n')
    ret = 'Sten Aksel'
    print('\n\t(in article/conftest.py)\n\t@pytest.fixture\n\tdef author_name() -> str: {ret}')
    return ret


# @pytest.fixture
# def context_fixture(request, context) -> None:
#     print(f'\n==> context_fixture (article/conftest.py)\n\t==> request: {request}')
#     print(f'\n==> context_fixture (article/conftest.py)\n\t==> context: {context}')
#     # return contextfixture.ContextFixture(request, context)


# @pytest.fixture
# def fcontext() -> None:
#     class Context(object):
#         pass

#     return Context()


