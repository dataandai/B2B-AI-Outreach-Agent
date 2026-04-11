from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class Lead(Base):
    __tablename__ = 'leads'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    contact_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    industry: Mapped[str] = mapped_column(String(120))
    country: Mapped[str] = mapped_column(String(120))
    source: Mapped[str] = mapped_column(String(120), default='Google Maps')
    website: Mapped[str] = mapped_column(String(255), default='')
    status: Mapped[str] = mapped_column(String(50), default='Cold')
    score: Mapped[float] = mapped_column(Float, default=20.0)
    opted_out: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    emails = relationship('EmailMessage', back_populates='lead', cascade='all, delete-orphan')
    replies = relationship('InboundReply', back_populates='lead', cascade='all, delete-orphan')


class Campaign(Base):
    __tablename__ = 'campaigns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    target_country: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default='Draft')
    sequence_steps: Mapped[int] = mapped_column(Integer, default=3)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    open_rate: Mapped[float] = mapped_column(Float, default=0.0)
    reply_rate: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EmailMessage(Base):
    __tablename__ = 'email_messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey('leads.id'))
    subject: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    direction: Mapped[str] = mapped_column(String(20), default='outbound')
    step_number: Mapped[int] = mapped_column(Integer, default=1)
    delivery_status: Mapped[str] = mapped_column(String(50), default='sent')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lead = relationship('Lead', back_populates='emails')


class InboundReply(Base):
    __tablename__ = 'inbound_replies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey('leads.id'))
    subject: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    detected_intent: Mapped[str] = mapped_column(String(50), default='unknown')
    auto_response: Mapped[str] = mapped_column(Text, default='')
    handled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lead = relationship('Lead', back_populates='replies')


class AuditEvent(Base):
    __tablename__ = 'audit_events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100))
    actor: Mapped[str] = mapped_column(String(120), default='system')
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
