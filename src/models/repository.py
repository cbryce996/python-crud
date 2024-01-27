from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.session import Base
from models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str):
        try:
            user = User(username=username, password=password)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            self.session.rollback()
            return None

    # Add other repository methods as needed
