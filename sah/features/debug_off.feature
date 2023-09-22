# content of debug_glue.feature
Feature: Debug Off

  # Background: Using log_glue
  #   Given a Pytest-BDD test using the "log_glue" module
  # #   And the "TEST_CONTEXT" item "logger" is not present
  #   And the "conftest.py" uses Pytest-BDD hooks that calls the corresponding "log_glue" functions
  #   And the run is configured with at least log_level = "DEBUG"
  # # eg. "pytest_bdd_before_step" calls "before_step"

  # Scenario: Using Pytest-BDD in vscode
  # Given you're in the feature file in vscode
  # And you would like to go from Step to the Step Definition (the "glue code")
  # And your vscode don't use the "Pytest BDD" extension
  # But your vscode uses the "Cucumber (Gherkin) Full Support" extension
  # And your have added the Cucumber Expression to the glue code
  # When you asks to "Go to Definition" from the step in a feature file
  # Then the correct Step Definition (aka glue function) will be shown


  # KEY_CURR_FEATURE = 'Current feature'
  # KEY_CURR_GLUE = 'Current glue'
  # KEY_CURR_SCENARIO = 'Current scenario'
  # KEY_CURR_STEP = 'Current step'
  # KEY_CONTEXT = 'context'
  # KEY_DBG_FUNC_NAME = 'dbg:func_name'
  # KEY_LOG_GLUE = 'log_glue'    # TODO: Values: None (=False), False,  True, Hooks (=True), Feature, Scenario, Step
  # KEY_LOGGER = 'logger'    # TODO: Values: None (=False), False,  True
  # KEY_STEP_COUNTER = 'step_counter'
  # TEST_CONTEXT = {'name': 'TEST_CONTEXT'}
  # GLUE_LOGGER = logging.getLogger(KEY_LOG_GLUE)

  @todo #TODO work-in-progress
  Scenario: Just testing
    Given a Pytest-BDD test using the "log_glue" module
    Given the "TEST_CONTEXT" item "Current feature" is present
  # Given the "TEST_CONTEXT" item "Current scenario" is present
  # Given the "TEST_CONTEXT" item "logger" is present
  # Given the "TEST_CONTEXT" item "logger" is present
  # But the item value is "False"
  # Given the "TEST_CONTEXT" item "logger" is not present or value "False"

  Scenario: Current feature should be logged
    Given a Pytest-BDD test using the "log_glue" module
    When the scenario is run

    Given the "TEST_CONTEXT" item "Current feature" is present

  @todo #TODO work-in-progress
  Scenario: No logging from log_glue functions
    # Given the "TEST_CONTEXT" item "logger" is present
    # But the item value is "False"
    # Given the "TEST_CONTEXT" item "logger" is not present or value "False"
    # Given that item "logger" is not present
    When Pytest-BDD is run
    Then there should not be logging from "log_glue" functions

  @todo
  Scenario: Set logging to on
    Given I set "TEST_CONTEXT" item "logger" with value "True"
    When Pytest-BDD is run
    Then there should not be any logging from "log_glue" functions
