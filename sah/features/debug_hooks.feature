# content of debug_glue.feature
Feature: Debug Hooks

  Background: Using log_glue
    Given a Pytest-BDD test using the "log_glue" module
  #   And the "x" uses Pytest-BDD hooks that calls the corresponding "log_glue" functions
  # # eg. "pytest_bdd_before_step" calls "before_step"

  # Scenario: Using Pytest-BDD in vscode
  # Given you're in the feature file in vscode
  # And you would like to go from Step to the Step Definition (the "glue code")
  # And your vscode don't use the "Pytest BDD" extension
  # But your vscode uses the "Cucumber (Gherkin) Full Support" extension
  # And your have added the Cucumber Expression to the glue code
  # When you asks to "Go to Definition" from the step in a feature file
  # Then the correct Step Definition (aka glue function) will be shown

  @wipz
  @ok
  Scenario: try out
    Given this scenario is tagged with "wip"
    When the scenario is run

  @ok
  Scenario: before_feature called once
    Given the Pytest-BDD hook-function "pytest_bdd_before_scenario" in conftest.py
    When the scenario is run
    #TODO When the step definition is run
    #TODO When the step definition after function is run
    # Then information in context "TEST_CONTEXT" will include "Current glue"
    # Then "TEST_CONTEXT" should show that the hook-function "pytest_bdd_before_scenario" have been run
    Then "TEST_CONTEXT" should show that the function "before_scenario" have been run


  @ok
  Scenario Outline: Add information about running hooks
    Given the Pytest-BDD hook-function "<hook>" in conftest.py
    When the hook-function have run
    # Then "TEST_CONTEXT" should show that the hook-function "<hook>" have been run
    Then "TEST_CONTEXT" should show that the function "<func>" have been run

    Examples:
      # Hint: before_feature will be called on first scenario
      | hook                       | func            |
      # | pytest_configure           | configure       |
      | pytest_bdd_before_scenario | before_feature  |
      # | pytest_bdd_before_scenario | before_scenario |
      # | pytest_bdd_after_scenario  | after_scenario  |
      # | pytest_bdd_before_step     | before_step     |
      # | pytest_bdd_after_step      | after_step      |


  @wipz
  Scenario: Inform about the test run
    Given this scenario is tagged with "wip"
    And the Pytest-BDD hook-function "pytest_bdd_before_step" in conftest.py
    # Given a "pytest_bdd_before_scenario" Pytest-BDD hook-function in conftest.py
    # When the scenario is run
    When the hook-function have run
    Then before each Gherkin step is run the "before_step" function is called
    # Then information in context "TEST_CONTEXT" will include "Current glue"
    Then "TEST_CONTEXT" should show that the function "before_step" have been run


  # Then information in context will include "Current glue"
  # And information in context "TEST_CONTEXT" will include:
  # "|Func" with value "before_scenario"
  # | key              | value
  # | Current feature  | Debug Hooks
  # | Current scenario | Inform about the test run
  # | Current Step     | N/A or Then/And? "TEST_CONTEXT" should show that the function "before_scenario" have been run
  # | Current glue     | N/A

  @wipz
  Scenario: Current information added to TEST_CONTEXT when running
    # Given the variable "DO_INCL_CURR_INFO" is set to "True"
    When the step definition is run
    Then information in TEST_CONTEXT will include "Current glue"

  Scenario: Inform about the Pytest-BDD process (glue without params)
    Given a glue function without any parameters
    When the step definition is run
    Then information about the glue call will be shown
    And the information logged shows noe parameters were passed to the glue function
  # When you run "pytest -rA -m wip"
  # Then pytest will execute the tests tagged "@wip"
  # # (tests = scenarioes)
  # And provide a detailed summary report
  # And the "log_glue" function will also display informative texts for the run

  Scenario: Inform about the Pytest-BDD process
    Given a step definition (aka a glue function)
    When you run "pytest -rA -m wip"
    Then pytest will execute the tests tagged "@wip"
    # (tests = scenarioes)
    And at before each step the "before_step" function is called
    And at after each step the "after_step" function is called
    And provide a detailed summary report
    And the "log_glue" functions will also display informative texts for the run


  @todo
  Scenario: Add information in context when running
    Given a scenario step using the "log_glue" function
    And the variable "DO_INCL_CURR_INFO" is set to "True"
    When _you run "pytest -rA -m wip"
    Then information about context stored in "TEST_CONTEXT" will include
      | key              |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |

  Scenario: glue function without any parameters - no context param
    Given I have a glue function "glue_func_no_params" without parameters
    When "glue_func_no_params" is called by Pytest-BDD
    Then information about the called function should be logged
  #   And the log should include text "glue_func_no_params()"
  #   And the log should include text "context: NOT provided!"

  Scenario: glue function with context
    Given I have step definition given a "context" parameter
    When I check the provided context parameter
    Then it should be a dictionary

  Scenario: glue function with only context param
    Given I have glue function "glue_func_with_context" with "context" parameter
    When it is calledby Pytest-BDD
    Then information about the called function should be logged
    And the log should include text "glue_func_with_context(context)"
    And the log should include text "context: 1 key"


  #####################################################################
  # Hooks
  #####################################################################

  @todo
  Scenario:
    Given I have the hook-function "pytest_bdd_before_scenario" declared
    And it calls the function "before_scenario"
    When I run "pytest -rA"
    Then hook "pytest_bdd_before_scenario" function execution should be logged
    And the log should include text "pytest_bdd_before_scenario"
    And the log should include text "context: 1 key"
