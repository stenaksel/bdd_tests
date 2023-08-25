Feature:Eating cucumbers

  Some text in the feature

  @wip
  Scenario: Arguments for given, when, then
    Given there are 5 cucumbers
    When I eat 3 cucumbers
    And I eat 2 cucumbers
    Then I should have 0 cucumbers

  Scenario Outline: Eating: <case>
    Given there are <start> cucumbers
    When I eat <eat> cucumbers
    Then I should have <left> cucumbers

    Examples:
      | case     | start | eat | left |
      | Eat some | 12    | 5   | 7    |
      | Eat all  | 12    | 12  | 0    |
