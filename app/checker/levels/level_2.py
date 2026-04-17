def check(user_code: str):
    namespace = {}

    try:
        exec(user_code, namespace)
    except Exception as e:
        return False, {
            "type": "runtime_error",
            "message": str(e)
        }

    if "calculate" not in namespace:
        return False, {
            "type": "compile_error",
            "message": "Function calculate() not found"
        }

    calculate = namespace["calculate"]

    tests = [
        ((1, 2), 3),
        ((0, 0), 0),
        ((1, 1), 2),
        ((6, 6), 12),
        ((100, 100), 200)
    ]

    for i, (inp, expected) in enumerate(tests, start=1):
        try:
            result = calculate(*inp)
        except Exception as e:
            return False, {
                "type": "runtime_error",
                "test": i,
                "input": inp,
                "message": str(e)
            }

        if result != expected:
            return False, {
                "type": "wrong_answer",
                "test": i,
                "input": inp,
                "expected": expected,
                "got": result
            }

    return True, {
        "type": "success",
        "tests_passed": len(tests)
    }