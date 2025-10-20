from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from .database import Base, engine, get_session
from .models import SiteConfig, Ministerio, Evento, Mensagem

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IBINOVIRP Site (Python)")

# Templates
templates_env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

# Static (optional placeholder)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with get_session() as db:
        site = db.execute(select(SiteConfig).limit(1)).scalar_one_or_none()
        eventos = db.execute(select(Evento).order_by(Evento.inicio.asc()).limit(5)).scalars().all()
        ministerios = db.execute(select(Ministerio).order_by(Ministerio.updated_at.desc()).limit(5)).scalars().all()
        mensagens = db.execute(select(Mensagem).order_by(Mensagem.data.desc().nullslast()).limit(5)).scalars().all()

    template = templates_env.get_template("index.html")
    return template.render(site=site, eventos=eventos, ministerios=ministerios, mensagens=mensagens)


@app.get("/config", response_class=HTMLResponse)
async def config_get(request: Request):
    with get_session() as db:
        site = db.execute(select(SiteConfig).limit(1)).scalar_one_or_none()
    template = templates_env.get_template("config.html")
    return template.render(site=site)


@app.post("/config")
async def config_post(
    nomeIgreja: str = Form(""),
    descricaoBreve: str = Form("")
):
    with get_session() as db:
        site = db.execute(select(SiteConfig).limit(1)).scalar_one_or_none()
        if site is None:
            site = SiteConfig(nome_igreja=nomeIgreja, descricao_breve=descricaoBreve)
            db.add(site)
        else:
            site.nome_igreja = nomeIgreja
            site.descricao_breve = descricaoBreve
        db.commit()
    return RedirectResponse(url="/config", status_code=status.HTTP_302_FOUND)
