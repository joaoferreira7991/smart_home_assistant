"""first

Revision ID: 186af72f62f7
Revises: 
Create Date: 2020-06-24 17:28:08.059340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186af72f62f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('home',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_name'), 'home', ['name'], unique=False)
    op.create_table('reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('data_reading', sa.Float(), nullable=False),
    sa.Column('data_type', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reading_timestamp'), 'reading', ['timestamp'], unique=False)
    op.create_table('actuator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('interruptor', sa.Boolean(), nullable=False),
    sa.Column('home_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actuator_name'), 'actuator', ['name'], unique=False)
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('home_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sensor_name'), 'sensor', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=512), nullable=False),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_sensor_name'), table_name='sensor')
    op.drop_table('sensor')
    op.drop_index(op.f('ix_actuator_name'), table_name='actuator')
    op.drop_table('actuator')
    op.drop_index(op.f('ix_reading_timestamp'), table_name='reading')
    op.drop_table('reading')
    op.drop_index(op.f('ix_home_name'), table_name='home')
    op.drop_table('home')
    # ### end Alembic commands ###