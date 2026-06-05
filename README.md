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

Railway configures one deployment from `railway.toml`, but secrets and volumes still need to be configured in the Railway project.

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
DB_TYPE=sqlite
```

Optional variables:

```text
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

## Disclaimer

This project is meant for personal and educational purposes as it said in the description. Respect the privacy of your contacts and ensure you have their consent before tracking their online activity.

## Contributing

Contributions are welcome! If you find issues or have feature ideas, feel free to open an issue or pull request.

## License

This project is licensed under the [MIT License](LICENSE).
