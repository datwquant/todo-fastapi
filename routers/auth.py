from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserLogin, UserResponse
from repositories.user_repository import UserRepository
from db.session import SessionLocal
from core.security import hash_password, verify_password, create_access_token
from jose import jwt
from core.security import SECRET_KEY, ALGORITHM
from core.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    if repo.get_by_email(data.email):
        raise HTTPException(400, "Email already exists")

    hashed = hash_password(data.password)
    return repo.create(data.email, hashed)



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    repo = UserRepository(db)
    user = repo.get_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id)}   # 🔥 QUAN TRỌNG
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    return current_user