# Project SGR

Projeto de gestão integrada com frontend Nuxt e backend Python. O sistema contempla registro e visualização de resíduos, gestão de usuários, dashboards, exportação de dados e previsão de receita.

## Estrutura do projeto

- `frontend/` → aplicação Nuxt 4 com Vue 3 e Tailwind CSS
- `backend/` → API Python com FastAPI e PostgreSQL

## Descrição

O backend fornece endpoints para:
- autenticação de usuários
- cadastro e consulta de resíduos, tipos de resíduos, matérias-primas, localizações e destinos
- dashboard e exportação de relatórios
- previsão de receitas

O frontend consome a API e exibe:
- painel administrativo
- rotas para funcionários
- gráficos e tabelas
- formulários de login e cadastro
- integração com exportação de PDFs

## Tecnologias

### Frontend
- Nuxt 4
- Vue 3
- Tailwind CSS
- Chart.js
- Vue Chart.js
- Sweetalert2
- jsPDF / jspdf-autotable
- html2canvas
- Vue Router

### Backend
- Python 3.14+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- PostgreSQL
- python-dotenv
- psycopg2-binary
- passlib
- python-multipart
- pandas / numpy / scikit-learn / scipy / seaborn / matplotlib

## Dependências do backend

O backend lista suas dependências em `backend/requirements.txt`. Exemplo:

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- python-dotenv
- pydantic
- passlib
- python-multipart
- pandas
- numpy
- scikit-learn
- scipy
- seaborn
- matplotlib

## Pré-requisitos

- Node.js e npm
- Python 3.14+
- PostgreSQL instalado e configurado
- Conexão de banco definida em `backend/.env`

## Configuração de ambiente

Crie o arquivo `backend/.env` com a URL de conexão do PostgreSQL:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/name_database
```

## Como executar

### Frontend

```bash
cd frontend
npm install
npm run dev
```

A aplicação Nuxt deve ficar disponível em `http://localhost:3000`.

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend deve ficar disponível em `http://localhost:8000`.

## Observações

- Se `frontend` ainda estiver sendo tratado como repositório separado, remova `frontend/.git` para que o diretório seja versionado no repositório pai.
- Se o backend não iniciar, confirme a existência de `backend/app/main.py` e o `DATABASE_URL` em `backend/.env`.
