from fastapi import FastAPI
from app.routers import user, auth, post, follow, like, comment
app = FastAPI()
# uvicorn app.main:app --reload

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(follow.router)
app.include_router(like.router)
app.include_router(comment.router)

@app.get("/")
def root():
    return {
        "message": "FastAPI "
    }