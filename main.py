import os
import time
from argparse import ArgumentParser
from datetime import datetime

import requests

from src.generators.generate_quote_image import (generate_and_save_quote,
                                                 get_shiba)
from telethon.sync import TelegramClient
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)


def set_arguments(arg_parser: ArgumentParser):
    arg_parser.add_argument("--api_id", default=None)
    arg_parser.add_argument("--api_hash", default=None)

def convert_time_to_string(dt):
    return f"{dt.hour}:{dt.minute:02}" if dt.hour > 9 else f"0{dt.hour}:{dt.minute:02}"

def time_has_changed(prev_time):
    return convert_time_to_string(datetime.now()) != prev_time

def main():
    parser = ArgumentParser()
    set_arguments(parser)
    args = parser.parse_args()


    client = TelegramClient("tele_session", args.api_id, args.api_hash)
    client.start()

    prev_update_time = ""
    while True:
        if time_has_changed(prev_update_time):
            prev_update_time = convert_time_to_string(datetime.now())
            get_shiba()
            client(DeletePhotosRequest(client.get_profile_photos('me', limit=1)))
            file = client.upload_file(os.getcwd()+'/src/generators/shiba.jpg')
            client(UploadProfilePhotoRequest(file))
            os.remove(os.getcwd()+'/src/generators/shiba.jpg')
        time.sleep(1)

if __name__ == '__main__':
    main()
