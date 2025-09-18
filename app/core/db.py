from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError

try:
    # Import settings to get DATABASE_URL and engine options
    from settings import DATABASE_URL, SQL_ECHO, POOL_SIZE, POOL_RECYCLE, POOL_PRE_PING
except Exception as e:  # pragma: no cover
    raise RuntimeError(f"Failed to import settings: {e}")


class Base(DeclarativeBase):
    pass


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
    pool_size=POOL_SIZE,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=POOL_PRE_PING,
    future=True,
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    """Yield a DB session (FastAPI-style dependency pattern)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_database() -> bool:
    """Return True if a simple SELECT 1 works, else False."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False
