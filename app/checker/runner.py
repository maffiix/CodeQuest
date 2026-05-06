import importlib


def run_checker(checker_name, user_code):

    module_path = f"app.checker.levels.{checker_name}"

    checker_module = importlib.import_module(module_path)

    return checker_module.check(user_code)