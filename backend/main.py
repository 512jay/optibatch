# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import runs_db_connected as runs
from backend.routers import stats_db_connected as stats

app = FastAPI(title="OptiBatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(runs.router, prefix="/runs", tags=["Runs"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])
