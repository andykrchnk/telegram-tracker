#!/usr/bin/env python3

import argparse
import os
import sqlite3


def default_db_path():
    data_dir = os.getenv('RAILWAY_VOLUME_MOUNT_PATH') or os.getenv('DATA_DIR') or '.'
    return os.getenv('DB_PATH') or os.path.join(data_dir, 'database.sqlite')


def print_rows(title, rows):
    print(f'\n{title}')
    print('-' * len(title))

    if not rows:
        print('No rows found.')
        return

    for row in rows:
        print(dict(row))


def main():
    parser = argparse.ArgumentParser(description='View Telegram tracker SQLite data.')
    parser.add_argument('--db-path', default=default_db_path(), help='SQLite database path.')
    parser.add_argument('--limit', type=int, default=25, help='Number of rows to show per section.')
    parser.add_argument('--user-id', type=int, help='Only show data for this Telegram user id.')
    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        raise SystemExit(f'Database not found: {args.db_path}')

    connection = sqlite3.connect(args.db_path)
    connection.row_factory = sqlite3.Row

    filters = []
    params = []
    if args.user_id is not None:
        filters.append('id = ?')
        params.append(args.user_id)

    where = f'WHERE {" AND ".join(filters)}' if filters else ''

    users = connection.execute(
        f'''
        SELECT
            id,
            status_online,
            status_time,
            status_expires,
            username,
            first_name,
            last_name,
            phone_number
        FROM users
        {where}
        ORDER BY status_time DESC
        LIMIT ?
        ''',
        [*params, args.limit],
    ).fetchall()

    updates = connection.execute(
        f'''
        SELECT
            id,
            CASE state WHEN 1 THEN 'online' ELSE 'offline' END AS state,
            time
        FROM updates
        {where}
        ORDER BY time DESC
        LIMIT ?
        ''',
        [*params, args.limit],
    ).fetchall()

    print(f'Database: {args.db_path}')
    print_rows('Latest Users', users)
    print_rows('Latest Status Updates', updates)


if __name__ == '__main__':
    main()
