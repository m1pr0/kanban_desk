from sqlalchemy import Column as SA_Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Column(Base):
    __tablename__ = "columns"

    id = SA_Column(Integer, primary_key=True, index=True)
    title = SA_Column(String, nullable=False)
    project_id = SA_Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    order = SA_Column(Integer, default=0)

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="column", cascade="all, delete")