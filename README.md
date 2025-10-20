## IBINOVIRP Site — FastAPI + PostgreSQL (Render)

Projeto web em Python com FastAPI, HTML (Jinja2) e PostgreSQL. Inclui área administrativa simples (CRUDs) protegida por Basic Auth e migrações com Alembic.

### Estrutura

- `app/main.py`: rotas públicas e administrativas
- `app/models.py`: modelos SQLAlchemy
- `app/database.py`: conexão com `DATABASE_URL`
- `app/auth.py`: Basic Auth (`ADMIN_USER`/`ADMIN_PASS`)
- `app/templates/`: templates Jinja2 (públicos e admin)
- `alembic/`: configuração do Alembic e migrations
- `render.yaml`: blueprint para Render (Python)
- `requirements.txt`: dependências do projeto

### Variáveis de ambiente
- `DATABASE_URL`: string de conexão PostgreSQL
- `ADMIN_USER`: usuário do painel admin
- `ADMIN_PASS`: senha do painel admin

Exemplo local (PowerShell):
```powershell
setx DATABASE_URL "postgresql://postgres:postgres@localhost:5432/ibinovirp"
setx ADMIN_USER "admin"
setx ADMIN_PASS "senha"
# reinicie o terminal após setx
```

### Setup local
```bash
python -m venv .venv
# Windows (PowerShell)
. .venv/Scripts/activate
pip install -r requirements.txt

# Primeiro aplique as migrations (após configurar DATABASE_URL):
alembic upgrade head

# Rodar o servidor
uvicorn app.main:app --reload
```
Acesse:
- Home: http://localhost:8000/
- Admin: http://localhost:8000/admin/ministerios | /admin/eventos | /admin/mensagens
- Config: http://localhost:8000/config

### Alembic (Migrações)
Gerar uma nova migration após alterar `app/models.py`:
```bash
alembic revision --autogenerate -m "description"
```
Aplicar migrations:
```bash
alembic upgrade head
```

### Deploy na Render
- Este repo está pronto para Web Service Python via `render.yaml`:
  - `runtime: python`
  - `buildCommand: pip install -r requirements.txt`
  - `startCommand: alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Configure as envs no serviço:
  - `DATABASE_URL` (da instância PostgreSQL Render)
  - `ADMIN_USER`
  - `ADMIN_PASS`
- O deploy aplicará migrations automaticamente no start.

### Rotas Principais
- Público:
  - `GET /` — Home com destaques
- Admin (Basic Auth):
  - Ministérios: `GET /admin/ministerios`, `GET/POST /admin/ministerios/novo`, `GET/POST /admin/ministerios/editar/{id}`, `POST /admin/ministerios/excluir/{id}`
  - Eventos: `GET /admin/eventos`, `GET/POST /admin/eventos/novo`, `GET/POST /admin/eventos/editar/{id}`, `POST /admin/eventos/excluir/{id}`
  - Mensagens: `GET /admin/mensagens`, `GET/POST /admin/mensagens/novo`, `GET/POST /admin/mensagens/editar/{id}`, `POST /admin/mensagens/excluir/{id}`
  - Configuração do Site: `GET/POST /config`

### Notas
- Layout base em `app/templates/base.html`.
- Para uploads e mídias, integrar serviço de storage (ex.: S3) e criar endpoints apropriados.
