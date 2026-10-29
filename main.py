from fastapi import FastAPI
from routers import issues, users, buys_router

app = FastAPI(
    title="Maverick Comic Collection V0.1",
    description="An API designed to manage your inventory at a comic store",
    version="0.1.0"
)

app.include_router(users.router)
app.include_router(issues.router)
app.include_router(buys_router.router)

@app.get("/")
def root():
    return {"message": "endpoint test"}