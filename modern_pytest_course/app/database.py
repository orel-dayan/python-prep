import time


class FakeDatabase:
    def __init__(self):
        print("Starting fake database server...")
        time.sleep(2)  # simulate expensive setup

        self.users = {
            1: "Alice",
            2: "Bob",
            3: "Charlie",
        }

    def user_count(self):
        return len(self.users)
    
    def get_user(self, user_id):
        return self.users.get(user_id)
 
