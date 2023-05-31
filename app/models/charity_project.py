from sqlalchemy import Column, String, Text

from app.core.constants import LENGTH
from app.core.db import Base
from app.models.base import AbstractMixin


class CharityProject(AbstractMixin, Base):
    name = Column(String(LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
