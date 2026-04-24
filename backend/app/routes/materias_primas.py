from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.auth.dependencies import get_current_admin

from app.database import get_db
from app.models.materia_prima import MateriaPrima
from app.schemas.materia_prima_schema import (
    MateriaPrimaCreate,
    MateriaPrimaResponse
)

from app.models.utilizador import Utilizador

router = APIRouter(
    prefix="/materias-primas",
    tags=["Materias-Primas"]
)


# CREATE
@router.post("/", response_model=MateriaPrimaResponse)
def criar_materia_prima(
    materia: MateriaPrimaCreate,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):
    # Verificar se já existe
    existente = db.query(MateriaPrima).filter(
        MateriaPrima.nome == materia.nome
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Matéria-prima já existe")

    nova_materia = MateriaPrima(nome=materia.nome)

    db.add(nova_materia)
    db.commit()
    db.refresh(nova_materia)

    return nova_materia


# READ ALL
@router.get("/", response_model=List[MateriaPrimaResponse])
def listar_materias_primas(db: Session = Depends(get_db)):
    return db.query(MateriaPrima).all()


# READ ONE
@router.get("/{materia_id}", response_model=MateriaPrimaResponse)
def obter_materia_prima(materia_id: int, db: Session = Depends(get_db)):
    materia = db.query(MateriaPrima).filter(
        MateriaPrima.id == materia_id
    ).first()

    if not materia:
        raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")

    return materia


#  DELETE
@router.delete("/{materia_id}")
def apagar_materia_prima(
    materia_id: int, 
    db: Session = Depends(get_db), 
    admin: Utilizador = Depends(get_current_admin)):

    materia = db.query(MateriaPrima).filter(
        MateriaPrima.id == materia_id
    ).first()

    if not materia:
        raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")

    db.delete(materia)
    db.commit()

    return {"message": "Matéria-prima apagada com sucesso"}