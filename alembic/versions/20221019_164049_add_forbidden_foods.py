"""Add Forbidden Foods

Revision ID: cdb5be91f04f
Revises: 7ff02749cf32
Create Date: 2022-10-19 16:40:49.987099

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cdb5be91f04f"
down_revision = "7ff02749cf32"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "forbidden_foods",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("food_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nutritional_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["food_id"], ["food.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["nutritional_plan_id"], ["nutritional_plan.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("forbidden_foods")
    # ### end Alembic commands ###
