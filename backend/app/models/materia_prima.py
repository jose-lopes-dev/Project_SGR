from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class MateriaPrima(Base):
    __tablename__ = "materias_primas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True) # mármore | granito | calcário
    ativo = Column(Boolean, default=True)