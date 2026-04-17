from sqlalchemy import create_engine, URL
import os
from schemas.chat_schema import Base

# Load PostgreSQL credentials
postgres_vars = {
    'POSTGRES_USER': os.getenv('POSTGRES_USER'),
    'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'POSTGRES_DB': os.getenv('POSTGRES_DB'),
    'DB_HOST': os.getenv('DB_HOST'),
    'DB_PORT': os.getenv('DB_PORT')
}

# Validate all required variables are set
for var_name, var_value in postgres_vars.items():
    if not var_value:
        raise ValueError(f"Missing environment variable: {var_name}")

POSTGRES_USER = postgres_vars['POSTGRES_USER']
POSTGRES_PASSWORD = postgres_vars['POSTGRES_PASSWORD']
POSTGRES_DB = postgres_vars['POSTGRES_DB']
DB_HOST = postgres_vars['DB_HOST']
DB_PORT = postgres_vars['DB_PORT']

url = URL.create(
    drivername="postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=POSTGRES_DB,
    query={"sslmode": "disable"}
)

# Initialize PostgreSQL engine and ensure schema exists
engine = create_engine(url)
Base.metadata.create_all(engine)