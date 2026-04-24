from pydantic import BaseModel, EmailStr
from datetime import datetime


class UtilizadorBase(BaseModel):
    nome: str
    email: EmailStr
    role: str


class UtilizadorCreate(UtilizadorBase):
    password: str


class UtilizadorResponse(UtilizadorBase):
    id: int
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True