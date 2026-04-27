from pydantic import BaseModel


class LocalizacaoBase(BaseModel):
    tipo_local: str


class LocalizacaoCreate(LocalizacaoBase):
    pass


class LocalizacaoResponse(LocalizacaoBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True