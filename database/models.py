from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional, Dict
from sqlalchemy import ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(primary_key=True)
    job_name: Mapped[str]
    expert_name: Mapped[str]
    expert_path: Mapped[str]
    strategy_version: Mapped[Optional[str]]

    modeling_mode: Mapped[Optional[str]]  # from [Tester]
    optimization_mode: Mapped[Optional[str]] = mapped_column(nullable=True)
    optimization_criterion: Mapped[Optional[str]] = mapped_column(nullable=True)
    period: Mapped[str]  # previously timeframe, now matches INI "Period"

    deposit: Mapped[float]
    currency: Mapped[str]
    leverage: Mapped[str]
    tester_inputs: Mapped[Dict[str, str]] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"), nullable=True)
    runs: Mapped[List["Run"]] = relationship(back_populates="job", cascade="all, delete-orphan")


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    job: Mapped[Job] = relationship(back_populates="runs")

    start_date: Mapped[date]
    end_date: Mapped[date]
    pass_number: Mapped[int]

    profit: Mapped[Optional[float]]
    drawdown: Mapped[Optional[float]]
    custom_score: Mapped[Optional[float]]
    win_rate: Mapped[Optional[float]]

    symbol: Mapped[str]
    run_month: Mapped[str]
    is_full_month: Mapped[bool]

    sharpe_ratio: Mapped[Optional[float]]
    trades: Mapped[Optional[int]]
    expected_payoff: Mapped[Optional[float]]
    recovery_factor: Mapped[Optional[float]]
    profit_factor: Mapped[Optional[float]]
    params_json: Mapped[Optional[dict]] = mapped_column(JSON)
    result_hash: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
