from fastapi import FastAPI

app = FastAPI()

@app.post("/users")
def create_user(user: dict):
    return {
        "message": "Utilisateur cree",
        "data": user
    }
