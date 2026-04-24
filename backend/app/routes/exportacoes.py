from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
import pandas as pd

from app.database import get_db
from app.models.residuo import Residuo
from app.models.destino_residuo import DestinoResiduo
from app.services.export_service import gerar_csv, gerar_pdf

router = APIRouter(prefix="/export", tags=["Exportações"])


def _parse_data(data_str: Optional[str], default: Optional[date] = None) -> Optional[date]:
    """Transforma string ISO em date ou retorna default"""
    if data_str:
        return datetime.fromisoformat(data_str).date()
    return default


# EXPORTAR RESÍDUOS
@router.get("/residuos")
def exportar_residuos(
    formato: str = Query("csv", pattern="^(csv|pdf)$"),
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    tipo_residuo_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    hoje = date.today()

    # Se não houver datas, usa o mês atual
    dt_inicio = _parse_data(data_inicio, default=hoje.replace(day=1))
    dt_fim = _parse_data(data_fim, default=hoje)

    query = db.query(Residuo).filter(Residuo.data >= dt_inicio, Residuo.data <= dt_fim)

    if tipo_residuo_id:
        query = query.filter(Residuo.tipo_residuo_id == tipo_residuo_id)

    resultados = query.all()

    dados = [
        {
            "ID": r.id,
            "Tipo Resíduo": r.tipo_residuo.nome if r.tipo_residuo else "",
            "Local": r.local.tipo_local if r.local else "",
            "Matéria Prima": r.materia_prima.nome if r.materia_prima else "",
            "Quantidade": r.quantidade,
            "Data": r.data.strftime("%Y-%m-%d")
        }
        for r in resultados
    ]
    df = pd.DataFrame(dados)
    return gerar_csv(df, "residuos.csv") if formato == "csv" else gerar_pdf(df, "residuos.pdf")


# EXPORTAR DESTINOS
@router.get("/destinos")
def exportar_destinos(
    formato: str = Query("csv", pattern="^(csv|pdf)$"),
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    db: Session = Depends(get_db)
):
    hoje = date.today()
    dt_inicio = _parse_data(data_inicio, default=hoje.replace(day=1))
    dt_fim = _parse_data(data_fim, default=hoje)

    query = db.query(DestinoResiduo).filter(DestinoResiduo.data >= dt_inicio, DestinoResiduo.data <= dt_fim)
    resultados = query.all()

    dados = [
        {
            "ID": d.id,
            "Resíduo": d.residuo.tipo_residuo.nome if d.residuo else "",
            "Destino": d.destino,
            "Quantidade": d.quantidade,
            "Receita": d.receita,
            "Data": d.data.strftime("%Y-%m-%d")
        }
        for d in resultados
    ]
    df = pd.DataFrame(dados)
    return gerar_csv(df, "destinos.csv") if formato == "csv" else gerar_pdf(df, "destinos.pdf")