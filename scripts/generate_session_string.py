#!/usr/bin/env python3

import os

import dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession


def main():
    dotenv.load_dotenv()

    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')

    assert api_id is not None, 'API_ID is not set'
    assert api_hash is not None, 'API_HASH is not set'
    assert api_id.isdigit(), 'API_ID is not a number'

    with TelegramClient(StringSession(), int(api_id), api_hash) as client:
        print(client.session.save())


if __name__ == '__main__':
    main()
