from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from fastapi import Query
from sqlalchemy import extract
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.residuo import Residuo
from app.models.destino_residuo import DestinoResiduo
from app.models.localizacao import Localizacao
from app.models.tipo_residuo import TipoResiduo
from app.auth.dependencies import get_current_admin
from app.models.utilizador import Utilizador
from app.analytics.previsao import prever_receita
from app.schemas.residuo_schema import ResiduoResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

def _add_months(d: date, months: int) -> date:
    month0 = (d.month - 1) + months
    year = d.year + (month0 // 12)
    month = (month0 % 12) + 1
    return date(year, month, 1)


def _month_start(ano: int, mes: int) -> date:
    return date(ano, mes, 1)


def _month_end(d: date) -> date:
    return _add_months(d, 1) - timedelta(days=1)


def _ultimos_3_meses(ref_ano: int = 2026, ref_mes: int = 3):
    ref = _month_start(ref_ano, ref_mes)
    meses = [_add_months(ref, -2), _add_months(ref, -1), ref]
    janelas = []
    for m in meses:
        janelas.append(
            {
                "inicio": m,
                "fim": _month_end(m),
                "label": f"{m.year:04d}-{m.month:02d}",
            }
        )
    return janelas


@router.get("/kpis")
def obter_kpis(
    data_inicio: date | None = Query(None),
    data_fim: date | None = Query(None),
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):
    
    query_residuos = db.query(Residuo)
    query_destinos = db.query(DestinoResiduo)

    if data_inicio:
        query_residuos = query_residuos.filter(Residuo.data >= data_inicio)
        query_destinos = query_destinos.filter(DestinoResiduo.data >= data_inicio)

    if data_fim:
        query_residuos = query_residuos.filter(Residuo.data <= data_fim)
        query_destinos = query_destinos.filter(DestinoResiduo.data <= data_fim)

    total_residuos = query_residuos.with_entities(
    func.sum(Residuo.quantidade)
).scalar() or 0

    receita_total = query_destinos.with_entities(
    func.sum(DestinoResiduo.receita)
).scalar() or 0

    reutilizado = query_destinos.filter(
    DestinoResiduo.destino != "aterro"
).with_entities(
    func.sum(DestinoResiduo.quantidade)
).scalar() or 0

    aterro = query_destinos.filter(
    DestinoResiduo.destino == "aterro"
).with_entities(
    func.sum(DestinoResiduo.quantidade)
).scalar() or 0

    percentagem_reutilizacao = 0
    if total_residuos > 0:
        percentagem_reutilizacao = round((reutilizado / total_residuos) * 100, 2)

    return {
        "total_residuos": total_residuos,
        "receita_total": receita_total,
        "total_reutilizado": reutilizado,
        "total_aterro": aterro,
        "percentagem_reutilizacao": percentagem_reutilizacao
    }

@router.get("/receita-mensal")
def receita_mensal(
    ano: int,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):

    resultados = db.query(
        extract("month", DestinoResiduo.data).label("mes"),
        func.sum(DestinoResiduo.receita)
    ).filter(
        extract("year", DestinoResiduo.data) == ano
    ).group_by("mes").all()

    return [
        {"mes": int(mes), "receita": float(receita or 0)}
        for mes, receita in resultados
    ]


@router.get("/receita-ultimos-3-meses")
def receita_ultimos_3_meses(
    ref_ano: int = 2026,
    ref_mes: int = 3,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin),
):
    janelas = _ultimos_3_meses(ref_ano, ref_mes)
    inicio = janelas[0]["inicio"]
    fim = janelas[-1]["fim"]

    resultados = (
        db.query(
            func.date_trunc("month", DestinoResiduo.data).label("mes"),
            func.sum(DestinoResiduo.receita).label("receita"),
        )
        .filter(DestinoResiduo.data >= inicio, DestinoResiduo.data <= fim)
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    por_mes = {}
    for mes_dt, receita in resultados:
        # mes_dt é datetime (date_trunc)
        label = f"{mes_dt.year:04d}-{mes_dt.month:02d}"
        por_mes[label] = float(receita or 0)

    return [
        {"mes": j["label"], "receita": por_mes.get(j["label"], 0.0)}
        for j in janelas
    ]

@router.get("/resumo")
def dashboard_resumo(
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):
    total_residuos = db.query(func.sum(Residuo.quantidade)).scalar() or 0
    receita_total = db.query(func.sum(DestinoResiduo.receita)).scalar() or 0

    reutilizado = db.query(func.sum(DestinoResiduo.quantidade))\
        .filter(DestinoResiduo.destino != "aterro")\
        .scalar() or 0

    aterro = db.query(func.sum(DestinoResiduo.quantidade))\
        .filter(DestinoResiduo.destino == "aterro")\
        .scalar() or 0

    percentagem = 0
    if total_residuos > 0:
        percentagem = round((reutilizado / total_residuos) * 100, 2)

    return {
        "total_residuos": total_residuos,
        "receita_total": receita_total,
        "reutilizado": reutilizado,
        "aterro": aterro,
        "percentagem_reutilizacao": percentagem
    }

@router.get("/financeiro")
def dashboard_financeiro(
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):

    resultados = (
        db.query(
            TipoResiduo.nome,
            func.sum(DestinoResiduo.receita),
        )
        .join(Residuo, Residuo.tipo_residuo_id == TipoResiduo.id)
        .join(DestinoResiduo, DestinoResiduo.residuo_id == Residuo.id)
        .group_by(TipoResiduo.nome)
        .all()
    )

    return [
        {"tipo_residuo": nome, "receita": float(receita or 0)}
        for nome, receita in resultados
    ]


@router.get("/financeiro-ultimos-3-meses")
def dashboard_financeiro_ultimos_3_meses(
    ref_ano: int = 2026,
    ref_mes: int = 3,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin),
):
    janelas = _ultimos_3_meses(ref_ano, ref_mes)
    inicio = janelas[0]["inicio"]
    fim = janelas[-1]["fim"]

    resultados = (
        db.query(
            func.date_trunc("month", DestinoResiduo.data).label("mes"),
            func.sum(DestinoResiduo.receita).label("receita"),
        )
        .filter(DestinoResiduo.data >= inicio, DestinoResiduo.data <= fim)
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    por_mes = {}
    for mes_dt, receita in resultados:
        label = f"{mes_dt.year:04d}-{mes_dt.month:02d}"
        por_mes[label] = float(receita or 0)

    return [
        {"mes": j["label"], "receita": por_mes.get(j["label"], 0.0)}
        for j in janelas
    ]

@router.get("/operacional")
def dashboard_operacional(
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):

    resultados = (
        db.query(
            Localizacao.tipo_local,
            func.sum(Residuo.quantidade),
        )
        .join(Localizacao, Localizacao.id == Residuo.local_id)
        .group_by(Localizacao.tipo_local)
        .all()
    )

    return [
        {
            "localizacao": loc,
            "quantidade": float(qtd or 0)
        }
        for loc, qtd in resultados
    ]


@router.get("/operacional-ultimos-3-meses")
def dashboard_operacional_ultimos_3_meses(
    ref_ano: int = 2026,
    ref_mes: int = 3,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin),
):
    janelas = _ultimos_3_meses(ref_ano, ref_mes)
    inicio = janelas[0]["inicio"]
    fim = janelas[-1]["fim"]

    agreg = (
        db.query(
            func.date_trunc("month", Residuo.data).label("mes"),
            func.sum(Residuo.quantidade).label("quantidade"),
        )
        .filter(Residuo.data >= inicio, Residuo.data <= fim)
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    por_mes = {}
    for mes_dt, quantidade in agreg:
        label = f"{mes_dt.year:04d}-{mes_dt.month:02d}"
        por_mes[label] = float(quantidade or 0)

    registos = (
        db.query(Residuo)
        .options(
            joinedload(Residuo.local),
            joinedload(Residuo.materia_prima),
            joinedload(Residuo.tipo_residuo),
            joinedload(Residuo.utilizador),
        )
        .filter(Residuo.data >= inicio, Residuo.data <= fim)
        .order_by(Residuo.data.desc(), Residuo.id.desc())
        .all()
    )

    return {
        "series": [
            {"mes": j["label"], "quantidade": por_mes.get(j["label"], 0.0)}
            for j in janelas
        ],
        "registos": [
            ResiduoResponse.model_validate(r).model_dump()
            for r in registos
        ],
    }

@router.get("/ambiental")
def dashboard_ambiental(
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):

    reutilizado = db.query(func.sum(DestinoResiduo.quantidade))\
        .filter(DestinoResiduo.destino != "aterro")\
        .scalar() or 0

    co2_evitar = reutilizado * Decimal("0.5")

    return {
        "quantidade_reutilizada": reutilizado,
        "co2_evitar_estimado": round(co2_evitar, 2)
    }


@router.get("/ambiental-ultimos-3-meses")
def dashboard_ambiental_ultimos_3_meses(
    ref_ano: int = 2026,
    ref_mes: int = 3,
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin),
):
    janelas = _ultimos_3_meses(ref_ano, ref_mes)
    inicio = janelas[0]["inicio"]
    fim = janelas[-1]["fim"]

    reutilizado_mes = (
        db.query(
            func.date_trunc("month", DestinoResiduo.data).label("mes"),
            func.sum(DestinoResiduo.quantidade).label("reutilizado"),
        )
        .filter(
            DestinoResiduo.data >= inicio,
            DestinoResiduo.data <= fim,
            DestinoResiduo.destino != "aterro",
        )
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    por_mes = {}
    for mes_dt, qtd in reutilizado_mes:
        label = f"{mes_dt.year:04d}-{mes_dt.month:02d}"
        por_mes[label] = float(qtd or 0)

    series = []
    for j in janelas:
        qtd = Decimal(str(por_mes.get(j["label"], 0.0)))
        co2 = qtd * Decimal("0.5")
        series.append(
            {
                "mes": j["label"],
                "reutilizado": float(qtd),
                "co2_evitar_estimado": float(round(co2, 2)),
            }
        )

    return {"series": series}

@router.get("/previsao-receita")
def previsao_receita(
    db: Session = Depends(get_db),
    admin: Utilizador = Depends(get_current_admin)
):

    resultados = (
        db.query(
            func.date_trunc("month", DestinoResiduo.data).label("mes"),
            func.sum(DestinoResiduo.receita).label("receita"),
        )
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    meses_historico = [f"{r[0].year:04d}-{r[0].month:02d}" for r in resultados]
    receitas_historico = [float(r[1] or 0) for r in resultados]

    if len(receitas_historico) < 3:
        return {"erro": "Dados insuficientes para previsão"}

    previsao = prever_receita(receitas_historico)

    # meses futuros (próximos 3 meses após o último mês histórico)
    ultimo_mes = date(int(meses_historico[-1].split("-")[0]), int(meses_historico[-1].split("-")[1]), 1)
    meses_previsao = [
        f"{_add_months(ultimo_mes, i).year:04d}-{_add_months(ultimo_mes, i).month:02d}"
        for i in (1, 2, 3)
    ]

    return {
        "meses_historico": meses_historico,
        "historico": receitas_historico,
        "meses_previsao": meses_previsao,
        "previsao_proximos_meses": previsao,
    }