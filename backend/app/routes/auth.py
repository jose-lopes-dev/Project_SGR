import token

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.utilizador import Utilizador
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from app.auth.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    utilizador = db.query(Utilizador).filter(
        Utilizador.email == form_data.username
    ).first()

    if not utilizador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    if not verify_password(form_data.password, utilizador.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    token = create_access_token(
        data={
            "sub": utilizador.email,
            "role": utilizador.role
        }
    )

    return {
"access_token": token,
"token_type": "bearer",
"role": utilizador.role
}