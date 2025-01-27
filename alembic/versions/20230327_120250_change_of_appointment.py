"""Change of appointment

Revision ID: 9d82dfea55f2
Revises: 83a474212a84
Create Date: 2023-03-27 12:02:50.181329

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9d82dfea55f2"
down_revision = "83a474212a84"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "appointment", sa.Column("nutritionist_id", postgresql.UUID(as_uuid=True), nullable=False)
    )
    op.alter_column(
        "appointment", "date", existing_type=sa.DATE(), type_=sa.DateTime(), existing_nullable=False
    )
    op.create_foreign_key(
        None, "appointment", "user", ["nutritionist_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "appointment", type_="foreignkey")
    op.alter_column(
        "appointment", "date", existing_type=sa.DateTime(), type_=sa.DATE(), existing_nullable=False
    )
    op.drop_column("appointment", "nutritionist_id")
    # ### end Alembic commands ###
