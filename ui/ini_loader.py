from tkinter import filedialog
from pathlib import Path
from core.loader import load_ini_file
from core.session import cache_ini_file
from core.input_parser import parse_ini_inputs


def load_ini_and_update_ui(
    root, parsed_inputs_holder, update_fields_callback, post_input_callback=None
):
    file_path = filedialog.askopenfilename(
        title="Select INI File", filetypes=[("INI Files", "*.ini")]
    )
    if not file_path:
        return

    data = load_ini_file(Path(file_path))
    cache_ini_file(Path(file_path), data)
    parsed_inputs_holder.clear()
    parsed_inputs_holder.extend(parse_ini_inputs(data.get("inputs", {})))

    update_fields_callback(data)

    if post_input_callback:
        post_input_callback()
