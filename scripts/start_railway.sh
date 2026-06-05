#!/usr/bin/env sh
set -eu

DATA_DIR="${RAILWAY_VOLUME_MOUNT_PATH:-${DATA_DIR:-/app/data}}"
mkdir -p "$DATA_DIR"

export DB_TYPE="${DB_TYPE:-sqlite}"
export DB_PATH="${DB_PATH:-$DATA_DIR/database.sqlite}"
export TELEGRAM_SESSION="${TELEGRAM_SESSION:-$DATA_DIR/status-collector}"

if [ "$DB_TYPE" = "sqlite" ]; then
    python scripts/setup_sqlite_db.py
fi

exec python main.py
