from fastapi import FastAPI
from app.routers import user
app = FastAPI()
# uvicorn app.main:app --reload

app.include_router(user.router)

@app.get("/")
def root():
    return {
        "message": "FastAPI "
    }