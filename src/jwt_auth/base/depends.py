from database.session import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
