from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from .database import Base

class SiteConfig(Base):
    __tablename__ = "site_config"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome_igreja: Mapped[str | None] = mapped_column(String(200), nullable=True)
    descricao_breve: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Ministerio(Base):
    __tablename__ = "ministerios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagem: Mapped[str | None] = mapped_column(String(500), nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Evento(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    local: Mapped[str | None] = mapped_column(String(200), nullable=True)
    inicio: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fim: Mapped[str | None] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Mensagem(Base):
    __tablename__ = "mensagens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    pregador: Mapped[str | None] = mapped_column(String(200), nullable=True)
    data: Mapped[str | None] = mapped_column(String(50), nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    capa_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resumo: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
