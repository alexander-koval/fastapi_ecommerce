from IPython import embed
from app.backend.db import Base

banner = "Additional imports:\n"
from app.main import app

banner = f"{banner}from app.main import app\n"


for clazz in Base.registry._class_registry.values():
    if hasattr(clazz, "__tablename__"):
        globals()[clazz.__name__] = clazz
        import_string = f"from {clazz.__module__} import {clazz.__name__}\n"
        banner = banner + import_string

embed(colors="neutral", banner2=banner)
