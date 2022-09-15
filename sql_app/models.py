from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class todo(Base):
    __tablename__ = "todo"

    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(30), index=True)
    isEnd = Column(Integer, index=True)
    

    #owner = relationship("User", back_populates="items")