"""add base entities

Revision ID: 6329b98ac97c
Revises: 1a31ce608336
Create Date: 2024-11-05 22:06:29.311289

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '6329b98ac97c'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


role_enum = ENUM('hr', 'interviewer', 'applicant', name='role', create_type=True)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    role_enum.create(op.get_bind(), checkfirst=True)

    op.drop_column('user', 'id')
    op.add_column('user', sa.Column('login', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False))
    op.add_column('user', sa.Column('role', role_enum, nullable=False))
    op.create_primary_key('pk_user_login', 'user', ['login'])

    op.create_table('stacktag',
    sa.Column('tag_code', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.PrimaryKeyConstraint('tag_code')
    )
    op.create_table('interview',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('interviewer_login', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('applicant_login', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('link', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('type', sa.Enum('algo', 'backend', name='interviewtype'), nullable=False),
    sa.Column('status', sa.Enum('waiting', 'in_progress', 'finished', name='interviewstatus'), nullable=False),
    sa.Column('mark', sa.Enum('waiting', 'in_progress', 'finished', name='interviewstatus'), nullable=True),
    sa.Column('comments', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['applicant_login'], ['user.login'], ),
    sa.ForeignKeyConstraint(['interviewer_login'], ['user.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interviewslot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_login', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('event_datetime', sa.DateTime(), nullable=False),
    sa.Column('max_applicant', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_login'], ['user.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('interviewslot')
    op.drop_table('interview')
    op.drop_table('stacktag')

    op.add_column('user', sa.Column('id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint('pk_user_login', 'user', type_='primary')
    op.drop_column('user', 'role')
    op.drop_column('user', 'login')
    role_enum.drop(op.get_bind(), checkfirst=True)
    op.create_table('item',

    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('owner_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name='item_owner_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='item_pkey')
    )
    # ### end Alembic commands ###
