from app.models import AuditEvent, Lead


UNSUBSCRIBE_FOOTER = (
    "\n\n---\n"
    "You are receiving this message because we believe this offer may be relevant to your business role. "
    "If you do not want further emails, reply with 'unsubscribe' or click the opt-out link in production."
)


def can_contact(lead: Lead) -> bool:
    return not lead.opted_out and lead.country in {'France', 'Switzerland', 'Luxembourg'}


def mark_opt_out(db, lead: Lead, reason: str = 'reply request'):
    lead.opted_out = True
    db.add(AuditEvent(event_type='lead_opt_out', actor='ai-agent', payload=f'{lead.email} | {reason}'))
