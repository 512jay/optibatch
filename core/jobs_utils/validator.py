# File: core/jobs/validator.py
from state.app_state import AppState


def validate_config(state: AppState) -> list[str]:
    errors = []

    if not state.expert_path_var.get():
        errors.append("Expert path is required.")

    if not state.symbol_var.get():
        errors.append("At least one symbol must be selected.")

    try:
        float(state.deposit_var.get())
    except ValueError:
        errors.append("Deposit must be a valid number.")

    return errors
