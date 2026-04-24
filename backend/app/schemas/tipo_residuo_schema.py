from pydantic import BaseModel
from typing import Optional


class TipoResiduoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class TipoResiduoCreate(TipoResiduoBase):
    pass


class TipoResiduoResponse(TipoResiduoBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True