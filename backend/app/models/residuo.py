from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Residuo(Base):
    __tablename__ = "residuos"

    id = Column(Integer, primary_key=True, index=True)

    local_id = Column(Integer, ForeignKey("localizacoes.id"), nullable=False)
    materia_prima_id = Column(Integer, ForeignKey("materias_primas.id"), nullable=False)
    tipo_residuo_id = Column(Integer, ForeignKey("tipos_residuos.id"), nullable=False)
    utilizador_id = Column(Integer, ForeignKey("utilizadores.id"), nullable=False)

    quantidade = Column(Numeric(12, 2), nullable=False)
    data = Column(Date, nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relações (ORM)
    local = relationship("Localizacao")
    materia_prima = relationship("MateriaPrima")
    tipo_residuo = relationship("TipoResiduo")
    utilizador = relationship("Utilizador")