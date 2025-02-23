from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from .config import get_settings

settings = get_settings()

url_object = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PWD,
    host=settings.POSTGRES_SERVER,
    port=settings.PGPORT,
    database=settings.POSTGRES_DB,
)

engine = create_engine(url_object)

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

Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(engine, autoflush=True)

