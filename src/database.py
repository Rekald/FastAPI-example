from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from src.dependencies import db_root

engine = create_engine(db_root)


class Base(DeclarativeBase):
    ...


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[int] = mapped_column(default="ro", nullable=False)


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    part_code: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    producer: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(default=False)
    catalog_price: Mapped[float] = mapped_column(default=False)
    discount: Mapped[float] = mapped_column(default=False)
    buy_price: Mapped[float] = mapped_column(default=False)
    total_value: Mapped[float] = mapped_column(default=False)


class Rents(Base):
    __tablename__ = "rents"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    part_code: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(default=False)
    position: Mapped[str] = mapped_column(nullable=True)
    rent_date: Mapped[str] = mapped_column(nullable=False)


Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(engine, autoflush=True)

