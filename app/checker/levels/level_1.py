def check(user_code: str):
    namespace = {}

    try:
        exec(user_code, namespace)
    except Exception as e:
        return False, {
            "type": "runtime_error",
            "message": str(e)
        }

    if "greet" not in namespace:
        return False, {
            "type": "compile_error",
            "message": "Function greet() not found"
        }

    greet = namespace["greet"]

    tests = [
        ("Alex", "Hello, Alex!"),
        ("Python", "Hello, Python!"),
        ("World", "Hello, World!")
    ]

    for i, (inp, expected) in enumerate(tests, start=1):
        try:
            result = greet(inp)
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