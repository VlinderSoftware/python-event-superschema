Feature: Event Dispatching
  As a developer using the event superschema library
  I want to dispatch events to appropriate handlers
  So that events can be processed by the correct components

  Scenario: Dispatch an event to a specific handler
    Given I have an event dispatcher with a handler for "OrderPlaced"
    When I dispatch a valid "OrderPlaced" event
    Then the "OrderPlaced" handler should be called

  Scenario: Dispatch an event with invalid schema
    Given I have an event dispatcher with an error handler
    When I dispatch an invalid event missing required fields
    Then the error handler should be called with a schema mismatch error

  Scenario: Dispatch an event to the default handler
    Given I have an event dispatcher with a default handler
    And I have no specific handler for "UnknownEvent"
    When I dispatch a valid "UnknownEvent" event
    Then the default handler should be called

  Scenario: Dispatch multiple events to different handlers
    Given I have an event dispatcher with handlers for "OrderPlaced" and "OrderCancelled"
    When I dispatch a valid "OrderPlaced" event
    And I dispatch a valid "OrderCancelled" event
    Then the "OrderPlaced" handler should be called
    And the "OrderCancelled" handler should be called
