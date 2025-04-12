# File: database/models.py
# Location: optibatch/database/models.py

from datetime import date, datetime
from typing import Optional
from sqlalchemy import (
    Integer,
    String,
    Float,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ----------------------------
# Tables
# ----------------------------


class Strategy(Base):
    __tablename__ = "strategies"
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_deposit: Mapped[Optional[float]] = mapped_column(nullable=True)
    default_modeling: Mapped[Optional[str]] = mapped_column(nullable=True)


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(nullable=False)
    expert_name: Mapped[str] = mapped_column(nullable=False)
    expert_path: Mapped[str] = mapped_column(nullable=False)
    strategy_version: Mapped[Optional[str]] = mapped_column(nullable=True)
    modeling_mode: Mapped[Optional[str]] = mapped_column(nullable=True)
    deposit: Mapped[float] = mapped_column()
    currency: Mapped[str] = mapped_column()
    leverage: Mapped[str] = mapped_column()
    tester_inputs: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    runs: Mapped[list["Run"]] = relationship("Run", back_populates="job")


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(nullable=False)
    timeframe: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    run_month: Mapped[str] = mapped_column(nullable=False)
    is_full_month: Mapped[bool] = mapped_column(default=False)
    pass_number: Mapped[int] = mapped_column(nullable=False)

    profit: Mapped[Optional[float]] = mapped_column()
    drawdown: Mapped[Optional[float]] = mapped_column()
    sharpe_ratio: Mapped[Optional[float]] = mapped_column()
    expected_payoff: Mapped[Optional[float]] = mapped_column()
    recovery_factor: Mapped[Optional[float]] = mapped_column()
    profit_factor: Mapped[Optional[float]] = mapped_column()
    trades: Mapped[Optional[int]] = mapped_column()
    custom_score: Mapped[Optional[float]] = mapped_column()

    params_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    result_hash: Mapped[Optional[str]] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    job: Mapped["Job"] = relationship("Job", back_populates="runs")
    parameters: Mapped[list["Parameter"]] = relationship(
        "Parameter", back_populates="run"
    )
    tags: Mapped[list["RunTag"]] = relationship("RunTag", back_populates="run")


class Parameter(Base):
    __tablename__ = "parameters"
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    optimize: Mapped[Optional[bool]] = mapped_column()

    run: Mapped["Run"] = relationship("Run", back_populates="parameters")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class RunTag(Base):
    __tablename__ = "run_tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), nullable=False)
    tag: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[Optional[str]] = mapped_column(nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    run: Mapped["Run"] = relationship("Run", back_populates="tags")
    user: Mapped[Optional["User"]] = relationship("User")


class IniExport(Base):
    __tablename__ = "ini_exports"
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), nullable=False)
    export_path: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
