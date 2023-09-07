# content of debug_glue.feature
Feature: Debug Off

  Background: Using log_glue but don't want logging
    Given a Pytest-BDD test using the "log_glue" module
    And the run is configured with at least log_level = "INFO"
    And the "conftest.py" uses Pytest-BDD hooks that calls the corresponding "log_glue" functions
    But the "TEST_CONTEXT" item "dbg_logging" is not present or is "False"
  # eg. "pytest_bdd_before_step" calls "before_step"

  # Scenario: Using Pytest-BDD in vscode
  # Given you're in the feature file in vscode
  # And you would like to go from Step to the Step Definition (the "glue code")
  # And your vscode don't use the "Pytest BDD" extension
  # But your vscode uses the "Cucumber (Gherkin) Full Support" extension
  # And your have added the Cucumber Expression to the glue code
  # When you asks to "Go to Definition" from the step in a feature file
  # Then the correct Step Definition (aka glue function) will be shown

  @wip
  Scenario: No logging from log_glue functions
  When Pytest-BDD is run
  Then there should not be any logging from "log_glue" functions

  Scenario: Set logging to on
  Given I set "TEST_CONTEXT" item "logging" with value "True"
  When Pytest-BDD is run
  Then there should not be any logging from "log_glue" functions
