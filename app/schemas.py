from pydantic import BaseModel


class ReplyPayload(BaseModel):
    lead_id: int
    subject: str
    body: str


class LeadCreate(BaseModel):
    company_name: str
    contact_name: str
    email: str
    industry: str
    country: str
    source: str = 'Google Maps'
    website: str = ''
