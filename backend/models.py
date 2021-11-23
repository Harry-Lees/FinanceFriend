from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String, Integer, Column, Float, DateTime
from sqlalchemy.sql.schema import ForeignKey

SQLALCHEMY_DATABASE_URL: str = ''
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__: str = 'users_tab'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True)
    password_hash = Column(String(256))
    api_id = Column(Integer, unique=True)

class Transaction(Base):
    __tablename__: str = 'transaction_tab'

    transaction_id = Column(String, primary_key=True, index=True)
    amount = Column(Float)
    currency = Column(String)
    credit_debit_indicator = Column(String)
    timestamp = Column(DateTime, index=True)
    lat = Column(Float)
    lon = Column(Float)
    status = Column(String)
    message = Column(String)
    point_of_sale = Column(String)

    @declared_attr
    def merchant(cls) -> Column:
        return Column(String, ForeignKey('merchant_tab.name'))

    @declared_attr
    def account_id(cls) -> Column:
        return Column(Integer, ForeignKey('users_tab.user_id'))

class Merchant(Base):
    __tablename__: str = 'merchant_tab'

    name = Column(String, primary_key=True, index=True)

    category = Column(String)
    description = Column(String)
