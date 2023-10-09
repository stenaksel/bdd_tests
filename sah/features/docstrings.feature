Feature: Doc Strings

  Doc Strings are useful when you have plenty of text to enter in multiple lines.
  For example, to represent the exact content of an email message, you could use a Doc String.
  DocString should be written within pair of triple quotes (or alernatively three backticks)

  @ok
  Scenario: Assign string value without a doc string
    Given I have a step without a doc string:
    When I ask for how many lines the doc string have
    Then I should be told it was no lines (because the doc string was missing)

  @ok
  Scenario: Assign string value from doc string with no lines
    Given I have a step with a doc string:
      """
      """
    But the doc string don't contain any lines
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

  #TODO Handle multiple docstrings in same scenario
  @skip @todo
  Scenario: Assign string values from multiple one-liner doc strings
    Given I have a message:
      """
      This is a test message.
      """
    And I have another message:
      """
      This is another
      test message.
      """
    When I ask for information about message(s) and number of line(s)
    Then I should be informed it was 2 doc strings
    And informed that 1. had 1 line
    And informed that 2. had 2 lines

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
    Given I have a step with a doc string:
      """
        This is a test message.
        This is a second message.
        This is the third test message.
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

  @ok
  Scenario: Using a docstring with xml content (normal format)
    Given I have a step with a doc string:
      """xml
      <xml>
        <tag>Content: This is a test message.</tag>
      </xml>
      """
    When I ask for how many lines the message have
    Then I should be told it was 3 lines

  @ok
  Scenario: Using a docstring with xml content (strange format)
    Given I have a step with a doc string:
      """
      <xml><tag>Content: This is a test message.</tag></xml>
      """
    When I ask for how many lines the message have
    Then I should be told it was 1 lines


  @ok
  Scenario: Using a docstring with xml content (weird format)
    Given I have a step with a doc string:
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
