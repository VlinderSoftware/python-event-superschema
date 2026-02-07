Feature: Event Formatting
  As a developer using the event superschema library
  I want to format events with proper metadata
  So that they can be traced and processed correctly in the system

  Scenario: Format a basic event
    Given I have an event formatter
    When I send a basic "OrderPlaced" event
    Then the formatted event should have a type "OrderPlaced"
    And the formatted event should have an id
    And the formatted event should have metadata with correlation id
    And the formatted event should have metadata with transaction id
    And the formatted event should be valid according to the superschema

  Scenario: Format an event with custom data
    Given I have an event formatter
    When I send an "OrderPlaced" event with data:
      | key      | value  |
      | orderId  | 12345  |
      | amount   | 99.99  |
    Then the formatted event should have a type "OrderPlaced"
    And the formatted event should contain data field "orderId" with value "12345"
    And the formatted event should contain data field "amount" with value "99.99"
    And the formatted event should be valid according to the superschema

  Scenario: Format an event with custom correlation id
    Given I have an event formatter
    When I send an "OrderPlaced" event with correlation id "custom-cid-123"
    Then the formatted event should have metadata with correlation id "custom-cid-123"
    And the formatted event should be valid according to the superschema

  Scenario: Format an event with custom transaction id
    Given I have an event formatter
    When I send an "OrderPlaced" event with transaction id "custom-tid-456"
    Then the formatted event should have metadata with transaction id "custom-tid-456"
    And the formatted event should be valid according to the superschema
