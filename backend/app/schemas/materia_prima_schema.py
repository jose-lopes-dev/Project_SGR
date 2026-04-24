from pydantic import BaseModel


class MateriaPrimaBase(BaseModel):
    nome: str


class MateriaPrimaCreate(MateriaPrimaBase):
    pass


class MateriaPrimaResponse(MateriaPrimaBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True