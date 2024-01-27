from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

# Creating the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Creating the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the base class for declarative models
Base = declarative_base()

# Initializing the session in the app context
def init_db(app):
    with app.app_context():
        Base.metadata.create_all(bind=engine)

# Function to get a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
