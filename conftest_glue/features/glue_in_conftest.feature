# content of glue_in_conftest.feature
Feature: glue_in_conftest

  Scenario: Steps declared in the conftest file
    Given I have a key "bar" in the context
    When I do nothing
    Then context bar should have value "bar-context"

  Scenario: Steps declared in the conftest file with a fixture
    Given I have a target_fixture bar
    When I do nothing
    Then target_fixture bar should have value "bar-target_fixture"
