import importlib

falcon_spec = importlib.util.find_spec("numpy")
if falcon_spec is None:
    raise Exception("Numpy module has not been installed.")

falcon_spec = importlib.util.find_spec("pyurdme")
if falcon_spec is None:
    raise Exception("Numpy module has not been installed.")
