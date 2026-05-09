"""Add lesson table

Revision ID: b9f1c0d3e201
Revises: a25a08db998a
Create Date: 2026-05-09 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b9f1c0d3e201'
down_revision = 'a25a08db998a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'lesson',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('about', sa.String(length=2000), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_type', sa.String(length=10), nullable=False),
        sa.Column('html_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('lesson')
