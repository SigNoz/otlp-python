from locust import HttpUser, task, between
import random

class UserTasks(HttpUser):
    wait_time = between(30, 60)
    users = [
        "alice",
        "bob",
        "charlie",
        "david",
        "eve",
        "frank",
        "grace",
        "heidi",
        "ivan",
        "judy",
        "kevin",
        "larry",
        "michael",
        "naomi",
        "oliver",
        "patricia",
        "quinn",
        "ray",
        "sarah",
        "trent",
        "ursula",
        "victor",
        "wendy",
        "xavier",
        "yvonne",
        "zelda"
    ]

    @task(1)
    def list(self):
        random_user = random.choice(self.users)
        self.client.get("/?user="+random_user)