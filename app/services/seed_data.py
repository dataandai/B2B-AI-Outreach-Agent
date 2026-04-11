from app.models import AuditEvent, Campaign, Lead


DEMO_LEADS = [
    {
        'company_name': 'Atelier Growth',
        'contact_name': 'Claire Martin',
        'email': 'claire@atelier-growth.fr',
        'industry': 'Marketing Services',
        'country': 'France',
        'source': 'Google Maps',
        'website': 'https://atelier-growth.example',
        'status': 'Cold',
        'score': 24,
    },
    {
        'company_name': 'Lux Advisory Partners',
        'contact_name': 'Tom Weber',
        'email': 'tom@luxadvisory.lu',
        'industry': 'Financial Services',
        'country': 'Luxembourg',
        'source': 'Business Directory',
        'website': 'https://luxadvisory.example',
        'status': 'Warm',
        'score': 65,
    },
    {
        'company_name': 'Swiss Industrial Systems',
        'contact_name': 'Nina Keller',
        'email': 'nina@swissindustrial.ch',
        'industry': 'Industrial Automation',
        'country': 'Switzerland',
        'source': 'Google Maps',
        'website': 'https://swissindustrial.example',
        'status': 'Hot',
        'score': 88,
    },
    {
        'company_name': 'Bordeaux Data Conseil',
        'contact_name': 'Lucas Bernard',
        'email': 'lucas@bdconseil.fr',
        'industry': 'IT Consulting',
        'country': 'France',
        'source': 'LinkedIn Export',
        'website': 'https://bdconseil.example',
        'status': 'Cold',
        'score': 18,
    },
]


def seed_database(db):
    if db.query(Lead).count() == 0:
        for item in DEMO_LEADS:
            db.add(Lead(**item))
    if db.query(Campaign).count() == 0:
        db.add(Campaign(name='France AI Outreach Sprint', target_country='France', status='Draft', sequence_steps=3))
        db.add(Campaign(name='Luxembourg SDR Pilot', target_country='Luxembourg', status='Running', sequence_steps=3, sent_count=12, open_rate=46, reply_rate=20))
        db.add(Campaign(name='Swiss Market Entry', target_country='Switzerland', status='Paused', sequence_steps=4, sent_count=8, open_rate=38, reply_rate=12))
    db.add(AuditEvent(event_type='seed_loaded', actor='system', payload='Demo data initialized'))
    db.commit()
