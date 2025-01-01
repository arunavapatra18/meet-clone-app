from fastapi.responses import RedirectResponse
import jwt

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.db import db_session_dependency
from app.core.utils import create_access_token, generate_password_hash, verify_password
from app.models import LoginResponse, RegisterResponse, TokenData, UserGetResponse, UserRegister, User
from app.user.service import get_user_by_email, get_user_by_id


auth_router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

auth_dependency = Annotated[str, Depends(oauth2_scheme)]

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def authenticate_user(session: db_session_dependency, email: str, password: str):
    """Authenticate user

    Args:
        session (db_session_dependency): DB Session
        email (str): Input Email
        password (str): Input Password

    Returns:
        User: Authenticated user
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


def verify_access_token(token: str, credentials_exception: HTTPException):
    """Verify access token

    Args:
        token (str): JWT
        credentials_exception (HTTPException): Credentials exception

    Raises:
        credentials_exception: 401 - Credential exception

    Returns:
        TokenData: Response with token
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data


async def get_current_user(session: db_session_dependency, token: auth_dependency):
    """Get current user

    Args:
        token (auth_dependency): Depends on auth_dependency for access_token

    Raises:
        credentials_exception: 401 - Could not validate credentials

    Returns:
        User: Current user
    """
    token_data = verify_access_token(
        token=token, credentials_exception=credentials_exception
    )
    db_user = get_user_by_id(session=session, id=token_data.user_id)
    if not db_user:
        raise credentials_exception
    return db_user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get current active user

    Args:
        current_user (Annotated[User, Depends): Depends on get_current_user

    Raises:
        HTTPException: 400 - Inactive user

    Returns:
        User: Current active user
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user

@auth_router.post("/login", response_model=LoginResponse)
async def login_user(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: db_session_dependency,
    response: Response
):
    """User Login Route Handler

    Args:
        login_data (Annotated[OAuth2PasswordRequestForm, Depends): Depends on OAuth2PasswordRequestForm to get username and password from client
        session (db_session_dependency): DB Session

    Raises:
        HTTPException: 401 - Incorrect username or password

    Returns:
        LoginResponse: Respose containing access token
    """
    db_user = authenticate_user(session, login_data.username, login_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=access_token_expires)
    return LoginResponse(access_token=access_token, token_type="bearer")


@auth_router.post("/register", response_model=RegisterResponse)
async def register_user(user_data: UserRegister, session: db_session_dependency):
    """User Register Route Handler

    Args:
        user_data (UserRegister): User data input
        session (db_session_dependency): DB Session

    Raises:
        HTTPException: 409 - Email Already Exists

    Returns:
        RegisterResponse: Response with user id
    """
    db_user = get_user_by_email(session, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already taken!"
        )

    hashed_password = generate_password_hash(user_data.password)
    db_user = User(email=user_data.email, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return RegisterResponse(message="User registered successfully", user_id=db_user.id)


@auth_router.get("/users/me/", response_model=UserGetResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.get("/status/")
async def auth_status(request: Request):
    print(request.headers)
    token = request.cookies.get("access_token")
    print(f"Recv token:{token}")
    if not token:
        return {"is_authenticated": False}
    try:
        token_data = verify_access_token(token, credentials_exception=credentials_exception)
        if token_data:
            return {"is_authenticated": True}
    except HTTPException:
        return {"is_authenticated": False}
        

@auth_router.post("/logout/")
async def logout(request: Request):
    response = RedirectResponse(url="http://127.0.0.1:5173/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response