from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime  # type: ignore

Base = declarative_base()

class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)  # type: ignore
    phone = Column(String, nullable=False)  # type: ignore  
    created_at = DateTime(auto_now_add=True)
    updated_at = DateTime(auto_now=True)

    def __repr__(self):
        return f"<User {self.name} {self.surname}>"
    
    # TODO add describe and declarative info


class UserSerssion(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    cookie = Column(String, nullable=False)
    expired_at = Column(DateTime, nullable=False)
    created_at = DateTime(auto_now_add=True)
    updated_at = DateTime(auto_now=True)

    def __repr__(self):
        return f"<UserSerssion {self.user_id} {self.created_at}>"
