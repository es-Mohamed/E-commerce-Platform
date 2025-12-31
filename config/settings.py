"""
Bridge module: expose the project's existing settings as `config.settings`.

This dynamically loads the top-level `settings.py` file and copies
uppercase attributes (Django settings) into this module's namespace so
Django can import `config.settings` normally.
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'settings.py'

spec = importlib.util.spec_from_file_location('project_settings', str(SOURCE))
project_settings = importlib.util.module_from_spec(spec)
sys.modules['project_settings'] = project_settings
spec.loader.exec_module(project_settings)

# Copy uppercase attributes (Django settings) into this module
for name, value in vars(project_settings).items():
    if name.isupper():
        globals()[name] = value
