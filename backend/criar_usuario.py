from app.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import gerar_hash_senha


def criar_usuario(username: str, senha: str, is_admin: bool = True):
    db = SessionLocal()

    existe = db.query(Usuario).filter(Usuario.username == username).first()
    if existe:
        print("Usuário já existe.")
        db.close()
        return

    novo_usuario = Usuario(
        username=username,
        password_hash=gerar_hash_senha(senha),
        is_admin=is_admin,
        is_active=True
    )

    db.add(novo_usuario)
    db.commit()
    db.close()

    print("Usuário criado com sucesso.")


if __name__ == "__main__":
    username = input("Usuário: ").strip()
    senha = input("Senha: ").strip()
    criar_usuario(username, senha, True)