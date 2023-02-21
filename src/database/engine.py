from sqlalchemy.engine import create_engine

engine = create_engine(
    url="postgresql+psycopg2://test:test@localhost/test"
)

