from fastapi import FastAPI
from app.routers import user, auth
app = FastAPI()
# uvicorn app.main:app --reload

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "message": "FastAPI "
    }