from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.residuo import Residuo
from app.schemas.residuo_schema import (
    ResiduoCreate,
    ResiduoResponse
)

from app.models.utilizador import Utilizador

from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/residuos",
    tags=["Residuos"]
)

# CREATE
@router.post("/", response_model=ResiduoResponse)
def criar_residuo(
    residuo: ResiduoCreate,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):

    novo = Residuo(
        local_id=residuo.local_id,
        materia_prima_id=residuo.materia_prima_id,
        tipo_residuo_id=residuo.tipo_residuo_id,
        utilizador_id=user.id,
        quantidade=residuo.quantidade,
        data=residuo.data
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

# READ ALL
@router.get("/", response_model=List[ResiduoResponse])
def listar_residuos(
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):
    return (
        db.query(Residuo)
        .options(
            joinedload(Residuo.local),
            joinedload(Residuo.materia_prima),
            joinedload(Residuo.tipo_residuo),
            joinedload(Residuo.utilizador),
        )
        .all()
    )

# READ ONE
@router.get("/{residuo_id}", response_model=ResiduoResponse)
def obter_residuo(
    residuo_id: int,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):
    residuo = (
        db.query(Residuo)
        .options(
            joinedload(Residuo.local),
            joinedload(Residuo.materia_prima),
            joinedload(Residuo.tipo_residuo),
            joinedload(Residuo.utilizador),
        )
        .filter(Residuo.id == residuo_id)
        .first()
    )

    if not residuo:
        raise HTTPException(status_code=404, detail="Resíduo não encontrado")

    return residuo

# UPDATE
@router.put("/{residuo_id}", response_model=ResiduoResponse)
def atualizar_residuo(
    residuo_id: int,
    dados: ResiduoCreate,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):

    residuo = db.query(Residuo).filter(
        Residuo.id == residuo_id
    ).first()

    if not residuo:
        raise HTTPException(status_code=404, detail="Resíduo não encontrado")

    residuo.local_id = dados.local_id
    residuo.materia_prima_id = dados.materia_prima_id
    residuo.tipo_residuo_id = dados.tipo_residuo_id
    residuo.quantidade = dados.quantidade
    residuo.data = dados.data

    db.commit()
    db.refresh(residuo)

    return residuo

# DELETE
@router.delete("/{residuo_id}")
def apagar_residuo(
    residuo_id: int,
    db: Session = Depends(get_db),
    user: Utilizador = Depends(get_current_user)
):
    residuo = db.query(Residuo).filter(
        Residuo.id == residuo_id
    ).first()

    if not residuo:
        raise HTTPException(status_code=404, detail="Resíduo não encontrado")

    db.delete(residuo)
    db.commit()

    return {"message": "Resíduo apagado com sucesso"}
 
 