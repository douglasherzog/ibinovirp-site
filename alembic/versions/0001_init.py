from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'site_config',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome_igreja', sa.String(length=200), nullable=True),
        sa.Column('descricao_breve', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'ministerios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(length=200), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('imagem', sa.String(length=500), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'eventos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(length=200), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('local', sa.String(length=200), nullable=True),
        sa.Column('inicio', sa.String(length=50), nullable=True),
        sa.Column('fim', sa.String(length=50), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'mensagens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(length=200), nullable=False),
        sa.Column('pregador', sa.String(length=200), nullable=True),
        sa.Column('data', sa.String(length=50), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('audio_url', sa.String(length=500), nullable=True),
        sa.Column('capa_url', sa.String(length=500), nullable=True),
        sa.Column('resumo', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    op.drop_table('mensagens')
    op.drop_table('eventos')
    op.drop_table('ministerios')
    op.drop_table('site_config')
