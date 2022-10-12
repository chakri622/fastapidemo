from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from starlette import status

from db import get_session
from schemas import UserOutput, User

URL_PREFIX="/auth"
router=APIRouter(prefix=URL_PREFIX)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= f"{URL_PREFIX}/token")
'''
#Basic Authentication - username and password
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security),
                     session: Session = Depends(get_session)) -> UserOutput:
    query = select(User).where(User.username == credentials.username)
    user = session.exec(query).first()
    if user and user.verify_password(credentials.password):
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or Password is incorrect")

'''


def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> UserOutput:
    query = select(User).where(User.username == token)
    user = session.exec(query).first()
    if user:
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or Password is incorrect",
            headers={"WWW-Authenticate": "Bearer"})


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm =  Depends(),
                session: Session = Depends(get_session)):
    query = select(User).where(User.username == form_data.username)
    user = session.exec(query).first()
    if user and user.verify_password(form_data.password):
        return { "access_token": user.username, "token_type": "Bearer"}
    else:
        raise HTTPException(
            status_code=400,
            detail="Incorrect Username or Password")


@router.post("/api/user")
async def add_user(username: str, password: str,  session: Session = Depends(get_session)):
    if username and password:
        new_user = User()
        new_user.username = username
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    else:
        raise HTTPException(
            status_code=400,
            detail="Empty Username or Password")