from app.database import engine, Base
from app.models import user

Base.metadata.create_all(bind=engine)
