import subprocess


def check(user_code: str):
    tests = [
        ("1\n2\n", "3"),
        ("o\n0\n", "0"),
        ("1\n1\n", "2"),
        ("6\n6\n", "12"),
        ("100\n100\n", "200")
    ]

    for i, (inp, expected) in enumerate(tests, start=1):
        try:
            proc = subprocess.run(
                ["python", "-c", user_code],
                input=inp,
                capture_output=True,
                text=True
            )
            result = proc.stdout.strip()
            if result != expected:
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