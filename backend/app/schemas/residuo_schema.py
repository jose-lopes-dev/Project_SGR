from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.schemas.localizacao_schema import LocalizacaoResponse
from app.schemas.materia_prima_schema import MateriaPrimaResponse
from app.schemas.tipo_residuo_schema import TipoResiduoResponse
from app.schemas.utilizador_schema import UtilizadorResponse


class ResiduoBase(BaseModel):
    local_id: int
    materia_prima_id: int
    tipo_residuo_id: int
    quantidade: float
    data: date


class ResiduoCreate(ResiduoBase):
    pass

class ResiduoUpdate(ResiduoBase):
    pass

class ResiduoResponse(ResiduoBase):
    id: int
    utilizador_id: int

    local: Optional[LocalizacaoResponse] = None
    materia_prima: Optional[MateriaPrimaResponse] = None
    tipo_residuo: Optional[TipoResiduoResponse] = None
    utilizador: Optional[UtilizadorResponse] = None

    class Config:
        from_attributes = True