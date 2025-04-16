# /backend/runs_db_connected.py

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import select
from backend.db import get_session
from database.models import Run, Job

router = APIRouter()


class RunModel(BaseModel):
    run_id: int
    job_id: int
    symbol: str
    profit: float
    run_month: str
    custom_score: Optional[float]
    trades: Optional[int]
    drawdown: Optional[float]

    model_config = {"from_attributes": True}


@router.get("/", response_model=list[RunModel])
def list_runs(symbol: Optional[str] = None, min_profit: Optional[float] = None) -> list[RunModel]:
    with get_session() as session:
        stmt = select(Run).join(Job)

        if symbol:
            stmt = stmt.where(Run.symbol == symbol)
        if min_profit is not None:
            stmt = stmt.where(Run.profit >= min_profit)

        runs = session.scalars(stmt).all()
        return [
            RunModel(
                run_id=run.id,
                job_id=run.job_id,
                symbol=run.symbol,
                profit=run.profit,
                run_month=run.run_month,
                custom_score=run.custom_score,
                trades=run.trades,
                drawdown=run.drawdown,
            )
            for run in runs
        ]


@router.get("/{run_id}", response_model=RunModel)
def get_run(run_id: int) -> RunModel:
    with get_session() as session:
        run = session.get(Run, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return RunModel(
            run_id=run.id,
            job_id=run.job_id,
            symbol=run.symbol,
            profit=run.profit,
            run_month=run.run_month,
            custom_score=run.custom_score,
            trades=run.trades,
            drawdown=run.drawdown,
        )
