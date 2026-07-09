"""add conversation message metadata

Revision ID: be74e955d9e2
Revises: 299a8e789938
Create Date: 2026-07-09

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "be74e955d9e2"
down_revision: Union[str, Sequence[str], None] = "299a8e789938"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # Add new metadata columns
    # ------------------------------------------------------------------

    op.add_column(
        "conversation_messages",
        sa.Column(
            "model_name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "conversation_messages",
        sa.Column(
            "prompt_tokens",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "conversation_messages",
        sa.Column(
            "completion_tokens",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "conversation_messages",
        sa.Column(
            "total_tokens",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "conversation_messages",
        sa.Column(
            "generation_time_ms",
            sa.Integer(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("conversation_messages", "generation_time_ms")
    op.drop_column("conversation_messages", "total_tokens")
    op.drop_column("conversation_messages", "completion_tokens")
    op.drop_column("conversation_messages", "prompt_tokens")
    op.drop_column("conversation_messages", "model_name")
