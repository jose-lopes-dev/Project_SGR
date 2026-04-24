from fastapi import FastAPI
from app.database import engine, Base
import app.models
from app.routes import materias_primas
from app.routes import tipos_residuos
from app.routes import localizacoes
from app.routes import residuos
from app.routes import utilizadores
from app.routes import auth
from app.routes import destinos_residuos
from app.routes import dashboard
from app.routes import exportacoes

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(localizacoes.router)
app.include_router(tipos_residuos.router)
app.include_router(materias_primas.router)
app.include_router(residuos.router)
app.include_router(utilizadores.router)
app.include_router(auth.router)
app.include_router(destinos_residuos.router)
app.include_router(dashboard.router)
app.include_router(exportacoes.router)

@app.get("/")
def read_root():
    return {"message": "Stone ESG API is running"}