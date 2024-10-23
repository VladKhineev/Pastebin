from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy import text as textS
from typing import Annotated
from datetime import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, 50]
class Base(DeclarativeBase):
    type_annotated_map = {
        str_50: String(50)
    }

    repr_cols_num = 6
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"



class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    username: Mapped[str_50]

    post: Mapped[list['Post']] = relationship(back_populates='user')

class Post(Base):
    __tablename__ = 'post'

    id: Mapped[intpk]
    title: Mapped[str_50]
    text: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(server_default=textS("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=textS("TIMEZONE('utc', now())"), onupdate=datetime.utcnow())

    user: Mapped['User'] = relationship(back_populates='post')