"""Add Diagnosis

Revision ID: a73206a8c93a
Revises: ef5039022972
Create Date: 2022-10-10 17:20:24.005006

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a73206a8c93a"
down_revision = "ef5039022972"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "diagnosis",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("main", sa.String(length=1000), nullable=False),
        sa.Column("secondary", sa.String(length=1000), nullable=True),
        sa.Column("bowel_function", sa.String(length=1000), nullable=True),
        sa.Column("send_by_doctor", sa.Boolean(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("diagnosis")
    # ### end Alembic commands ###