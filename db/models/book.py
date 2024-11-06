from .. import Base

from sqlalchemy.orm import Mapped,mapped_column

class Book(Base):
    __tablename__ = "Books"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=True)