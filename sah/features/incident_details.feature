Feature: View incident details
  As a Fraud Engineer, I would like to view all information needed to analyze the incident
  from incident detail page.

  Background: All tests run with an authorized user with Unrestricted access
    Given I am authenticated for a session
    And the user is authorized to view and update incidents
    When the user selects an incident to view in more detail.

  Scenario: Show Incident Details
    Then I will see the incident containing:
      | Section      |
      | Reasoning    |
      | Routing      |
      | Impact       |
      | Metrics      |
      | Data Records |

  Scenario: Show Incident Reasoning
    Then the reasoning should contain an explanation why this is considered a fraud incident
    And the type of the fraud
    And the severity
    And the current status

  Scenario: Show Incident Impact
    Then the incident impact should contain the primary metric used to detect the incident.
    And the number of affected subscribers

  Scenario: Show Incident Routing
    Then the incident routing should contain a network routing path of the traffic

  Scenario: Show Incident Metrics
    Then the incident metrics should contain metrics of the top level grouping metrics development over time
    And the important timestamps of the incident: start-time, action taken time and resolved time
    And the metrics data is grouped by unit: number, percentage, time

  Scenario: Show Data Records
    Then the incident data records should contain a top level grouping of the important metrics of the incident
    And one or more level groupings of the important metrics
      """
              EXAMPLE
      -----------------------------
      Top Level:
                  | Origination | Total calls | ... | Bad Number Rate |
                  | Barbados    | 1000        | ... | 70%             |

             Second Level:
                  | Received From | Total calls | ... | Bad Number Rate |
                  | ScamORama     | 1000        | ... | 70%             |

      Third Level:
                  | Number Series | Total calls | ... | Bad Number Rate |
                  | 999999..      | 1000        | ... | 70%             |
      """

  Scenario: Change Status
    When I change the status of the incident
    Then the incident is visually indicated with the new status

  Scenario: Share Incident
    When I share the incident
    Then a link to the incident is shown

  Scenario: Assign Incident
    When I assign the incident
    Then the incident is visually indicated with the assignee
