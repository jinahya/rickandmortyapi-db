from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    type: Mapped[str] = mapped_column(String())
    dimension: Mapped[str] = mapped_column(String())
    residents: Mapped[str] = mapped_column(String())
    url: Mapped[str] = mapped_column(String())
    created: Mapped[str] = mapped_column(String())

    # addresses: Mapped[List["Address"]] = relationship(
    #     back_populates="user", cascade="all, delete-orphan"
    # )

    def __repr__(self) -> str:
        return f"""Location(
        id={self.id!r},
        name={self.name!r},
        type={self.fullname!r}),
        dimension={self.dimension!r},
        residents={self.residents!r},
        url={self.url!r},
        created={self.created!r})
        """
