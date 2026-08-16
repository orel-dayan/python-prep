from gate_controller import GateController

# A fake has real working logic, just simplified.
# Here: an in-memory DB instead of a real SQL database.

class FakeDatabase:
    def __init__(self):
        # Real storage — but in a dict, not on disk
        self._employees = set()

    def add_employee(self, tag_id):
        self._employees.add(tag_id)

    def query(self, tag_id):
        # Actually checks — real logic, unlike a stub/mock
        return "found" if tag_id in self._employees else "not_found"


def test_gate_with_fake_db():
    fake_db = FakeDatabase()
    fake_db.add_employee("12345")  # set up real data

    controller = GateController(database=fake_db)

    # This really searches the in-memory store
    assert controller.handle_tag("12345") == "GATE_OPEN"
    assert controller.handle_tag("99999") == "ALARM"