import pytest


@pytest.mark.ok
def test_no_bdd_divisible_by_3(input_value=21) -> None:
    assert input_value % 3 == 0


@pytest.mark.ok
def test_no_bdd_divisible_by_6(input_value=24) -> None:
    assert input_value % 6 == 0
