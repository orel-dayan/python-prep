class GateController:
    """Decides what to do when a tag is swiped, based on the DB answer."""
 
    def __init__(self, database):
        self.database = database
 
    def handle_tag(self, tag_id):
        answer = self.database.query(tag_id)
        if answer == "found":
            return "GATE_OPEN"
        return "ALARM"
 