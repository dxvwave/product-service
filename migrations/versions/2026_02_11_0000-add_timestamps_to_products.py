"""add timestamps to products

Revision ID: b1c2d3e4f5a6
Revises: ea8ff69b4a6a
Create Date: 2026-02-11 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, Sequence[str], None] = "ea8ff69b4a6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add created_at and updated_at columns
    op.add_column(
        "products",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    
    # Add index on name column
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index
    op.drop_index(op.f("ix_products_name"), table_name="products")
    
    # Drop timestamp columns
    op.drop_column("products", "updated_at")
    op.drop_column("products", "created_at")
