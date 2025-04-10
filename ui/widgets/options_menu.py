# File: ui/widgets/options_menu.py
from tkinter import Menu, BooleanVar
from core.state import registry

# Define your toggle options here
TOGGLE_OPTIONS = [
    ("Use Month-to-Month Windows", "use_discrete_months"),
    ("Enable Report Export", "export_reports"),
    ("Skip Symbols with Cached Results", "skip_cached_results"),
    ("Save Last Opened File Path", "save_last_path"),
]


def build_options_menu(parent_menu: Menu) -> tuple[Menu, dict[str, BooleanVar]]:
    var_map: dict[str, BooleanVar] = {}
    options_menu = Menu(parent_menu, tearoff=0)

    for label, key in TOGGLE_OPTIONS:
        var_map[key] = BooleanVar(value=registry.get(key, False))

        def on_toggle(k=key, v=var_map[key]):
            registry.set(k, v.get())
            registry.save()

        options_menu.add_checkbutton(
            label=label,
            variable=var_map[key],
            onvalue=True,
            offvalue=False,
            command=on_toggle,
        )

    return options_menu, var_map
