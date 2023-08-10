"""create_table

Revision ID: b2805ea27732
Revises: 
Create Date: 2023-08-02 18:00:42.372466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2805ea27732'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('average_score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('companies',
    sa.Column('company_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('visibility', sa.Enum('HIDDEN', 'VISIBLE_TO_ALL', name='companyvisibility'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('company_id')
    )
    op.create_table('company_membership',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('is_owner', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'company_id')
    )
    op.create_table('company_requests',
    sa.Column('request_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'DECLINED', 'DEACTIVATED', name='requeststatus'), nullable=True),
    sa.Column('created_by', sa.Enum('USER', 'COMPANY', name='requestcreatedby'), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_table('company_roles',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('role_type', sa.Enum('OWNER', 'ADMIN', 'USER', name='roletype'), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('quizzes',
    sa.Column('quiz_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('frequency_in_days', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.PrimaryKeyConstraint('quiz_id')
    )
    op.create_table('questions',
    sa.Column('question_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_text', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
    sa.PrimaryKeyConstraint('question_id')
    )
    op.create_table('answers',
    sa.Column('answer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer_text', sa.String(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
    sa.PrimaryKeyConstraint('answer_id')
    )
    op.create_table('user_answers',
    sa.Column('user_answer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['answer_id'], ['answers.answer_id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_answer_id')
    )
    op.create_table('quiz_results',
    sa.Column('result_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('user_answer_id', sa.Integer(), nullable=False),
    sa.Column('result', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
    sa.ForeignKeyConstraint(['user_answer_id'], ['user_answers.user_answer_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('result_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz_results')
    op.drop_table('user_answers')
    op.drop_table('answers')
    op.drop_table('questions')
    op.drop_table('quizzes')
    op.drop_table('company_roles')
    op.drop_table('company_requests')
    op.drop_table('company_membership')
    op.drop_table('companies')
    op.drop_table('users')
    # ### end Alembic commands ###
