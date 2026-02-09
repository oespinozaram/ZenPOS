import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine # El engine sigue siendo de SQLAlchemy
from sqlmodel.ext.asyncio.session import AsyncSession # <--- IMPORTANTE: La sesión debe ser de SQLModel
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

# Selección dinámica del Engine
if APP_ENV == "production":
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    # Driver async para MariaDB
    DATABASE_URL = f"mysql+asyncmy://{user}:{password}@{host}/{db_name}"
else:
    # Driver async para SQLite
    DATABASE_URL = "sqlite+aiosqlite:///database.db"

# Crear el motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Factory de sesiones
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Crea las tablas si no existen"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session