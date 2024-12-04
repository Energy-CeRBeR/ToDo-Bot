import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[str] = mapped_column(default="default", nullable=False)
    refresh_token: Mapped[str] = mapped_column(default="default", nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
