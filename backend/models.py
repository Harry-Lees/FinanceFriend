from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String, Integer, Column

SQLALCHEMY_DATABASE_URL: str = 'postgresql://aosjkguddchbnf:db0a47e3ed71b98a7f4d5766bbec92e128806b493d6bb8912941d911770dc65a@ec2-63-33-14-215.eu-west-1.compute.amazonaws.com:5432/dftnmhsp6ucj83'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__: str = 'users_tab'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True)
    password_hash = Column(String(256))
    api_id = Column(Integer, unique=True)
