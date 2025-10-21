from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from .database import Base, engine, get_session
from .models import SiteConfig, Ministerio, Evento, Mensagem
from .auth import require_basic_auth

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Igreja Batista Independente Nova Vida - Rio Pardo - RS")

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
async def config_get(request: Request, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        site = db.execute(select(SiteConfig).limit(1)).scalar_one_or_none()
    template = templates_env.get_template("config.html")
    return template.render(site=site)


@app.post("/config")
async def config_post(
    nomeIgreja: str = Form(""),
    descricaoBreve: str = Form(""),
    _: bool = Depends(require_basic_auth),
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


# ---------------------- ADMIN CRUDS (basic) ----------------------

# Ministerio CRUD
@app.get("/admin/ministerios", response_class=HTMLResponse)
async def admin_ministerios_list(_: bool = Depends(require_basic_auth)):
    with get_session() as db:
        items = db.execute(select(Ministerio).order_by(Ministerio.updated_at.desc())).scalars().all()
    t = templates_env.get_template("admin_ministerios.html")
    return t.render(items=items)

@app.get("/admin/ministerios/novo", response_class=HTMLResponse)
async def admin_ministerios_new(_: bool = Depends(require_basic_auth)):
    t = templates_env.get_template("admin_ministerios_form.html")
    return t.render(item=None)

@app.post("/admin/ministerios/novo")
async def admin_ministerios_create(
    titulo: str = Form(""),
    descricao: str = Form(""),
    imagem: str = Form(""),
    _: bool = require_basic_auth,
):
    with get_session() as db:
        m = Ministerio(titulo=titulo, descricao=descricao or None, imagem=imagem or None)
        db.add(m)
        db.commit()
    return RedirectResponse(url="/admin/ministerios", status_code=status.HTTP_302_FOUND)

@app.get("/admin/ministerios/editar/{id}", response_class=HTMLResponse)
async def admin_ministerios_edit(id: int, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        item = db.get(Ministerio, id)
    t = templates_env.get_template("admin_ministerios_form.html")
    return t.render(item=item)

@app.post("/admin/ministerios/editar/{id}")
async def admin_ministerios_update(
    id: int,
    titulo: str = Form(""),
    descricao: str = Form(""),
    imagem: str = Form(""),
    _: bool = require_basic_auth,
):
    with get_session() as db:
        item = db.get(Ministerio, id)
        if item:
            item.titulo = titulo
            item.descricao = descricao or None
            item.imagem = imagem or None
            db.commit()
    return RedirectResponse(url="/admin/ministerios", status_code=status.HTTP_302_FOUND)

@app.post("/admin/ministerios/excluir/{id}")
async def admin_ministerios_delete(id: int, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        item = db.get(Ministerio, id)
        if item:
            db.delete(item)
            db.commit()
    return RedirectResponse(url="/admin/ministerios", status_code=status.HTTP_302_FOUND)


# Evento CRUD
@app.get("/admin/eventos", response_class=HTMLResponse)
async def admin_eventos_list(_: bool = Depends(require_basic_auth)):
    with get_session() as db:
        items = db.execute(select(Evento).order_by(Evento.inicio.asc())).scalars().all()
    t = templates_env.get_template("admin_eventos.html")
    return t.render(items=items)

@app.get("/admin/eventos/novo", response_class=HTMLResponse)
async def admin_eventos_new(_: bool = Depends(require_basic_auth)):
    t = templates_env.get_template("admin_eventos_form.html")
    return t.render(item=None)

@app.post("/admin/eventos/novo")
async def admin_eventos_create(
    titulo: str = Form(""),
    descricao: str = Form(""),
    local: str = Form(""),
    inicio: str = Form(""),
    fim: str = Form(""),
    _: bool = require_basic_auth,
):
    with get_session() as db:
        e = Evento(titulo=titulo, descricao=descricao or None, local=local or None, inicio=inicio or None, fim=fim or None)
        db.add(e)
        db.commit()
    return RedirectResponse(url="/admin/eventos", status_code=status.HTTP_302_FOUND)

@app.get("/admin/eventos/editar/{id}", response_class=HTMLResponse)
async def admin_eventos_edit(id: int, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        item = db.get(Evento, id)
    t = templates_env.get_template("admin_eventos_form.html")
    return t.render(item=item)

@app.post("/admin/eventos/editar/{id}")
async def admin_eventos_update(
    id: int,
    titulo: str = Form(""),
    descricao: str = Form(""),
    local: str = Form(""),
    inicio: str = Form(""),
    fim: str = Form(""),
    _: bool = require_basic_auth,
):
    with get_session() as db:
        item = db.get(Evento, id)
        if item:
            item.titulo = titulo
            item.descricao = descricao or None
            item.local = local or None
            item.inicio = inicio or None
            item.fim = fim or None
            db.commit()
    return RedirectResponse(url="/admin/eventos", status_code=status.HTTP_302_FOUND)

@app.post("/admin/eventos/excluir/{id}")
async def admin_eventos_delete(id: int, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        item = db.get(Evento, id)
        if item:
            db.delete(item)
            db.commit()
    return RedirectResponse(url="/admin/eventos", status_code=status.HTTP_302_FOUND)


# Mensagem CRUD
@app.get("/admin/mensagens", response_class=HTMLResponse)
async def admin_mensagens_list(_: bool = Depends(require_basic_auth)):
    with get_session() as db:
        items = db.execute(select(Mensagem).order_by(Mensagem.data.desc().nullslast())).scalars().all()
    t = templates_env.get_template("admin_mensagens.html")
    return t.render(items=items)

@app.get("/admin/mensagens/novo", response_class=HTMLResponse)
async def admin_mensagens_new(_: bool = Depends(require_basic_auth)):
    t = templates_env.get_template("admin_mensagens_form.html")
    return t.render(item=None)

@app.post("/admin/mensagens/novo")
async def admin_mensagens_create(
    titulo: str = Form(""),
    pregador: str = Form(""),
    data: str = Form(""),
    video_url: str = Form(""),
    audio_url: str = Form(""),
    capa_url: str = Form(""),
    resumo: str = Form(""),
    _: bool = require_basic_auth,
):
    with get_session() as db:
        m = Mensagem(
            titulo=titulo,
            pregador=pregador or None,
            data=data or None,
            video_url=video_url or None,
            audio_url=audio_url or None,
            capa_url=capa_url or None,
            resumo=resumo or None,
        )
        db.add(m)
        db.commit()
    return RedirectResponse(url="/admin/mensagens", status_code=status.HTTP_302_FOUND)

@app.get("/admin/mensagens/editar/{id}", response_class=HTMLResponse)
async def admin_mensagens_edit(id: int, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        item = db.get(Mensagem, id)
    t = templates_env.get_template("admin_mensagens_form.html")
    return t.render(item=item)

@app.post("/admin/mensagens/editar/{id}")
async def admin_mensagens_update(
    id: int,
    titulo: str = Form(""),
    pregador: str = Form(""),
    data: str = Form(""),
    video_url: str = Form(""),
    audio_url: str = Form(""),
    capa_url: str = Form(""),
    resumo: str = Form(""),
    _: bool = require_basic_auth,
):
    with get_session() as db:
        item = db.get(Mensagem, id)
        if item:
            item.titulo = titulo
            item.pregador = pregador or None
            item.data = data or None
            item.video_url = video_url or None
            item.audio_url = audio_url or None
            item.capa_url = capa_url or None
            item.resumo = resumo or None
            db.commit()
    return RedirectResponse(url="/admin/mensagens", status_code=status.HTTP_302_FOUND)

@app.post("/admin/mensagens/excluir/{id}")
async def admin_mensagens_delete(id: int, _: bool = Depends(require_basic_auth)):
    with get_session() as db:
        item = db.get(Mensagem, id)
        if item:
            db.delete(item)
            db.commit()
    return RedirectResponse(url="/admin/mensagens", status_code=status.HTTP_302_FOUND)
