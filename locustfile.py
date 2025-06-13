from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # waktu tunggu antar request (detik)

    @task
    def index(self):
        self.client.get("/")

    @task
    def mahasiswa(self):
        self.client.get("/admin/mahasiswa")

    @task
    def login(self):
        self.client.post("/login", data={"email": "test@example.com", "password": "password"})