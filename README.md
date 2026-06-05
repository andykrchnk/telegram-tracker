# Telegram Tracker

![python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)

The Telegram Tracker is a Python project designed to monitor the online/offline activity of your Telegram contacts and store this data in a MySQL/SQLite database.

The motivation for creating this project came from my desire to study data science and data analysis.

## Features

- **Contact Monitoring**: Keep track of when your Telegram contacts go online and offline.
- **Data Storage**: Store the timestamps of online and offline events in a MySQL or SQLite database.
- **Activity Insights**: Gain insights into your contacts' online patterns over time.

## Setup and Usage

1. **Clone the repository**: Start by cloning this repository to your local machine.

   ```bash
   git clone https://github.com/cubicbyte/telegram-tracker.git
   cd telegram-tracker
   ```

2. **Install dependencies**: Install the necessary dependencies using the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup .env configuration file**: Copy `.env.example` to `.env` and modify it according to your needs. Update the `API_ID` and `API_HASH` with your Telegram API credentials (https://my.telegram.org):

4. **Database setup**: Depending on the chosen database type, run either `scripts/setup_mysql_db.py` or `scripts/setup_sqlite_db.py` to set up the database structure. Default database is sqlite.

5. **Run the tracker**: Execute the main script:

   ```bash
   python main.py
   ```

   At first startup the program will guide you through the login process for Telegram.

## Railway + SQLite Deployment

This repository includes a `railway.toml` and `scripts/start_railway.sh` so Railway can build the Python app with Railpack, initialize SQLite, and start the long-running Telegram tracker.

For the fastest reusable deploy flow, create a Railway Template from this repo. The template can prompt for the Telegram secrets and include the SQLite volume. See [RAILWAY_TEMPLATE.md](RAILWAY_TEMPLATE.md).

After you publish the template, add the generated template URL here:

```md
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/YOUR_TEMPLATE_CODE)
```

Until the template exists, deploy from GitHub with the steps below.

### 1. Generate a Telegram session string

Railway deployments are headless, so generate a Telethon session locally and store it as a Railway variable.

```bash
cp .env.example .env
# Fill API_ID and API_HASH in .env first.
pip install -r requirements.txt
python scripts/generate_session_string.py
```

Copy the printed value. Treat it like a password because it authenticates your Telegram account.

### 2. Create the Railway service

Create a new Railway project from this GitHub repository, or deploy with the Railway CLI:

```bash
railway login
railway init
railway up
```

### 3. Add a persistent volume

Attach a volume to the tracker service and set the mount path to:

```text
/app/data
```

The startup script stores SQLite at `/app/data/database.sqlite` by default. If no volume is attached, the app can still boot, but the SQLite database will not survive redeploys.

### 4. Set Railway variables

Add these service variables in Railway:

```text
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
TELEGRAM_SESSION_STRING=the_value_from_generate_session_string
```

Optional variables:

```text
DB_TYPE=sqlite
LOG_USER_UPDATES=false
ESCAPE_EMOJIS=false
DB_PATH=/app/data/database.sqlite
```

Leave `DB_PATH` unset unless you want a custom SQLite path.

### 5. Deploy

Trigger a deploy from Railway or run:

```bash
railway up
```

Keep this service at one replica when using SQLite and one Telegram session. SQLite is a local file database, and this tracker is designed as a single long-running collector process.

## Viewing Tracked Data

For live activity, open the Railway service logs. If `LOG_USER_UPDATES=true`, the app prints online/offline changes as they arrive.

To inspect the SQLite rows, SSH into the deployed Railway service:

```bash
railway login
railway link
railway ssh
```

Then run:

```bash
python scripts/view_data.py
```

Useful filters:

```bash
python scripts/view_data.py --limit 100
python scripts/view_data.py --user-id 123456789
```

The SQLite file is stored at:

```text
/app/data/database.sqlite
```

You can also query it directly if `sqlite3` is available in the container:

```bash
sqlite3 /app/data/database.sqlite 'SELECT * FROM users ORDER BY status_time DESC LIMIT 20;'
sqlite3 /app/data/database.sqlite 'SELECT * FROM updates ORDER BY time DESC LIMIT 50;'
```

## Disclaimer

This project is meant for personal and educational purposes as it said in the description. Respect the privacy of your contacts and ensure you have their consent before tracking their online activity.

## Contributing

Contributions are welcome! If you find issues or have feature ideas, feel free to open an issue or pull request.

## License

This project is licensed under the [MIT License](LICENSE).
