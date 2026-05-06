import subprocess


def check(user_code: str):
    tests = [
        ("ABCD-1111-BOSCALI\n", "2E996AB-BOSCALI"),
        ("A2BDS-122456-BASD\n", "Неверный формат. Используйте: ABCD-1111-BOSCALI"),
        ("BBAC-1152-PRIMERVA\n", "34C8600-PRIMERVA")
    ]

    for i, (inp, expected) in enumerate(tests, start=1):
        try:
            proc = subprocess.run(
                ["python3", "-c", user_code],
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