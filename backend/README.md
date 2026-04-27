# API Gestão de Resíduos (FastAPI + PostgreSQL)

API para registar residuos produzidos pelas empresas de extração de marmóre

**Instalar dependências**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

**Executar a API**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Documentação: http://localhost:8000/docs

## Endpoints

- `GET /tipos-residuos` — Listar todos os tipos de resíduos
- `POST /residuos` — Criar residuo (nome_empresa, tipo_id, quantidade)
- `GET /residuos` — Listar todos
- `GET /residuos/stats` — Apresentar grafico para analise do total de residuos por tipo
- `GET /residuos/{id}` — Obter um residuo
- `PUT /residuos/{id}` — Atualizar (nome_empresa, tipo_id, quantidade)
- `DELETE /residuos/{id}` — Eliminar