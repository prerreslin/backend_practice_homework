from .. import Base
from datetime import date as datetim
from sqlalchemy.orm import Mapped,mapped_column,relationship,validates


class Event(Base):
    __tablename__ = "Events"

    title: Mapped[str] = mapped_column(nullable=False, autoincrement=True)
    description: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetim] = mapped_column(nullable=False)
    is_public: Mapped[bool] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    executors: Mapped[str] = mapped_column(nullable=True)

    def add_executor(self, user: "User") -> None:
        executor_ids = self.get_executor_ids()
        if user.id not in executor_ids:
            executor_ids.append(user.id)
            self.executors = ",".join(map(str, executor_ids))

    def get_executor_ids(self) -> list[int]:
        if self.executors:
            return list(map(int, self.executors.split(",")))
        return []