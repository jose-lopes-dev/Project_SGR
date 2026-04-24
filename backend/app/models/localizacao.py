from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Localizacao(Base):

    __tablename__ = "localizacoes"

    id = Column(Integer, primary_key=True, index=True)

    tipo_local = Column(
        String(50),
        nullable=False
    )  # pedreira | fabrica | armazem | loja

    ativo = Column(Boolean, default=True)