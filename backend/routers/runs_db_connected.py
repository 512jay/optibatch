from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import select
from backend.db import get_session
from database.models import Run, Job
from datetime import date, datetime


router = APIRouter()


class RunModel(BaseModel):
    run_id: int = Field(alias="id")  # ✅ Alias from SQLAlchemy 'id' field
    job_id: str
    symbol: str
    profit: Optional[float]
    drawdown: Optional[float]
    custom_score: Optional[float]
    sharpe_ratio: Optional[float]
    trades: Optional[int]
    expected_payoff: Optional[float]
    recovery_factor: Optional[float]
    profit_factor: Optional[float]
    run_month: str
    start_date: date
    end_date: date
    pass_number: int
    result: Optional[float]
    is_full_month: bool
    params_json: Optional[dict]
    result_hash: Optional[str]
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    notes: Optional[str]
    run_label: Optional[str]
    status: str
    is_archived: bool

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,  # ✅ Enables alias resolution
    }


@router.get("/", response_model=list[RunModel])
def list_runs() -> list[RunModel]:
    with get_session() as session:
        stmt = select(Run).join(Job)
        runs = session.scalars(stmt).all()
        return [RunModel.model_validate(run) for run in runs]


@router.get("/{run_id}", response_model=RunModel)
def get_run(run_id: int) -> RunModel:
    with get_session() as session:
        run = session.get(Run, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return RunModel.model_validate(run)
