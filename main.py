from telethon.sync import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from datetime import datetime
import time
import os

from argparse import ArgumentParser
from src.generators.generate_quote_image import generate_and_save_quote

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
            generate_and_save_quote()
            prev_update_time = convert_time_to_string(datetime.now())
            # client(DeletePhotosRequest(client.get_profile_photos('me')))
            client(DeletePhotosRequest(client.get_profile_photos('me', limit=1)))
            path_to_file = os.getcwd() + f"/src/quote_images/new_quote.jpg"
            file = client.upload_file(path_to_file)
            client(UploadProfilePhotoRequest(file))
        time.sleep(1)

if __name__ == '__main__':
    main()

