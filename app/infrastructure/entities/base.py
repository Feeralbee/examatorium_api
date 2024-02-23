import datetime

from sqlalchemy import UUID, text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, index=True,
        server_default=text("gen_random_uuid()::uuid")
    )

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text("(timezone('utc', now()))"))

    def __repr__(self):
        values = {i.name: getattr(self, i.name, None) for i in self.metadata.tables[self.__tablename__].columns}
        return f'<{self.__class__.__name__} {" ".join([f"{k}={v}" for k, v in values.items()])}>'



