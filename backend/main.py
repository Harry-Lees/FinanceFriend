from fastapi import FastAPI, Depends, HTTPException, Response
from typing import Dict, Generator
from models import User, SessionLocal, Base, engine

# if we have an empty database, create the tables outlined in the models file,
# if the database already has tables, this doesn't do anything
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_database() -> Generator[SessionLocal, None, None]:
    """create a database connection"""

    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


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
async def create_user(username: str, password: str, database = Depends(get_database)) -> int:
    user: User = User(username=username, password_hash=password, api_id=4)

    database.add(user)
    database.commit()
