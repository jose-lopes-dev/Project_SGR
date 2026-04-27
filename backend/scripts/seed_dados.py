from sqlalchemy.orm import Session
from datetime import date, timedelta
import random

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.residuo import Residuo
from app.models.destino_residuo import DestinoResiduo
from app.models.utilizador import Utilizador

db: Session = SessionLocal()

materias = [1,2,3]
tipos = [1,2,3,4]
locais = [1,2,3,4]

# buscar utilizadores automaticamente
utilizadores = [u.id for u in db.query(Utilizador).all()]

destinos = [
    "reutilizacao",
    "reciclagem",
    "aterro"
]

data_inicio = date(2025,1,1)

for i in range(300):

    data = data_inicio + timedelta(days=random.randint(0,450))

    quantidade = random.randint(10,200)

    residuo = Residuo(
        local_id=random.choice(locais),
        materia_prima_id=random.choice(materias),
        tipo_residuo_id=random.choice(tipos),
        utilizador_id=random.choice(utilizadores),
        quantidade=quantidade,
        data=data
    )

    db.add(residuo)
    db.commit()
    db.refresh(residuo)

    destino = random.choice(destinos)

    receita = 0

    if destino != "aterro":
        receita = quantidade * random.randint(10,40)

    destino_residuo = DestinoResiduo(
        residuo_id=residuo.id,
        destino=destino,
        quantidade=quantidade,
        receita=receita,
        data=data
    )

    db.add(destino_residuo)
    db.commit()

print("✔ Dados gerados com sucesso!")