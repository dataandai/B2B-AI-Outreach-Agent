from app.models import AuditEvent, InboundReply, Lead
from app.services.compliance import mark_opt_out


INTEREST_KEYWORDS = {'interested', 'demo', 'call', 'pricing', 'more info', 'information', 'meeting'}
REJECT_KEYWORDS = {'not interested', 'no thanks', 'remove me', 'stop', 'unsubscribe'}


def detect_intent(body: str) -> str:
    text = body.lower()
    if any(keyword in text for keyword in REJECT_KEYWORDS):
        if 'unsubscribe' in text or 'remove me' in text or 'stop' in text:
            return 'unsubscribe'
        return 'not_interested'
    if any(keyword in text for keyword in INTEREST_KEYWORDS):
        if 'pricing' in text or 'more info' in text or 'information' in text:
            return 'request_info'
        return 'interested'
    return 'neutral'


def score_lead(lead: Lead, intent: str) -> tuple[str, float]:
    if intent == 'interested':
        return 'Hot', 92.0
    if intent == 'request_info':
        return 'Warm', 71.0
    if intent == 'not_interested':
        return 'Cold', 10.0
    if intent == 'unsubscribe':
        return 'Cold', 0.0
    return lead.status, lead.score


def draft_response(lead: Lead, intent: str) -> str:
    if intent == 'interested':
        return f"Thanks {lead.contact_name}, great to hear. I can send a short overview and propose two time slots for a quick call this week."
    if intent == 'request_info':
        return f"Thanks {lead.contact_name}. Here is a concise overview: we automate prospect sourcing, outreach sequencing, inbox triage and lead qualification for B2B teams."
    if intent == 'not_interested':
        return f"Understood {lead.contact_name}, thanks for the reply. I will not follow up further."
    if intent == 'unsubscribe':
        return f"Thanks {lead.contact_name}. You have been removed from future outreach."
    return f"Thanks {lead.contact_name}. I received your message and will review it shortly."


def process_reply(db, lead: Lead, subject: str, body: str) -> InboundReply:
    intent = detect_intent(body)
    status, score = score_lead(lead, intent)
    lead.status = status
    lead.score = score
    if intent == 'unsubscribe':
        mark_opt_out(db, lead)

    auto_response = draft_response(lead, intent)
    reply = InboundReply(
        lead_id=lead.id,
        subject=subject,
        body=body,
        detected_intent=intent,
        auto_response=auto_response,
        handled=True,
    )
    db.add(reply)
    db.add(AuditEvent(event_type='reply_processed', actor='ai-agent', payload=f'lead={lead.email}|intent={intent}|score={score}'))
    db.commit()
    db.refresh(reply)
    return reply
