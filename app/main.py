from fastapi import FastAPI
from app.routers import user, upload
app = FastAPI()
# uvicorn app.main:app --reload

app.include_router(user.router)
app.include_router(upload.router)
@app.get("/")
def root():
    return {
        "message": "FastAPI "
    }