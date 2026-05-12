import subprocess
import json
import os


def check(user_code: str):
    tests = [
        (
            "ABBR: MSV-AA-R90\nName: aerophobous\nCrDat: 2042/11/05\nType: Зенитный ракетный комплекс\nRange: 90 км\nAmmo: 12 ракет\n\x1a\n",
            {
                "console_contains": "> aerophobous.json",
                "filename": "aerophobous.json",
                "expected_json": {
                    "ABBR": "MSV-AA-R90",
                    "Name": "aerophobous",
                    "CrDat": "2042/11/05",
                    "Type": "Зенитный ракетный комплекс",
                    "Range": "90 км",
                    "Ammo": "12 ракет"
                }
            }
        ),
        (
            "ABBR: MSV-LADS\nCrDat: 2045/13/40\nType: Лазерное ПВО\nPower: 150 kW\n\x1a\n",
            {
                "console_contains": "WARING: INCORRECT DATE INPUT",
                "console_contains2": "> unnamed.json",
                "filename": "unnamed.json",
                "expected_json": {
                    "ABBR": "MSV-LADS",
                    "Name": "N/A",
                    "CrDat": "N/A",
                    "Type": "Лазерное ПВО",
                    "Power": "150 kW"
                }
            }
        ),
        (
            "\nABBR:   MSV-CIWS-AA4   \n\nName:   pointdef    \nCrDat: 2043/03/17\n\nType:   Система ПВО малой дальности  \nCaliber: 30 mm\nRateOfFire: 4500 rounds/min\n\n\x1a\n",
            {
                "console_contains": "> pointdef.json",
                "filename": "pointdef.json",
                "expected_json": {
                    "ABBR": "MSV-CIWS-AA4",
                    "Name": "pointdef",
                    "CrDat": "2043/03/17",
                    "Type": "Система ПВО малой дальности",
                    "Caliber": "30 mm",
                    "RateOfFire": "4500 rounds/min"
                }
            }
        ),
    ]

    for i, (inp, expected) in enumerate(tests, start=1):
        try:
            proc = subprocess.run(
                ["python3", "-c", user_code],
                input=inp,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            result = proc.stdout.strip()
            
            console_ok = expected["console_contains"] in result
            if "console_contains2" in expected:
                console_ok = console_ok and expected["console_contains2"] in result
            
            filename = expected["filename"]
            json_ok = False
            filedata = None
            
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    filedata = json.load(f)
                json_ok = (filedata == expected["expected_json"])
                os.remove(filename)
            
            if not (console_ok and json_ok):
                if os.path.exists(filename):
                    os.remove(filename)
                    
                return False, {
                    "type": "wrong_answer",
                    "test": i,
                    "input": inp.replace('\x1a', '^Z'),
                    "expected_console": expected["console_contains"],
                    "expected_json": expected["expected_json"],
                    "got_console": result,
                    "got_json": filedata
                }
                
        except subprocess.TimeoutExpired:
            if os.path.exists(expected["filename"]):
                os.remove(expected["filename"])
            return False, {
                "type": "runtime_error",
                "test": i,
                "input": inp.replace('\x1a', '^Z'),
                "message": "Timeout (5 seconds)"
            }
        except Exception as e:
            if os.path.exists(expected["filename"]):
                os.remove(expected["filename"])
            return False, {
                "type": "runtime_error",
                "test": i,
                "input": inp.replace('\x1a', '^Z'),
                "message": str(e)
            }

    return True, {
        "type": "success",
        "tests_passed": len(tests)
    }