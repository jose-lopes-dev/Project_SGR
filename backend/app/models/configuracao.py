from sqlalchemy import Column, Integer, String, Numeric, Text
from app.database import Base


class Configuracao(Base):
    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String(100), unique=True, nullable=False)
    valor = Column(Numeric(12, 4))
    descricao = Column(Text)