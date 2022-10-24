"""Add nutritional Plan Has Meal

Revision ID: 008e676fd8a9
Revises: c6944dc89fa6
Create Date: 2022-10-20 15:07:41.542991

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "008e676fd8a9"
down_revision = "c6944dc89fa6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "nutritional_plan_has_meal",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("meal_date", sa.Date(), nullable=False),
        sa.Column("nutritional_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("meals_of_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["meals_of_plan_id"], ["meals_of_plan.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["nutritional_plan_id"], ["nutritional_plan.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("nutritional_plan_has_meal")
    # ### end Alembic commands ###