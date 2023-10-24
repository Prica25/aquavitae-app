"""add_gender_column_to_personal_data

Revision ID: edc0a99d4fb6
Revises: 13962ec9075b
Create Date: 2023-10-24 13:51:54.535945

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'edc0a99d4fb6'
down_revision = '13962ec9075b'
branch_labels = None
depends_on = None

def upgrade():
    # Create the 'gender' enum type
    op.execute("CREATE TYPE gender AS ENUM ('MALE', 'FEMALE')")
    
    # Add the "gender" column with the enum constraint
    op.add_column(
        'personal_data',
        sa.Column('gender', sa.Enum("MALE", "FEMALE", name='gender'), nullable=False)
    )

def downgrade():
    # Remove the "gender" column
    op.drop_column('personal_data', 'gender')
    
    # Drop the 'gender' enum type
    op.execute("DROP TYPE gender")