import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# .env 경로 로딩
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# 환경변수에서 DB URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# DB 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True  # SQL 로그 보기 원치 않으면 False로
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델들이 상속할 베이스 클래스
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()