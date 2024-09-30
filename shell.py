afrom IPython import embed
from app.backend.db import Base
from sqlalchemy import select, update, insert, delete
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources, typically in module scope
engine = create_engine("sqlite:///ecommerce.db", echo=True)

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

banner = "Additional imports:\n"
from app.main import app

banner = f"{banner}from app.main import app\n"



for clazz in Base.registry._class_registry.values():
    if hasattr(clazz, "__tablename__"):
        globals()[clazz.__name__] = clazz
        import_string = f"from {clazz.__module__} import {clazz.__name__}\n"
        banner = banner + import_string

embed(colors="neutral", banner2=banner)


# Example
# from app.models.review import Review
# with Session() as session:
#     result = session.scalars(select(Review).where(Review.is_active == True))
#     for review in result.all():
#        print(review.rating.grade, review.user.email)

