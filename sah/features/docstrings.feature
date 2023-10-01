
Feature: doc strings

  @wip
  Scenario: Assign string value without a doc string
    Given I have step without a doc string:
      """
      1
      """
    When I ask for how many lines the doc string have
    Then I should be told it was no lines (because the doc string was missing)

  @ok
  Scenario: Assign string value from doc string with no lines
    Given I have step with a doc string:
      """
      """
    When I ask for how many lines the message have
    Then I should be told it was 0 lines

  @ok
  Scenario: Assign string value from doc string with one line
    Given I have a message:
      """
      This is a test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 1 line

  @ok
  Scenario: Assign string value from doc string with two lines
    Given I have a message:
      """
      This is a
      test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 2 lines

  @ok
  Scenario: Assign string value from doc string with multiple lines
    Given I have step with a doc string:
      """
        This is a test message.
        This is a second message.
        This is the third test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

#TODO Handle multiple docstrings in same scenario
  Scenario: Scenario with multiple doc strings
    Given I have step with a doc string:
      """
        This is a test message.
        This is a second message.
        This is the third test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

  #    When eg. ask for how many lines the doc string is
  #    Then I should be told it was 3 lines long

  #    Then the message should be delivered successfull

  # Scenario: Send an email
  #   Given I have an email address "john@example.com"
  #     And I have a message:
  #         """
  #         This is a test message.
  #         """
  #    When I send the message to the email address
  #    Then the message should be delivered successfull


  # Scenario: Create a new user
  #   Given I have the following user details:
  #    When I send a POST request to the /users endpoint
  #    Then the response status code should be 201

  @ok
  Scenario: Formatting the docstring based on content type: xml
    Given I have step with a doc string:
      """xml
      <xml>
        <tag>Content: This is a test message.</tag>
      </xml>
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

  @wip
  Scenario: Formatting the docstring based on content type: xml 1 line
    Given I have step with a doc string:
      """ <xml><tag>Content: This is a test message.</tag></xml> """
       When I ask for how many lines the message have
       Then I should be told it was 1 lines

  @todo
  Scenario: Formatting the docstring based on content type: xml 1 line
      Given I have step with a doc string:
      """<xml><tag>Content: This is a test message.</tag></xml>"""
    When I ask for how many lines the message have
    Then I should be told it was 2 lines  #Q: Why 2 lines?


# Feature: doc string variations

#   Scenario: minimalistic
#     Given a simple doc string
#       """
#       first line (no indent)
#         second line (indented with two spaces)

#       third line was empty
#       """
#     Given a doc string with content type
#       """xml
#       <foo>
#         <bar />
#       </foo>
#       """
#     And a doc string with wrong indentation
#       """
#     wrongly indented line
#       """
#     And a doc string with alternative separator
#       ```
#       first line
#       second line
#       ```
#     And a doc string with normal separator inside
#       ```
#       first line
#       """
#       third line
#       ```
#     And a doc string with alternative separator inside
#       """
#       first line
#       ```
#       third line
#       """
#     And a doc string with escaped separator inside
#       """
#       first line
#       \"\"\"
#       third line
#       """
