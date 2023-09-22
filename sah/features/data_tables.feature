# content of data_tables.feature
Feature: Data tables

  Steps with a data table, are passed an object that can be used to access the data

  @todo
  Scenario: Data table with column headers

    Given a step with a data table with column headers:
      | rows   |
      | 1. row |
      | 2. row |
      | 3. row |
      | 4. row |
    When
    Then the table should have 4 rows:
      """
        1. row
        2. row
        3. row
        4. row
      """


  @todo
  Scenario: Data table without column headers
    Given a step with a data table without column headers:
      | 1. row |
      | 2. row |
      | 3. row |
      | 4. row |
    When steps have a data table, they are passed an object with methods that can be used to access the data
    Then the table should have 4 rows:
      """
        1. row
        2. row
        3. row
        4. row
      """
