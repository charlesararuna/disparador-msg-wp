from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

# MySQL settings via .env
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "test")
MYSQL_PARAMS = os.getenv("MYSQL_PARAMS", "charset=utf8mb4")  # e.g., charset=utf8mb4

# SQLAlchemy database URL (PyMySQL driver)
# Example: mysql+pymysql://user:pass@host:3306/dbname?charset=utf8mb4
def _quote(value: str) -> str:
	"""Basic URL quoting for special characters in credentials."""
	from urllib.parse import quote_plus

	return quote_plus(value) if value is not None else ""

MYSQL_USER_Q = _quote(MYSQL_USER or "")
MYSQL_PASSWORD_Q = _quote(MYSQL_PASSWORD or "")

AUTH_PART = f"{MYSQL_USER_Q}:{MYSQL_PASSWORD_Q}@" if MYSQL_USER_Q or MYSQL_PASSWORD_Q else ""
HOST_PART = f"{MYSQL_HOST}:{MYSQL_PORT}"
PARAMS_PART = f"?{MYSQL_PARAMS}" if MYSQL_PARAMS else ""

DATABASE_URL = f"mysql+pymysql://{AUTH_PART}{HOST_PART}/{MYSQL_DB}{PARAMS_PART}"

# Optional engine kwargs from env
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() in ("1", "true", "yes", "on")
POOL_SIZE = int(os.getenv("SQL_POOL_SIZE", "5"))
POOL_RECYCLE = int(os.getenv("SQL_POOL_RECYCLE", "280"))
POOL_PRE_PING = os.getenv("SQL_POOL_PRE_PING", "true").lower() in ("1", "true", "yes", "on")
