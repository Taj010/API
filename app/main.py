from fastapi import FastAPI
from . import model
from .database import engine
from .routers import post, user, auth
from .config import settings 


model.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#path operation function -- route 
@app.get("/")
def root():
    return {"message": "Hello World"}