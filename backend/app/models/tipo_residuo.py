from sqlalchemy import Column, Integer, String, Boolean, Text
from app.database import Base


class TipoResiduo(Base):
    __tablename__ = "tipos_residuos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True) # bloco | pó | lama | lasca
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)