from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.localizacao import Localizacao
from app.schemas.localizacao_schema import (
    LocalizacaoCreate,
    LocalizacaoResponse
)

router = APIRouter(
    prefix="/localizacoes",
    tags=["Localizacoes"]
)


@router.post("/", response_model=LocalizacaoResponse)
def criar_localizacao(local: LocalizacaoCreate, db: Session = Depends(get_db)):
    nova = Localizacao(
        tipo_local=local.tipo_local
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


@router.get("/", response_model=List[LocalizacaoResponse])
def listar_localizacoes(db: Session = Depends(get_db)):
    return db.query(Localizacao).all()


@router.get("/{local_id}", response_model=LocalizacaoResponse)
def obter_localizacao(local_id: int, db: Session = Depends(get_db)):
    local = db.query(Localizacao).filter(Localizacao.id == local_id).first()

    if not local:
        raise HTTPException(status_code=404, detail="Localização não encontrada")

    return local


@router.delete("/{local_id}")
def apagar_localizacao(local_id: int, db: Session = Depends(get_db)):
    local = db.query(Localizacao).filter(Localizacao.id == local_id).first()

    if not local:
        raise HTTPException(status_code=404, detail="Localização não encontrada")

    db.delete(local)
    db.commit()

    return {"message": "Localização apagada com sucesso"}