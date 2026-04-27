from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DestinoResiduo(Base):
    __tablename__ = "destinos_residuos"

    id = Column(Integer, primary_key=True, index=True)

    residuo_id = Column(Integer, ForeignKey("residuos.id", ondelete="CASCADE"), nullable=False)

    destino = Column(String(50), nullable=False)  # reutilizacao | reciclagem | reabilitacao | aterro
    quantidade = Column(Numeric(12, 2), nullable=False)
    receita = Column(Numeric(14, 2), default=0)

    data = Column(Date, nullable=False)
    observacoes = Column(Text)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relação
    residuo = relationship("Residuo")