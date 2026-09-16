"""Baseline matching the existing users and resumes tables."""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_table('resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('stored_filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('resume_text', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('stored_filename'))
    op.create_index('ix_resumes_id', 'resumes', ['id'])
    op.create_index('ix_resumes_user_id', 'resumes', ['user_id'])


def downgrade():
    raise RuntimeError('The baseline downgrade would delete user data; restore a verified backup instead.')
