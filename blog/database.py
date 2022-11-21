from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLITE_URL = 'sqlite:///./{filename}'
# MYSQL_URL = 'mysql+pymysql://{username}:{password}@{host}:{port}'
# POSTGRES_URL = 'postgresql://{username}:{password}@{host}:{port}/{dbname}

filename = 'blog.db'

DB_URL = f'sqlite:///./{filename}'

engine = create_engine(DB_URL, connect_args = {'check_same_thread': False}) #connect_args only for sqlite

SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()