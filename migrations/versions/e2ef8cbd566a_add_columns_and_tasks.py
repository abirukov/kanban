"""Add Columns and tasks

Revision ID: e2ef8cbd566a
Revises: 
Create Date: 2023-03-18 19:25:46.878819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2ef8cbd566a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('columns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('sort', sa.Integer(), nullable=False),
    sa.Column('is_delete', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('is_important', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=False),
    sa.Column('column_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['column_id'], ['columns.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('columns')
    # ### end Alembic commands ###
