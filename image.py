''' Downloads image then copy-pastes it '''

import os
import random
import shutil
from pathlib import Path
import keyboard
from icrawler.builtin import GoogleImageCrawler
from helpers import copy_image, keystrokes_to_string, clear_input_field
from settings import Settings


def get_and_copy_image(query: str, max_num: int = 5, max_offset: int = 20) -> str:
    ''' Downloads the image from @link and returns its filepath '''

    random_offset = random.randrange(0, max_offset + 1)
    destination_path = os.path.join('output', 'images')
    crawler = GoogleImageCrawler(storage={'root_dir': destination_path})
    shutil.rmtree(destination_path)
    crawler.crawl(query, max_num=max_num, offset=random_offset)

    chosen_image_path = os.path.join(
        destination_path, random.choice(os.listdir(destination_path)))

    copy_image(chosen_image_path)
    keyboard.press_and_release('ctrl + v')

    shutil.rmtree(destination_path)
    Path(destination_path).mkdir(parents=True, exist_ok=True)


def listen_image():
    ''' Main infinite loop '''

    launch_hotkey = Settings.get_setting('image.launch_hotkey')
    submit_hotkey = Settings.get_setting('image.submit_hotkey')
    while True:
        try:
            keyboard.wait(launch_hotkey)
            clear_input_field()

            print(f'Reading image name, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            clear_input_field()
            image_name = keystrokes_to_string(keystrokes)

            print(f"Searching for image: {image_name}")

            get_and_copy_image(image_name,
                               Settings.get_setting('image.pool_size'),
                               Settings.get_setting('image.max_offset'))
        except Exception as exception:                                                  # pylint: disable=broad-except
            print(
                f'Unidentified error in listen_image: {type(exception).__name__}')
            print(exception)


if __name__ == '__main__':
    Settings.load_settings()
    listen_image()
