Feature: Multiple target fixtures for step function

  Scenario: A step can be decorated multiple times with different target fixtures
    Given there is a foo with value "test foo"
    And there is a bar with value "test bar"
    Then foo should be "test foo"
    And bar should be "test bar"
