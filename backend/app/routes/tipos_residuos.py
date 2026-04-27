from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.tipo_residuo import TipoResiduo
from app.schemas.tipo_residuo_schema import (
    TipoResiduoCreate,
    TipoResiduoResponse
)

router = APIRouter(
    prefix="/tipos-residuos",
    tags=["Tipos-Residuos"]
)


@router.post("/", response_model=TipoResiduoResponse)
def criar_tipo(tipo: TipoResiduoCreate, db: Session = Depends(get_db)):
    existente = db.query(TipoResiduo).filter(
        TipoResiduo.nome == tipo.nome
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Tipo já existe")

    novo = TipoResiduo(
        nome=tipo.nome,
        descricao=tipo.descricao
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@router.get("/", response_model=List[TipoResiduoResponse])
def listar_tipos(db: Session = Depends(get_db)):
    return db.query(TipoResiduo).all()


@router.delete("/{tipo_id}")
def apagar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    tipo = db.query(TipoResiduo).filter(
        TipoResiduo.id == tipo_id
    ).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo não encontrado")

    db.delete(tipo)
    db.commit()

    return {"message": "Tipo apagado com sucesso"}