# content of debug_glue.feature
Feature: Debug Glue

  Background: Using log_glue
    Given a Pytest-BDD test using the "log_glue" module

  # Scenario: Using Pytest-BDD in vscode
  # Given you're in the feature file in vscode
  # And you would like to go from Step to the Step Definition (the "glue code")
  # And your vscode don't use the "Pytest BDD" extension
  # But your vscode uses the "Cucumber (Gherkin) Full Support" extension
  # And your have added the Cucumber Expression to the glue code
  # When you


  @wipz
  Scenario: Current glue information not added to context when running
    # Given the variable "DO_INCL_CURR_INFO" is set to "True"
    When the step definition is run -> glue
    Then information in context, will not include "Current glue"


  Scenario: glue function without any parameters - no context param
    Given I have a glue function "glue_func_no_params" without parameters
    When "glue_func_no_params" is called by Pytest-BDD
    Then information about the called function should be logged
  #   And the log should include text "glue_func_no_params()"
  #   And the log should include text "context: NOT provided!"


  Scenario: Using context information
    # Given a_given_step (glue in conftest.py)
    # Given a_given_step
    # Given a step without context
    Given I have a glue function "glue_func_no_params" without parameters
    Given I have glue function without any parameters
    Given I have step definition given a context parameter
# Given I have a step2
# Given I have a step3
# Given a given step
# When a when step
# Then a then step
