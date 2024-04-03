from fastapi import FastAPI
from api.routers.main import api_router
from starlette.middleware.cors import CORSMiddleware

api = {
    "title": "API - HR Application",
    "description": "API for HR to data handling",
    "version": "1.0.0",
}

app = FastAPI(
    title=api["title"], description=api["description"], version=api["version"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(prefix="/api/v1", router=api_router)


@app.get("/")
def root():
    return {"Root": "API HR to data handling."}
