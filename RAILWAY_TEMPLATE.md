# Railway Template Setup

Use this checklist to turn the repo into a Railway one-click template.

Railway templates are created in the Railway dashboard, not from a committed repo manifest. The repo already contains the deploy config in `railway.toml`; the remaining template work is wiring the service variables and volume in Railway's template composer.

## Template Composer Settings

Create a new template from Railway:

1. Go to Workspace Settings -> Templates -> New Template.
2. Add a service from this GitHub repository.
3. Leave the build/start settings to the repo's `railway.toml`.
4. Do not enable public networking. This is a worker process, not a web app.
5. Keep replicas at `1`.

## Required Variables

Mark these as required template variables:

```text
API_ID=
API_HASH=
TELEGRAM_SESSION_STRING=
```

The deployer gets `API_ID` and `API_HASH` from https://my.telegram.org.

They generate `TELEGRAM_SESSION_STRING` locally:

```bash
cp .env.example .env
# Fill API_ID and API_HASH in .env.
pip install -r requirements.txt
python scripts/generate_session_string.py
```

## Default Variables

Add these as defaults in the template so users do not need to think about SQLite:

```text
DB_TYPE=sqlite
LOG_USER_UPDATES=true
ESCAPE_EMOJIS=false
```

Do not set `DB_PATH` in the template. The app defaults it to the attached Railway volume path.

## Volume

Attach one volume to the tracker service:

```text
/app/data
```

The app stores:

```text
/app/data/database.sqlite
/app/data/status-collector.session
```

When `TELEGRAM_SESSION_STRING` is set, Telethon uses that secret instead of the file session. The volume is still required for SQLite persistence.

## Publish Button

After creating the template, Railway gives you a template URL. Add this to `README.md`:

```md
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/YOUR_TEMPLATE_CODE)
```

Then the deploy flow is:

1. Click Deploy on Railway.
2. Paste `API_ID`, `API_HASH`, and `TELEGRAM_SESSION_STRING`.
3. Click Deploy.

SQLite setup and tracker startup are automatic.
