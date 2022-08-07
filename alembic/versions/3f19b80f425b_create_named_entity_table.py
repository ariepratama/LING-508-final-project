"""create named_entity table

Revision ID: 3f19b80f425b
Revises: a1aa2e1f0bcf
Create Date: 2022-08-06 23:22:19.773042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f19b80f425b'
down_revision = 'a1aa2e1f0bcf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "document_named_entities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement="ignore_fk"),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id"), index=True),
        sa.Column("start_span", sa.Integer()),
        sa.Column("end_span", sa.Integer()),
        sa.Column("ner_tag", sa.String(100)),
        sa.Column("ner_category", sa.String(100), index=True)
    )


def downgrade() -> None:
    op.drop_table("document_named_entities")
