"""Store explicit, owner-protected comparison snapshots."""
from alembic import op
import sqlalchemy as sa

revision = '0002_saved_comparisons'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('saved_comparisons',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resumes.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(120), nullable=False),
        sa.Column('job_description', sa.Text(), nullable=False),
        sa.Column('result', sa.JSON(), nullable=False),
        sa.Column('label_choices', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_index('ix_saved_comparisons_resume_id', 'saved_comparisons', ['resume_id'])
    op.create_index('ix_saved_comparisons_user_id', 'saved_comparisons', ['user_id'])


def downgrade():
    raise RuntimeError('Downgrade would delete saved comparisons; restore a verified backup instead.')
