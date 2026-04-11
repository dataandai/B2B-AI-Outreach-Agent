from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditEvent, Campaign, InboundReply, Lead
from app.schemas import LeadCreate
from app.services.ai_engine import process_reply
from app.services.email_engine import launch_campaign

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/')
def dashboard(request: Request, db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.score.desc()).all()
    campaigns = db.query(Campaign).order_by(Campaign.created_at.desc()).all()
    replies = db.query(InboundReply).order_by(InboundReply.created_at.desc()).all()
    events = db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(10).all()

    stats = {
        'total_leads': len(leads),
        'hot_leads': len([l for l in leads if l.status == 'Hot']),
        'warm_leads': len([l for l in leads if l.status == 'Warm']),
        'opt_outs': len([l for l in leads if l.opted_out]),
        'emails_sent': sum(c.sent_count for c in campaigns),
        'avg_open_rate': round(sum(c.open_rate for c in campaigns) / len(campaigns), 1) if campaigns else 0,
        'avg_reply_rate': round(sum(c.reply_rate for c in campaigns) / len(campaigns), 1) if campaigns else 0,
    }
    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'stats': stats,
        'leads': leads,
        'campaigns': campaigns,
        'replies': replies,
        'events': events,
    })


@router.post('/campaign/{campaign_id}/launch')
def run_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).get(campaign_id)
    if campaign:
        launch_campaign(db, campaign)
    return RedirectResponse(url='/', status_code=303)


@router.post('/reply/simulate')
def simulate_reply(lead_id: int = Form(...), subject: str = Form(...), body: str = Form(...), db: Session = Depends(get_db)):
    lead = db.query(Lead).get(lead_id)
    if lead:
        process_reply(db, lead, subject, body)
    return RedirectResponse(url='/', status_code=303)


@router.post('/lead/create')
def create_lead(
    company_name: str = Form(...),
    contact_name: str = Form(...),
    email: str = Form(...),
    industry: str = Form(...),
    country: str = Form(...),
    source: str = Form('Google Maps'),
    website: str = Form(''),
    db: Session = Depends(get_db),
):
    payload = LeadCreate(
        company_name=company_name,
        contact_name=contact_name,
        email=email,
        industry=industry,
        country=country,
        source=source,
        website=website,
    )
    db.add(Lead(**payload.model_dump()))
    db.commit()
    return RedirectResponse(url='/', status_code=303)
