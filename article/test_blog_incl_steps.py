# content of test_blog.py
"""
All stepdefs are in this file (not in seperate *steps.py file)
"""
from pytest_bdd import given, when, then, scenarios  # isort:skip

from src.domain.article import Article
from src.domain.result import Result

# from article import Article
# from article import *

scenarios('features/blog.feature')


# @given('there is an article')
@given('there is an article', target_fixture='article')
def given_there_is_an_article():
    print("==> given_there_is_an_article() (<- target_fixture='article')")
    ret_article = Article('art.title', 'art.author')
    assert ret_article.name == 'art.title'
    assert ret_article.title == 'art.title'
    assert ret_article.author is not None
    assert ret_article.author == 'art.author'
    print(f'\t<== returning target_fixture: "article": \n\t  {ret_article}')
    return ret_article


@when('I request the deletion of the article', target_fixture='request_result')
def when_i_request_the_deletion_of_the_article(article: Article) -> Result:
    print("==> when_i_request_the_deletion_of_the_article  (<- target_fixture='request_result')")
    print(f'\tReceived fixture param: {article}')
    assert article is not None
    # article.deleted()
    # return Result()
    ret = Result(200)
    print(f'\t<== returning target_fixture: "request_result": \n\t{ret}')
    return ret


@then('the request should be successful')
def request_should_be_successful(request_result: Result):
    print('==> request_should_be_successful')
    print(f'\tReceived fixture param: {request_result}')
    assert request_result.status_code == 200
