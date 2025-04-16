from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, func
from backend.db import get_session
from database.models import Run

router = APIRouter()


class SummaryStats(BaseModel):
    top_symbol: str
    best_month: str
    worst_month: str
    average_profit: float

    model_config = {"from_attributes": True}


@router.get("/summary", response_model=SummaryStats)
def get_summary_stats() -> SummaryStats:
    with get_session() as session:
        # Get total profit per symbol
        symbol_profit_stmt = select(Run.symbol, func.sum(Run.profit)).group_by(Run.symbol)
        symbol_results = session.execute(symbol_profit_stmt).all()
        symbol_profit = dict(symbol_results)

        # Get total profit per run month
        month_profit_stmt = select(Run.run_month, func.sum(Run.profit)).group_by(Run.run_month)
        month_results = session.execute(month_profit_stmt).all()
        month_profit = dict(month_results)

        if not symbol_profit or not month_profit:
            raise Exception("Insufficient data to compute summary.")

        top_symbol = max(symbol_profit, key=symbol_profit.get)
        best_month = max(month_profit, key=month_profit.get)
        worst_month = min(month_profit, key=month_profit.get)

        avg_profit_stmt = select(func.avg(Run.profit))
        average_profit = session.scalar(avg_profit_stmt)

        return SummaryStats(
            top_symbol=top_symbol,
            best_month=best_month,
            worst_month=worst_month,
            average_profit=average_profit
        )
