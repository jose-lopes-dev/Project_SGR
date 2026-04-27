from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.schemas.residuo_schema import ResiduoResponse


class DestinoResiduoBase(BaseModel):
    residuo_id: int
    destino: str
    quantidade: float
    receita: float
    data: date
    observacoes: Optional[str] = None


class DestinoResiduoCreate(DestinoResiduoBase):
    pass


class DestinoResiduoResponse(DestinoResiduoBase):
    id: int
    residuo: Optional[ResiduoResponse] = None

    class Config:
        from_attributes = True