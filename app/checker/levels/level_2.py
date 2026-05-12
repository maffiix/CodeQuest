import subprocess


def check(user_code: str):
    tests = [
        ("""BH-01-1
BH-01-2
END
J-1212 J-24:10 J-50:5 J-60:7 BH-01-1:1
J-24 J-1212:10 J-70:4 J-80:6 BH-01-2:1
J-50 J-1212:5 J-90:3 J-100:2 J-110:4
J-60 J-1212:7 J-120:5 J-130:6 J-140:8
END
J-50:J-90
END_ALL""", "BH-01-1 41"),
        ("""BH-1-1
BH-01-2
END
J-1212 J-24:10 J-50:5 J-60:7 BH-01-2:1
J-24 J-1212:10 J-70:4 J-80:6 J-90:3
END
END_ALL""", "INCORRECT INPUT: invalid exit format 'BH-1-1'"),
        ("""BH-01-1
END
J-1212 J-24:10 J-50:5 BH-01-1:1
J-24 J-1212:10 J-70:4 J-80:6 J-90:3
END
END_ALL""", "INCORRECT INPUT: node J-1212 has 3 connections, expected 4"),
        ("""BH-01-1
BH-01-2
END
J-1212 J-50:5 J-60:7 J-70:3 BH-01-1:1
J-24 J-80:4 J-90:2 J-100:6 BH-01-2:1
J-50 J-1212:5 J-110:4 J-120:3 J-130:2
J-80 J-24:4 J-140:5 J-150:6 J-160:7
END
END_ALL""", "INCORRECT INPUT: no valid path found")
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