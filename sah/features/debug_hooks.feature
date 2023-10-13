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

  @wip
  Scenario: before_feature called once
    Given a "pytest_bdd_before_scenario" hook function
    # And
    # Given a "pytest_bdd_before_scenario" Pytest-BDD hook function in conftest.py
    When the scenario is run
    # Then information in context "TEST_CONTEXT" will include "Current glue"
    Then "TEST_CONTEXT" should show that the function "before_scenario" have been run

  @wipz
  Scenario: Inform about the test run
    Given this scenario is tagged with "wip"
    Given a "pytest_bdd_before_scenario" hook function
    # Given a "pytest_bdd_before_scenario" Pytest-BDD hook function in conftest.py
    When the scenario is run
    Then at before each step the "before_step" function is called
    # Then information in context "TEST_CONTEXT" will include "Current glue"
    Then "TEST_CONTEXT" should show that the function "before_scenario" have been run


  # Then information in context will include "Current glue"
  # And information in context "TEST_CONTEXT" will include:
  # "|Func" with value "before_scenario"
  # | key              | value
  # | Current feature  | Debug Hooks
  # | Current scenario | Inform about the test run
  # | Current Step     | N/A or Then/And? "TEST_CONTEXT" should show that the function "before_scenario" have been run
  # | Current glue     | N/A

  @ok
  Scenario: Current information added to TEST_CONTEXT when running
    # Given the variable "DO_INCL_CURR_INFO" is set to "True"
    When the step definition is run
    Then information in TEST_CONTEXT will include "Current glue"

  @wipz
  Scenario: Add information in TEST_CONTEXT when running for pytest_bdd_before_scenario
    # Given a Pytest-BDD test using the "log_glue" module
    # And a "pytest_bdd_before_scenario" Pytest-BDD hook function in conftest.py
    # And a Pytest-BDD hook function <hook> in conftest.py
    When the step definition is run
    Then "TEST_CONTEXT" should show that the hook-function "before_scenario" have been run

  Scenario Outline: Add information in TEST_CONTEXT when running
    Given a "<hook>" Pytest-BDD hook function in conftest.py
    # Given a Pytest-BDD hook function <hook> in conftest.py
    When the step definition is run
    Then "TEST_CONTEXT" should show that the hook-function "<func>" have been run
    Examples:
      | hook                       | func            |
      | pytest_bdd_before_scenario | before_scenario |
  # | pytest_bdd_after_scenario  | after_scenario  |
  # | pytest_bdd_before_step     | before_step     |
  # | pytest_bdd_after_step      | after_step      |


  @todo
  Scenario: Inform about the running Feature
    Given a "pytest_bdd_before_scenario" pytest.hook function in conftest.py
    When you run "pytest -rA -m wip"
    Then information about context stored in "TEST_CONTEXT" will include:
      | key              |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |

  Scenario: Inform about the running Scenario
    Given a "pytest_bdd_before_scenario" pytest.hook function in conftest.py
    When you run "pytest -rA -m wip"
    Then information about context stored in "TEST_CONTEXT" will include:
      | key              |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |


  Scenario: Inform about the Pytest-BDD process (no params)
    Given a glue function without any parameters
    And at the start of the glue code "log_params" function is called
    Then information that no parameters will be shown
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
    And the "log_glue" function will also display informative texts for the run


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

  #####################################################################
  # Hooks
  #####################################################################

  @todo
  Scenario:
    Given I have the hook function "pytest_bdd_before_scenario" declared
    And it calls the function "before_scenario"
    When I run "pytest -rA"
    Then hook "pytest_bdd_before_scenario" function execution should be logged
    And the log should include text "pytest_bdd_before_scenario"
    And the log should include text "context: 1 key"
