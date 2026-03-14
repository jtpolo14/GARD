import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    agent_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("agents.id"), nullable=False
    )
    process_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    input_data: Mapped[str] = mapped_column(Text, nullable=False)  # JSON
    rules_evaluated: Mapped[str] = mapped_column(Text, nullable=False)  # JSON
    rules_triggered: Mapped[str] = mapped_column(Text, nullable=False)  # JSON
    outcome: Mapped[str] = mapped_column(Text, nullable=False)  # JSON
    decision: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    agent = relationship("Agent", back_populates="decision_logs")
