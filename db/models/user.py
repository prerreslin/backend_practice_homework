from .. import Base

from sqlalchemy.orm import Mapped,mapped_column,relationship

class User(Base):
    __tablename__ = "Users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    has_permission: Mapped[bool] = mapped_column(nullable=False)
    