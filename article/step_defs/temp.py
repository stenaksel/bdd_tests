# content of temp.py
# from pytest import fixture
from pytest_bdd import given   # isort:skip


@given('I have no step')
def i_have_a_step(context) -> None:
    print(f'\n==> Given I have a step (article/steps.py)\n\tContext: {context}')
    context['steps'].append('Given I have a step')
    # print(f'Step: {context.scenario.feature.name}
    # - {context.scenario.name} - {context.step.name}')
