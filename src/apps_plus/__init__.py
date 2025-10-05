import json
import requests
import re
import sys
import subprocess
from pathlib import Path


def get_apps_data() -> dict:
    """parse APPS+ into a dict."""
    data_path = Path(__file__).parent.parent.parent / "data" / "v1" / "data.json"
    with open(data_path, "r") as file:
        data = json.load(file)
    return data


def run_python_script(
    script: str | Path,
    stdin_data: str = "",
    timeout_sec: float = 5.0,
):
    try:
        result = subprocess.run(
            [sys.executable, str(script)],  # run another .py with your current Python
            input=stdin_data,  # send to stdin
            capture_output=True,  # capture stdout & stderr
            text=True,  # str in/out instead of bytes (use encoding=... if needed)
            timeout=timeout_sec,  # seconds
            check=False,  # don't raise on non-zero exit
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as e:
        # e.stdout / e.stderr may contain partial output
        return {
            "returncode": None,
            "stdout": e.stdout if e.stdout is not None else "",
            "stderr": e.stderr if e.stderr is not None else "",
            "timed_out": True,
        }


def is_void_function_signature(s: str) -> bool:
    pattern = r"^\s*def\s+[A-Za-z_]\w*\s*\(\)\s*:$"
    return bool(re.match(pattern, s))


def get_function_name(s: str) -> str | None:
    pattern = r"^\s*def\s+([A-Za-z_]\w*)\s*\(\)\s*:$"
    match = re.match(pattern, s)
    return match.group(1) if match else None


def evaluate_void_function(function_name, inputs, outputs, solution):
    import tempfile

    with tempfile.NamedTemporaryFile("w") as file:
        file.write(solution)
        file.write(f"\n\n{function_name}()\n")
        file.flush()

        results = []
        for i in inputs:
            res = run_python_script(file.name, i, 5)
            results.append(res["stdout"])

        results = [s.strip() for s in results]
        results = [s.replace(" \n", "\n") for s in results]
        outputs = [s.strip() for s in outputs]
        outputs = [s.replace(" \n", "\n") for s in outputs]
        if results != outputs:
            print(outputs)
            print(results)

        if results == outputs:
            return "passed"
        return "failed"


def evaluate_apps_solution(starter, inputs, outputs, solution):
    if is_void_function_signature(starter):
        function_name = get_function_name(starter)
        return evaluate_void_function(function_name, inputs, outputs, solution)
    return "can't run"
