# content of debug_glue.feature
Feature: Debug Glue

  Background: Using log_glue
    Given a pytest-bdd test using the "log_glue" module

  # Scenario: Using pytest-bdd in vscode
  # Given you're in the feature file in vscode
  # And you would like to go from Step to the Step Definition (the "glue code")
  # And your vscode don't use the "Pytest BDD" extension
  # But your vscode uses the "Cucumber (Gherkin) Full Support" extension
  # And your have added the Cucumber Expression to the glue code
  # When you


  @wiz
  Scenario: Add information with current glue context when running
    Given a step definition using the "context" fixture
    And the step definition is calling the "log_glue" function
    # And the variable "DO_INCL_CURR_INFO" is set to "True"
    When the step definition is run
    Then information about context will include "Current glue" until log_glue_end is called

  Scenario Outline: Add information in current context when running
    Given a step definition using the "context" fixture
    And the step definition is calling the "log_glue" function
    # And the variable "DO_INCL_CURR_INFO" is set to "True"
    When the step definition is run
    Then information about context will include "<info>" until log_glue_end is called
    Examples:
      | info         |
      | Current glue |
  # | Current Step     |
  # | Current scenario |
  # | Current feature  |

  Scenario: glue function without any parameters - no context param
    Given I have a glue function "glue_func_no_params" without parameters
    When "glue_func_no_params" is called by pytest-bdd
    Then information about the called function should be logged
  #   And the log should include text "glue_func_no_params()"
  #   And the log should include text "context: NOT provided!"

  Scenario: glue function with context
    Given I have step definition given a "context" parameter
    When I check the provided context parameter
    Then it should be a dictionary

  Scenario: glue function with only context param
    Given I have glue function "glue_func_with_context" with "context" parameter
    When it is calledby pytest-bdd
    Then information about the called function should be logged
    And the log should include text "glue_func_with_context(context)"
    And the log should include text "context: 1 key"


  Scenario: Using context information
    # Given a_given_step (glue in conftest.py)
    # Given a_given_step
    # Given a step without context
    Given I have glue function without any parameters (no context)
    Given I have step definition given a context parameter
  # Given I have a step2
  # Given I have a step3
  # Given a given step
  # When a when step
  # Then a then step
