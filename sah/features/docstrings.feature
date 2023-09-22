
Feature: DocStrings

  @ok
  Scenario: Assign string value without DocString
    Given I have step with no Docstring
    Given I have step without a Docstring:
    # Given I have a step without a message
    When I ask for how many lines the message have
    Then I should be told it was 0 lines

  @todo
  Scenario: Assign string value from DocString with no lines
    Given I have step with a Docstring:
      """
      """
    When I ask for how many lines the message have
    Then I should be told it was 0 lines

  @ok
  Scenario: Assign string value from DocString with one line
    Given I have a message:
      """
      This is a test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 1 line

  @todo
  Scenario: Assign string value from DocString with two lines
    Given I have a message:
      """
      This is a
      test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 2 lines

  @todo
  Scenario: Assign string value from DocString with multiple lines
    Given I have step with a Docstring:
      """
        This is a test message.
        This is a second message.
        This is the third test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

  #    When eg. ask for how many lines the DocString is
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

  @todo
  Scenario: Formatting the docstring based on content type: xml
    Given I have step with a Docstring:
      """xml
      <xml>
        <tag>Content: This is a test message.</tag>
      </xml>
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

  @todo
  Scenario: Formatting the docstring based on content type: xml 1 line
    Given I have step with a Docstring:
      """ <xml><tag>Content: This is a test message.</tag></xml> """
    When I ask for how many lines the message have
    Then I should be told it was 1 lines

  @todo
  Scenario: Formatting the docstring based on content type: xml 1 line
    Given I have step with a Docstring:
      """<xml><tag>Content: This is a test message.</tag></xml>"""
    When I ask for how many lines the message have
    Then I should be told it was 2 lines  #Q: Why 2 lines?

# Feature: DocString variations

#   Scenario: minimalistic
#     Given a simple DocString
#       """
#       first line (no indent)
#         second line (indented with two spaces)

#       third line was empty
#       """
#     Given a DocString with content type
#       """xml
#       <foo>
#         <bar />
#       </foo>
#       """
#     And a DocString with wrong indentation
#       """
#     wrongly indented line
#       """
#     And a DocString with alternative separator
#       ```
#       first line
#       second line
#       ```
#     And a DocString with normal separator inside
#       ```
#       first line
#       """
#       third line
#       ```
#     And a DocString with alternative separator inside
#       """
#       first line
#       ```
#       third line
#       """
#     And a DocString with escaped separator inside
#       """
#       first line
#       \"\"\"
#       third line
#       """
