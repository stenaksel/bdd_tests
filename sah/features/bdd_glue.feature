Feature: BDD Glue

    When_working_with_BDD we write prose in a feature file.

    The prose consists of scenarioes and it's steps (Given, When, Then, etc.).
    To make the scenarioes runnable as tests, we have to write the code to do
    exactly what each prose step explains.
    This code is "step definitions" popularly known as called "glue-code".
    To actually run the feature file(s) as tests, we also need a BDD tool.
    The tool choosen here is called Pytest-BDD.
    (Behave is another BDD tool usable with Python).

    In_a_scenario we can have many steps with the same type (Eg. many "Given" steps).
    It is then normal to use "And" prefix to ease the reading
    (Each "And" step will be the same kind of step as the one before it).

    Another normal thing to do is to have a shared "context" (usually a dictionary),
    where the glue can store information.
    For instance, collecting needed info from "Given" glue before reaching the "When" glue.
    Or storing the result in a "When" glue and later checking it in the "Then" glue.
    The "context" can be passed as a parameter to the glue code functions.

  # Background: Using log_glue
  #   Given a Pytest-BDD test using the "log_glue" module
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
