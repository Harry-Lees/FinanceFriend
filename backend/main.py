import requests
import random
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException 
from typing import Dict, Generator, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from models import User, SessionLocal, Base, engine, Transaction, Merchant
from schemas import Token, TokenData
from api import CapitalOne

SECRET_KEY: str = 'spo0ky-scary-skeletons'
ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

cap1_jwt='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2MzQxNjk2MDAsImFwaV9zdWIiOiI0MDVjMGUyNDRlOWI3OWU4Y2M1M2ZiMGYwN2VmMTljYjIwMmUxZWQ2ZmViNWRhMzBkZjZhYmNjNGFmMjAyY2FhMTY0MjM3NzYwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTY0MjM3NzYwMCwiZGV2ZWxvcGVyX2lkIjoiNDA1YzBlMjQ0ZTliNzllOGNjNTNmYjBmMDdlZjE5Y2IyMDJlMWVkNmZlYjVkYTMwZGY2YWJjYzRhZjIwMmNhYSJ9.fNPaRoOcD1LT0niT6VTTpAkUWUq5JbLTWIOxf0x_zm08hKgrUjuYI6gWTUkWbgp579t7N5Qjkoc_u-n44dc6FQw8_MxXxFZTJY1xObTCk5expEbHBDw3B6nLrv8iL1k27dHMhh5O1u142YAz24nhuKJV4EJjqHrbDsnebg_jjTQofDu072JBwXY445f_CJbwaaimmLUIpw7_CGVTuWzd52gbxEK9Uo8Q2O4zBcTvkjOVDQ7k5S5Y6x7mU-9yePcFXpkvvYEXXs4F6w3sSIf6ecjrLZUovHh3J7vSPp_I3jy-EBlatuzNP4Qui6zUhZU598GsFmwNW_RZjFGpst4rJw'

# if we have an empty database, create the tables outlined in the models file,
# if the database already has tables, this doesn't do anything
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["sha256_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
capital_one = CapitalOne(cap1_jwt)
app = FastAPI()

def get_database() -> Generator[SessionLocal, None, None]:
    """create a database connection"""

    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

def verify_password(plain_password, hashed_password):
    """function to verify that the given plaintext password matches the password hash"""

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """function to return the hashed version of the given plaintext password"""

    return pwd_context.hash(password)

def authenticate_user(database, username: str, password: str) -> Optional[User]:
    """function to check that the given user is valid"""

    user = database.query(User).where(username==User.username).first()

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """creates an access token for the given user"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(database=Depends(get_database), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = database.query(User).where(User.username == token_data.username).first() 
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

def get_httpsession():
    """create a http session"""
    headers = {
        'Authorization': f'Bearer {cap1_jwt}',
        'Content-Type': 'application/json',
        'version': '1.0'
    }
    session=requests.Session()
    session.headers.update(headers)
    try:
        yield session
    finally:
        session.close()

@app.get('/user')
async def get_user_by_id(user_id: str, database = Depends(get_database)) -> Dict[str, str]:
    """endpoint to get the user given the unique user ID"""

    response = database.query(User).where(user_id == User.user_id).first()
    if not response:
        raise HTTPException(404, detail='there is no user with that ID')
    return response


@app.get('/user/username')
async def get_user_by_username(username: str, database = Depends(get_database)):
    """endpoint to get the user given the username"""

    response = database.query(User).where(username = User.username).first()
    if not response:
        raise HTTPException(404, detail='there is no user with that username')
    return response

def upload_transactions(account_id, transactions, database) -> None:
    """function to upload CapitalOne transactions to the database"""
    
    temp: List[Transaction] = []
    for transaction in transactions['Transactions']:
        if not database.query(Merchant).where(Merchant.name == transaction['merchant']['name']).first():
            merchant = transaction['merchant']
            database.add(Merchant(
                name=merchant['name'],
                category=merchant['category'],
                description=merchant['description']
            ))

        temp.append(Transaction(
            transaction_id=transaction['transactionUUID'],
            account_id=account_id,
            merchant=transaction['merchant']['name'],
            amount=float(transaction['amount']),
            credit_debit_indicator=transaction['creditDebitIndicator'],
            currency=transaction['currency'],
            timestamp=transaction['timestamp'],
            lat=float(transaction['latitude']),
            lon=float(transaction['longitude']),
            status=transaction['status'],
            message=transaction['message'],
            point_of_sale=transaction['pointOfSale']
        ))
    database.add_all(temp)
    database.flush()

async def create_transactions(user, capital_one_account_id, database) -> None:
    await asyncio.sleep(random.random())
    transactions = await capital_one.add_transactions(capital_one_account_id)
    if transactions is not None:
        upload_transactions(user.user_id, transactions, database)

@app.put('/user', status_code=201)
async def create_user(username: str, password: str, database = Depends(get_database), http_session = Depends(get_httpsession)) -> int:
    """
    function to create a user.
    This function will create a User in the database,
    create a CapitalOne account, and create some transactions for the CapitalOne account.
    """

    # create CapitalOne account and create some transactions
    account_details: Dict[str, str] = await capital_one.create_uk_account()
    account_id: int = account_details['Accounts'][0]['accountId']
    print(account_id)

    # add the user to the database and flush the connection to generate a unique ID,
    # this is required to link the transactions with the user
    password_hash: str = get_password_hash(password)
    user: User = User(username=username, password_hash=password_hash, api_id=account_id)
    database.add(user)
    database.flush()

    # upload the CapitalOne transactions to the database
    tasks: list = [create_transactions(user, account_id, database) for i in range(10)]
    await asyncio.gather(*tasks)

    database.commit()


@app.post("/token", response_model=Token)
async def login_for_access_token(database=Depends(get_database), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

