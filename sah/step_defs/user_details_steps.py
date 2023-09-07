import json

import requests

from pytest_bdd import given, when, then   # isort:skip


@given('I have the following user details:')
def step_given_user_details(context, step):
    assert step is not None
    assert step.text is not None
    body = step.text
    assert isinstance(body, str)
    assert len(body) != 0
    user_details = json.loads(step.text)
    context['user_details'] = user_details


@when('I send a POST request to the /users endpoint')
def step_when_send_post_request(context):
    url = 'http://localhost:8000/users'
    headers = {'Content-Type': 'application/json'}
    data = context['user_details']
    response = requests.post(url, headers=headers, json=data, timeout=3.0)
    context['response'] = response


@then('the response status code should be 201')
def step_then_response_status_code(context):
    assert context['response'].status_code == 201
