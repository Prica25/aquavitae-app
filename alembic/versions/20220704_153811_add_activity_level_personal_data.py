"""Add Activity level & personal data

Revision ID: bf8a87127147
Revises: 36bff7b82540
Create Date: 2022-07-04 15:38:11.227017

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bf8a87127147'
down_revision = '36bff7b82540'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity_level',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('factor', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personal_data',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('birthday', sa.DateTime(), nullable=False),
    sa.Column('occupation', sa.String(length=255), nullable=False),
    sa.Column('food_history', sa.String(length=1000), nullable=False),
    sa.Column('bedtime', sa.Time(timezone=True), nullable=False),
    sa.Column('wake_up', sa.Time(timezone=True), nullable=False),
    sa.Column('activity_level_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['activity_level_id'], ['activity_level.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('food_food_category_id_fkey', 'food', type_='foreignkey')
    op.create_foreign_key(None, 'food', 'food_category', ['food_category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'food', type_='foreignkey')
    op.create_foreign_key('food_food_category_id_fkey', 'food', 'food_category', ['food_category_id'], ['id'])
    op.drop_table('personal_data')
    op.drop_table('activity_level')
    # ### end Alembic commands ###
