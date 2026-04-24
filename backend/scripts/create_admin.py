import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.utilizador import Utilizador
from app.auth.security import hash_password

db = SessionLocal()

password = hash_password("admin123")

admin = Utilizador(
    nome="Administrador",
    email="admin@email.com",
    password_hash=password,
    role="admin",
    ativo=True
)

db.add(admin)
db.commit()

print("Admin criado com sucesso!")
print("email: admin@email.com")
print("password: admin123")