from gate_controller import GateController

# A stub just provides canned answers. No verification of calls.


class StubDatabase:
    def query(self, tag_id):
        # Always returns the same answer, ignores the actual id
        return "found"


def test_gate_opens_with_stub():
    stub_db = StubDatabase()
    controller = GateController(database=stub_db)

    result = controller.handle_tag("12345")

    assert result == "GATE_OPEN"
    # Note: we do NOT check whether query() was called — that's the
    # difference from a mock. A stub only feeds data into the test.