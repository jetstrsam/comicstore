from fastapi import FastAPI
from routers import issues

app = FastAPI()

app.include_router(issues.router)

@app.get("/")
def root():
    return {"message": "comicstore test"}