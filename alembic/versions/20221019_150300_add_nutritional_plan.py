"""Add Nutritional Plan

Revision ID: 7ff02749cf32
Revises: 95f6ac6c9461
Create Date: 2022-10-19 15:03:00.935598

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7ff02749cf32"
down_revision = "95f6ac6c9461"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "nutritional_plan",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("calories_limit", sa.Integer(), nullable=True),
        sa.Column("lipids_limit", sa.Integer(), nullable=True),
        sa.Column("proteins_limit", sa.Integer(), nullable=True),
        sa.Column("carbohydrates_limit", sa.Integer(), nullable=True),
        sa.Column(
            "period_limit", sa.Enum("DAILY", "WEEKLY", "BY_MEAL", name="periods"), nullable=False
        ),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("nutritional_plan")
    # ### end Alembic commands ###
