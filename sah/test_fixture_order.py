import pytest


@pytest.mark.order(-2)
@pytest.fixture
def first() -> None:
    print('I go first.')


@pytest.mark.order(-1)
@pytest.fixture
def second() -> None:
    print('I go second.')


@pytest.fixture
def third() -> None:
    print('I go third.')


@pytest.mark.order(1)
@pytest.fixture
def fourth() -> None:
    print('I go fourth.')


@pytest.mark.order(2)
@pytest.fixture
def fifth() -> None:
    print('I go fifth.')


# SAH: The order of fixtures is given by param order, NOT pytest.mark.order


@pytest.mark.skip
def test_order_normal(first, second, third, fourth, fifth) -> None:
    print('Running your test param order.')


@pytest.mark.skip
def test_order_backward(fifth, fourth, third, second, first) -> None:
    print('Running your test param order (backwards).')
