from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


engine = create_engine("sqlite:///test.db", echo=True)
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True,unique=True)


def up():
    Base.metadata.create_all(engine)

def down():
    Base.metadata.drop_all(engine)

from .models import Book,User,Event

down()
up()
