Feature: Target fixture

  @wipz
  Scenario: Test given fixture injection
    Given I have injecting given
    Then foo should be "injected foo"
