from fastapi import Cookie, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import verificar_token_sessao


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    admin_session: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not admin_session:
        raise HTTPException(status_code=401, detail="Não autenticado")

    payload = verificar_token_sessao(admin_session)
    if not payload:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    user = db.query(Usuario).filter(
        Usuario.id == user_id,
        Usuario.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado ou inativo")

    return user


def require_admin(user: Usuario = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user