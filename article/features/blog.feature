# content of blog.feature
Feature: Blog

  example where all glue is in the test file (test_blog_incl_steps.py)

  @ok
  Scenario: Deleting the article
    Given there is an article
    When I request the deletion of the article
    Then the request should be successful
