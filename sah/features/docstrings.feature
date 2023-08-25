
Feature: DocStrings

  Scenario: Assign string value from DocString with no lines
    # But no message in the step
    Given I have a step without a message
    When I ask for how many lines the message have
    Then I should be told it was 0 lines

  Scenario: Assign string value from DocString with one line
    Given I have a message:
      """
      This is a test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 1 line

  Scenario: Assign string value from DocString with two lines
    Given I have a message:
      """
      This is a
      test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 2 lines

@wiz
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
