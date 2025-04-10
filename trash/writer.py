from core.input_parser import InputParam
from pathlib import Path


def update_ini_tester_inputs(path: Path, inputs: list[InputParam]) -> None:
    if not path.exists():
        return

    lines = path.read_text(encoding="utf-16").splitlines()
    output: list[str] = []

    inside_tester_inputs = False

    for line in lines:
        stripped = line.strip()

        if stripped == "[TesterInputs]":
            # Start replacing this section
            output.append("[TesterInputs]")
            for param in inputs:
                parts = [
                    param.default,
                    param.start or "",
                    param.step or "",
                    param.end or "",
                    "Y" if param.optimize else "N",
                ]
                output.append(f"{param.name} = {'||'.join(parts)}")
            inside_tester_inputs = True
            continue

        # Skip all lines in the original [TesterInputs] block
        if inside_tester_inputs:
            if stripped.startswith("[") and stripped.endswith("]"):
                inside_tester_inputs = False
                output.append(line)
            continue

        output.append(line)

    path.write_text("\n".join(output), encoding="utf-16", newline="\r\n")
