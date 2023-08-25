# content of debug_glue.feature
Feature: Debug Hooks

  Background: Using log_glue
    Given a pytest-bdd test using the "log_glue" module
    And the "conftest.py" uses hooks that calls the corresponding log_glue function
  # eg. "pytest_bdd_before_step" calls "log_before_step"

  # Scenario: Using pytest-bdd in vscode
  # Given you're in the feature file in vscode
  # And you would like to go from Step to the Step Definition (the "glue code")
  # And your vscode don't use the "Pytest BDD" extension
  # But your vscode uses the "Cucumber (Gherkin) Full Support" extension
  # And your have added the Cucumber Expression to the glue code
  # When you asks to "Go to Definition" from the step in a feature file
  # Then the correct Step Definition (aka glue function) will be shown

  @wiz
  Scenario: Inform about the running hook
    Given this scenario is tagged with "wip"
    And a "pytest_bdd_before_scenario" pytest.hook function in conftest.py
    When you run "pytest -rA -m wip"
    Then information about context stored in "TEST_CONTEXT" will include
      | key              |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |

  Scenario: Inform about the running Scenario
    Given this scenario is tagged with "wip"
    And a "pytest_bdd_before_scenario" pytest.hook function in conftest.py
    When you run "pytest -rA -m wip"
    Then information about context stored in "TEST_CONTEXT" will include
      | key              |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |


  Scenario: Inform about the pytest-bdd process (no params)
    Given a glue function without any parameters
    And at the start of the glue code "log_glue" function is called
  # And at the end of the glue "log_glue_end" function is called
  # When you run "pytest -rA -m wip"
  # Then pytest will execute the tests tagged "@wip"
  # # (tests = scenarioes)
  # And provide a detailed summary report
  # And the "log_glue" function will also display informative texts for the run

  Scenario: Inform about the pytest-bdd process
    Given a glue function
    And at the start of the glue code "log_glue" function is called
    And at the end of the glue "log_glue_end" function is called
    When you run "pytest -rA -m wip"
    Then pytest will execute the tests tagged "@wip"
    # (tests = scenarioes)
    And provide a detailed summary report
    And the "log_glue" function will also display informative texts for the run

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
      | info             |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |

  @wiz
  Scenario: Add information in context when running
    Given a scenario step using the "log_glue" function
    And the variable "DO_INCL_CURR_INFO" is set to "True"
    When the step definition is run
    Then information about context stored in "TEST_CONTEXT" will include
      | key              |
      | Current glue     |
      | Current Step     |
      | Current scenario |
      | Current feature  |

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
  #####################################################################
  # Hooks
  #####################################################################

  @wiz
  Scenario:
    Given I have the hook function "pytest_bdd_before_scenario" declared
    And it calls the function "before_scenario"
    When I run "pytest -rA"
    Then hook "pytest_bdd_before_scenario" function execution should be logged
    And the log should include text "pytest_bdd_before_scenario"
    And the log should include text "context: 1 key"
