from unittest.mock import Mock

from gate_controller import GateController

# Testing the gate controller in isolation.
# We don't want a real database, so we mock it.

def test_authorized_tag_opens_gate():
    # Create a mock DB that returns canned responses
    mock_db = Mock()
    mock_db.query.return_value = "found"  # always returns "found"

    controller = GateController(database=mock_db)
    result = controller.handle_tag("12345")

    # The mock did NOT really search a table — it just returned "found"
    assert result == "GATE_OPEN"

    # Mock's extra power: verify the DB was called correctly
    mock_db.query.assert_called_once_with("12345")


def test_unauthorized_tag_triggers_alarm():
    mock_db = Mock()
    mock_db.query.return_value = "not_found"

    controller = GateController(database=mock_db)
    result = controller.handle_tag("99999")

    assert result == "ALARM"
    mock_db.query.assert_called_once_with("99999")