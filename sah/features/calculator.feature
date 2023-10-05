Feature: Calculator

  @ok
  Scenario: Add numbers
    # Given I have a simple calculator
    Given I have a calculator
    When I add 2 and 3
    Then the result should be 5
  # Then the expected result should be 5

  @ok
  Scenario Outline: Outline Add numbers <num1> & <num2>
    Given I have a calculator
    When I add <num1> and <num2>
    Then the result should be <total>

    Examples:
      | num1 | num2 | total |
      | 2    | 2    | 4     |
      | -2   | 3    | 1     |
      | 10   | 15   | 25    |
      | 99   | -99  | 0     |
      | -1   | -10  | -11   |
