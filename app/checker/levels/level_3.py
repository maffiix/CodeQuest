import subprocess
import json
import os


def check(user_code: str):
    tests = [
        ("ABCD-1111-BOSCALI\n", {"console": "", "file_output": "", "output_file": ""}),
    ]

    for i, (inp, expected) in enumerate(tests, start=1):
        console = expected["console"]
        file_output = expected["filename"]
        output_file = expected["output_file"]
        try:
            proc = subprocess.run(
                ["python3", "-c", user_code],
                input=inp,
                capture_output=True,
                text=True
            )
            result = proc.stdout.strip()
            filedata = json.loads(open(output_file, "r").read())
            solved = (filedata == file_output) and (result == console)
            os.remove(output_file)
            if not solved:
                return False, {
                    "type": "wrong_answer",
                    "test": i,
                    "input": inp,
                    "expected": expected,
                    "got": result
                }
        except Exception as e:
            return False, {
                "type": "runtime_error",
                "test": i,
                "input": inp,
                "message": str(e)
            }

    return True, {
        "type": "success",
        "tests_passed": len(tests)
    }