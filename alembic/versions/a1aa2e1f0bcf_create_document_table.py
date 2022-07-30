"""create document table

Revision ID: a1aa2e1f0bcf
Revises: 
Create Date: 2022-07-30 16:27:52.927118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1aa2e1f0bcf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement="ignore_fk"),
        sa.Column("date", sa.DateTime(), index=True),
        sa.Column("text", sa.Text())
    )


def downgrade() -> None:
    op.drop_table("documents")
