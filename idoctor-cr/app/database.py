from __future__ import annotations

from pathlib import Path
from contextlib import contextmanager

from sqlmodel import SQLModel, Session, create_engine


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{(DATA_DIR / 'app.db').as_posix()}"
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Session:
    with Session(engine) as session:
        yield session