from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]] = mapped_column(index=True, default=None)
    