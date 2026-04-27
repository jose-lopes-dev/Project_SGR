from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.auth.dependencies import get_current_admin
from app.auth.dependencies import get_current_user

from app.database import get_db
from app.models.utilizador import Utilizador
from app.schemas.utilizador_schema import (
    UtilizadorCreate,
    UtilizadorResponse
)
from app.auth.security import hash_password

router = APIRouter(
    prefix="/utilizadores",
    tags=["Utilizadores"]
)


# CREATE
@router.post("/", response_model=UtilizadorResponse)
def criar_utilizador(
    dados: UtilizadorCreate,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):

    existente = db.query(Utilizador).filter(
        Utilizador.email == dados.email
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Email já registado")

    novo = Utilizador(
        nome=dados.nome,
        email=dados.email,
        role=dados.role,
        password_hash=hash_password(dados.password)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# READ ALL
@router.get("/", response_model=List[UtilizadorResponse])
def listar_utilizadores(db: Session = Depends(get_db)):
    return db.query(Utilizador).all()


# ME (deve vir antes do /{user_id})
@router.get("/me", response_model=UtilizadorResponse)
def obter_me(current_user: Utilizador = Depends(get_current_user)):
    return current_user


# READ ONE
@router.get("/{user_id}", response_model=UtilizadorResponse)
def obter_utilizador(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Utilizador).filter(
        Utilizador.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    return user


# DELETE
@router.delete("/{user_id}")
def apagar_utilizador(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Utilizador).filter(
        Utilizador.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    db.delete(user)
    db.commit()

    return {"message": "Utilizador apagado com sucesso"}