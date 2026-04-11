# Customer AI Agent MVP

A presentation-ready MVP for an autonomous B2B prospecting and email management agent.

## What this demo shows

- Lead list for France, Switzerland and Luxembourg
- Multi-campaign dashboard with outreach KPIs
- Campaign launch simulation
- AI-style inbound reply intent classification
- Lead qualification into Cold / Warm / Hot
- Compliance guardrails such as opt-out handling and audit events
- Clean UI suitable for client demos and screenshots

## Stack

- FastAPI
- Jinja2 templates
- SQLAlchemy
- SQLite for local demo
- Docker / Docker Compose

## Quick start

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

### Docker

```bash
docker compose up --build
```

## Demo scenario

1. Open the dashboard.
2. Launch `France AI Outreach Sprint`.
3. Add a sample lead.
4. Use **Simulate inbound reply** with text such as:
   - `We are interested. Please send more info and pricing.`
   - `Not interested, please remove me.`
5. Watch the lead status, score and audit log update.

## Project structure

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  routers/
  services/
  templates/
  static/
docs/
Dockerfile
docker-compose.yml
requirements.txt
```

## Notes for a production version

This repository is intentionally built as a local/demo MVP. For a production version you would typically add:

- PostgreSQL instead of SQLite
- Background workers for scheduled sends
- Real email provider integration
- OpenAI API integration for reply handling
- CRM sync
- User auth and team roles
- Full GDPR/legal review per target market

## Compliance notes

This MVP includes presentational compliance features, not legal advice:

- outbound messages contain an opt-out footer
- unsubscribe reply marks a lead as opted out
- audit events log campaign and reply actions
- only the target B2B markets are shown in the demo

Read `docs/compliance.md` before pitching it as a production-ready system.
