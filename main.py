from fastapi import FastAPI
from routers import issues, users

app = FastAPI()

app.include_router(users.router)
app.include_router(issues.router)

@app.get("/")
def root():
    return {"message": "comicstore test"}