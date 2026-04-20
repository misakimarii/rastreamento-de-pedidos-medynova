from fastapi import APIRouter, HTTPException, Response, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import verificar_senha, criar_token_sessao
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login_admin(dados: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == dados.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuário inativo")

    if not verificar_senha(dados.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = criar_token_sessao({
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    })

    response.set_cookie(
        key="admin_session",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 8
    )

    return {
        "success": True,
        "mensagem": "Login realizado com sucesso",
        "username": user.username,
        "is_admin": user.is_admin
    }


@router.post("/logout")
def logout_admin(response: Response):
    response.delete_cookie("admin_session")
    return {"success": True, "mensagem": "Logout realizado com sucesso"}


@router.get("/me")
def me(user: Usuario = Depends(get_current_user)):
    return {
        "success": True,
        "username": user.username,
        "is_admin": user.is_admin,
        "is_active": user.is_active
    }