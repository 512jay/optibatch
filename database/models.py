"""Database models for OptiBatch – job definitions, runs, users, and strategies."""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional, Dict, Union

import enum
from sqlalchemy import (
    ForeignKey,
    JSON,
    Text,
    Enum,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

TypedValue = Union[str, int, float, bool]

# Base class for all models
class Base(DeclarativeBase):
    pass


# Enum for run-level status tracking
class RunStatus(enum.Enum):
    new = "new"
    reviewed = "reviewed"
    flagged = "flagged"


# Strategy metadata (useful if multiple EAs are tracked)
class Strategy(Base):
    __tablename__ = "strategies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    jobs: Mapped[List["Job"]] = relationship(
        back_populates="strategy", cascade="all, delete-orphan"
    )


# Optional user model for future SaaS expansion
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    jobs: Mapped[List["Job"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


# High-level optimization job (usually one INI file = one job)
class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(primary_key=True)
    job_name: Mapped[str]
    expert_name: Mapped[str]
    expert_path: Mapped[str]
    strategy_version: Mapped[Optional[str]]

    # Optimization/Test Settings
    model: Mapped[Optional[str]] = mapped_column(nullable=True)
    optimization_mode: Mapped[Optional[str]] = mapped_column(nullable=True)
    optimization_criterion: Mapped[Optional[str]] = mapped_column(nullable=True)
    period: Mapped[str]  # e.g., H1, M5

    deposit: Mapped[float]
    currency: Mapped[str]
    leverage: Mapped[str]
    tester_inputs: Mapped[Dict[str, TypedValue]] = mapped_column(JSON)

    # Audit
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Optional: user and strategy relations
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    user: Mapped[Optional["User"]] = relationship(back_populates="jobs")

    strategy_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("strategies.id"), nullable=True
    )
    strategy: Mapped[Optional["Strategy"]] = relationship(back_populates="jobs")

    # Optional Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_archived: Mapped[bool] = mapped_column(default=False)
    execution_host: Mapped[Optional[str]] = mapped_column(nullable=True)

    # Relationships
    runs: Mapped[List["Run"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )


# Result of a single optimization pass
class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    job: Mapped["Job"] = relationship(back_populates="runs")

    start_date: Mapped[date]
    end_date: Mapped[date]
    pass_number: Mapped[int]
    result: Mapped[float] = mapped_column(nullable=True)

    # Metrics
    profit: Mapped[Optional[float]]
    drawdown: Mapped[Optional[float]]
    custom_score: Mapped[Optional[float]]
    sharpe_ratio: Mapped[Optional[float]]
    trades: Mapped[Optional[int]]
    expected_payoff: Mapped[Optional[float]]
    recovery_factor: Mapped[Optional[float]]
    profit_factor: Mapped[Optional[float]]

    # Metadata
    symbol: Mapped[str]
    run_month: Mapped[str]
    is_full_month: Mapped[bool]
    params_json: Mapped[Optional[dict]] = mapped_column(JSON)
    result_hash: Mapped[Optional[str]]

    # Audit
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Optional user-defined fields
    tags: Mapped[List[str]] = mapped_column(JSON, default=[])
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    run_label: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.new)
    is_archived: Mapped[bool] = mapped_column(default=False)
