"""empty message

Revision ID: ceffccd10b5a
Revises:
Create Date: 2024-03-04 12:37:02.893840

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize

# revision identifiers, used by Alembic.
revision = 'ceffccd10b5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('restrictions', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('allowances', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('mobile_number', sa.String(length=15), nullable=False),
    sa.Column('lms_user_id', sa.Integer(), nullable=True),
    sa.Column('otp', sa.Integer(), nullable=True),
    sa.Column('otp_token', sa.String(length=32), nullable=True),
    sa.Column('verification_token', sa.String(length=1024), nullable=True),
    sa.Column('verification_token_valid_until', sa.DateTime(), nullable=True),
    sa.Column('otp_valid_until', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('date_of_birth', sa.String(length=20), nullable=True),
    sa.Column('nationality', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('oauth2_client',
    sa.Column('client_id', sa.String(length=48), nullable=True),
    sa.Column('client_secret', sa.String(length=120), nullable=True),
    sa.Column('client_id_issued_at', sa.Integer(), nullable=False),
    sa.Column('client_secret_expires_at', sa.Integer(), nullable=False),
    sa.Column('client_metadata', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth2_client_client_id'), 'oauth2_client', ['client_id'], unique=False)
    op.create_table('oauth2_code',
    sa.Column('code', sa.String(length=120), nullable=False),
    sa.Column('client_id', sa.String(length=48), nullable=True),
    sa.Column('redirect_uri', sa.Text(), nullable=True),
    sa.Column('response_type', sa.Text(), nullable=True),
    sa.Column('scope', sa.Text(), nullable=True),
    sa.Column('nonce', sa.Text(), nullable=True),
    sa.Column('auth_time', sa.Integer(), nullable=False),
    sa.Column('code_challenge', sa.Text(), nullable=True),
    sa.Column('code_challenge_method', sa.String(length=48), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('oauth2_token',
    sa.Column('client_id', sa.String(length=48), nullable=True),
    sa.Column('token_type', sa.String(length=40), nullable=True),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('scope', sa.Text(), nullable=True),
    sa.Column('revoked', sa.Boolean(), nullable=True),
    sa.Column('issued_at', sa.Integer(), nullable=False),
    sa.Column('expires_in', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token')
    )
    op.create_index(op.f('ix_oauth2_token_refresh_token'), 'oauth2_token', ['refresh_token'], unique=False)
    op.create_table('token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    op.create_table('user_device_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('device_info', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user_group')
    op.drop_table('user_device_token')
    op.drop_table('token_blocklist')
    op.drop_index(op.f('ix_oauth2_token_refresh_token'), table_name='oauth2_token')
    op.drop_table('oauth2_token')
    op.drop_table('oauth2_code')
    op.drop_index(op.f('ix_oauth2_client_client_id'), table_name='oauth2_client')
    op.drop_table('oauth2_client')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('group')
    # ### end Alembic commands ###
