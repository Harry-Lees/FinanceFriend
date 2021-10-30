import requests
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException 
from typing import Dict, Generator, Optional
from models import User, SessionLocal, Base, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas import Token, TokenData

SECRET_KEY: str = 'spo0ky-scary-skeletons'
ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

cap1_jwt='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2MzQxNjk2MDAsImFwaV9zdWIiOiI0MDVjMGUyNDRlOWI3OWU4Y2M1M2ZiMGYwN2VmMTljYjIwMmUxZWQ2ZmViNWRhMzBkZjZhYmNjNGFmMjAyY2FhMTY0MjM3NzYwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTY0MjM3NzYwMCwiZGV2ZWxvcGVyX2lkIjoiNDA1YzBlMjQ0ZTliNzllOGNjNTNmYjBmMDdlZjE5Y2IyMDJlMWVkNmZlYjVkYTMwZGY2YWJjYzRhZjIwMmNhYSJ9.fNPaRoOcD1LT0niT6VTTpAkUWUq5JbLTWIOxf0x_zm08hKgrUjuYI6gWTUkWbgp579t7N5Qjkoc_u-n44dc6FQw8_MxXxFZTJY1xObTCk5expEbHBDw3B6nLrv8iL1k27dHMhh5O1u142YAz24nhuKJV4EJjqHrbDsnebg_jjTQofDu072JBwXY445f_CJbwaaimmLUIpw7_CGVTuWzd52gbxEK9Uo8Q2O4zBcTvkjOVDQ7k5S5Y6x7mU-9yePcFXpkvvYEXXs4F6w3sSIf6ecjrLZUovHh3J7vSPp_I3jy-EBlatuzNP4Qui6zUhZU598GsFmwNW_RZjFGpst4rJw'

# if we have an empty database, create the tables outlined in the models file,
# if the database already has tables, this doesn't do anything
Base.metadata.create_all(bind=engine)


pwd_context = CryptContext(schemes=["sha256_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

def get_database() -> Generator[SessionLocal, None, None]:
    """create a database connection"""

    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(database, username: str, password: str):
    user=database.query(User).where(username==User.username).first()
    
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
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


@app.put('/user', status_code=201)
async def create_user(username: str, password: str, database = Depends(get_database), http_session = Depends(get_httpsession)) -> int:
    response = http_session.post('https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/accounts/create', 
           json={"quantity": 1, "numTransactions": 25, "liveBalance": True})
    data=response.json()
    password_hash=get_password_hash(password)

    user: User = User(username=username, password_hash=password_hash, api_id=int(data['Accounts'][0]['accountId']))

    database.add(user)
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

