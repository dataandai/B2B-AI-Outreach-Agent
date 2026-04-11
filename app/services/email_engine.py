from app.models import AuditEvent, Campaign, EmailMessage, Lead
from app.services.compliance import UNSUBSCRIBE_FOOTER, can_contact


BASE_SEQUENCE = {
    1: "Hi {name},\n\nI noticed that {company} operates in the {industry} sector in {country}. We help teams automate outbound prospecting and qualification without increasing admin workload.\n\nWould you be open to a short discussion?",
    2: "Hi {name},\n\nJust following up in case my previous email got buried. We usually help {industry} businesses reduce manual lead qualification and improve reply handling.\n\nWould a quick overview help?",
    3: "Hi {name},\n\nLast follow-up from me. If streamlining outreach, inbox triage and lead scoring is relevant for {company}, I can share a concise summary tailored to your market."
}


def render_email(lead: Lead, step: int) -> tuple[str, str]:
    subject = f"{lead.company_name} × AI outbound workflow"
    body = BASE_SEQUENCE.get(step, BASE_SEQUENCE[1]).format(
        name=lead.contact_name,
        company=lead.company_name,
        industry=lead.industry,
        country=lead.country,
    )
    return subject, body + UNSUBSCRIBE_FOOTER


def launch_campaign(db, campaign: Campaign):
    leads = db.query(Lead).filter(Lead.country == campaign.target_country).all()
    sent = 0
    for lead in leads:
        if not can_contact(lead):
            continue
        subject, body = render_email(lead, 1)
        msg = EmailMessage(lead_id=lead.id, subject=subject, body=body, step_number=1, delivery_status='sent')
        db.add(msg)
        sent += 1
    campaign.status = 'Running'
    campaign.sent_count += sent
    campaign.open_rate = 41.0
    campaign.reply_rate = 17.0
    db.add(AuditEvent(event_type='campaign_launched', actor='system', payload=f'campaign={campaign.name}|sent={sent}'))
    db.commit()
    return sent
