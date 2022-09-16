''' Downloads image then copy-pastes it '''

import logging
import os
import random
import shutil
from pathlib import Path
import keyboard
from icrawler.builtin import GoogleImageCrawler
from helpers import copy_image, keystrokes_to_string, clear_input_field
from settings import Settings


def get_and_copy_image(query: str, max_offset: int = 20) -> str:
    ''' Downloads the image from @link and returns its filepath '''

    random_offset = random.randrange(0, max_offset + 1)
    destination_path = os.path.join('output', 'images')

    shutil.rmtree(destination_path)

    crawler = GoogleImageCrawler(
        storage={'root_dir': destination_path}, log_level=logging.CRITICAL)
    crawler.crawl(query, max_num=1, offset=random_offset,)

    logging.info('Successfully downloaded image \'%s\'', query)

    image_path = os.path.join(
        destination_path,
        os.listdir(destination_path)[0])

    copy_image(image_path)
    keyboard.press_and_release('ctrl + v')

    logging.info('Successfully copy-pasted image \'%s\'', query)

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
            logging.info('Summoned Image')

            print(f'Reading image name, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            clear_input_field()
            image_name = keystrokes_to_string(
                keystrokes).replace(submit_hotkey, '')

            logging.info("Searching for image: '%s'", image_name)

            get_and_copy_image(image_name,
                               Settings.get_setting('image.max_offset'))
        except Exception:                                                       # pylint: disable=broad-except
            logging.error("Exception occurred in Image", exc_info=True)


if __name__ == '__main__':
    Settings.load_settings()
    listen_image()
