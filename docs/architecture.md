# Architecture

## Overview

The MVP uses a single FastAPI app with server-rendered templates to demonstrate the full workflow without needing external infrastructure.

## Components

- **Web router**: serves the dashboard and demo forms
- **Database layer**: SQLAlchemy models for leads, campaigns, messages, replies and audit events
- **Email engine**: renders outbound sequence content and simulates campaign sending
- **AI engine**: classifies inbound reply intent using deterministic rules and updates lead score/status
- **Compliance service**: enforces basic market and opt-out rules
- **Seed service**: initializes demo records for immediate presentation

## Flow

1. Seed leads and campaigns on startup.
2. User launches a campaign.
3. Email engine creates outbound messages and updates KPIs.
4. User simulates an inbound reply.
5. AI engine classifies intent and drafts an appropriate response.
6. Lead is re-scored as Cold, Warm or Hot.
7. Compliance logic applies opt-out where needed.
8. Audit event is recorded.
