from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.destino_residuo import DestinoResiduo
from app.models.residuo import Residuo
from app.schemas.destino_residuo_schema import (
    DestinoResiduoCreate,
    DestinoResiduoResponse
)
from app.auth.dependencies import get_current_user
from app.models.utilizador import Utilizador

router = APIRouter(
    prefix="/destinos-residuos",
    tags=["Destinos-Residuos"]
)


# CREATE
@router.post("/", response_model=DestinoResiduoResponse)
def criar_destino(
    dados: DestinoResiduoCreate,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):

    novo = DestinoResiduo(
        residuo_id=dados.residuo_id,
        destino=dados.destino,
        quantidade=dados.quantidade,
        receita=dados.receita,
        data=dados.data,
        observacoes=dados.observacoes
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# READ ALL
@router.get("/", response_model=List[DestinoResiduoResponse])
def listar_destinos(
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):
    return (
        db.query(DestinoResiduo)
        .options(
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.local),
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.materia_prima),
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.tipo_residuo),
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.utilizador),
        )
        .all()
    )

# READ ONE
@router.get("/{destino_id}", response_model=DestinoResiduoResponse)
def obter_destino(
    destino_id: int,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):

    destino = (
        db.query(DestinoResiduo)
        .options(
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.local),
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.materia_prima),
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.tipo_residuo),
            joinedload(DestinoResiduo.residuo).joinedload(Residuo.utilizador),
        )
        .filter(DestinoResiduo.id == destino_id)
        .first()
    )

    if not destino:
        raise HTTPException(status_code=404, detail="Destino não encontrado")

    return destino

# UPDATE
@router.put("/{destino_id}", response_model=DestinoResiduoResponse)
def atualizar_destino(
    destino_id: int,
    dados: DestinoResiduoCreate,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):

    destino = db.query(DestinoResiduo).filter(
        DestinoResiduo.id == destino_id
    ).first()

    if not destino:
        raise HTTPException(status_code=404, detail="Destino não encontrado")

    destino.residuo_id = dados.residuo_id
    destino.destino = dados.destino
    destino.quantidade = dados.quantidade
    destino.receita = dados.receita
    destino.data = dados.data
    destino.observacoes = dados.observacoes

    db.commit()
    db.refresh(destino)

    return destino

# DELETE
@router.delete("/{destino_id}")
def apagar_destino(
    destino_id: int,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):

    destino = db.query(DestinoResiduo).filter(
        DestinoResiduo.id == destino_id
    ).first()

    if not destino:
        raise HTTPException(status_code=404, detail="Destino não encontrado")

    db.delete(destino)
    db.commit()

    return {"message": "Destino apagado com sucesso"}