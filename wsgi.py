import importlib.util

# Explicitly load app.py module to prevent Python from importing the app/ directory package
spec = importlib.util.spec_from_file_location("app_main", "app.py")
app_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_main)

app = app_main.app
