# Compliance posture for the MVP

This repository is a demonstration build and not legal advice.

## Included safeguards

- target markets are limited to France, Switzerland and Luxembourg in the demo data
- outbound email templates include opt-out language
- unsubscribe style replies mark the lead as opted out
- opted-out leads are no longer contactable through the campaign launcher
- audit events are recorded for campaign launches, reply handling and opt-outs

## Missing for production

- documented lawful basis and Legitimate Interest Assessment
- privacy notice generation per acquisition source
- source provenance retention policy
- suppression list synchronization across providers
- data subject access / deletion workflow
- per-country regulatory review
- deliverability and domain warm-up operations
