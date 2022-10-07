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


def get_and_copy_image(query: str, max_num: int = 5) -> str:
    ''' Downloads the image from @link and returns its filepath '''

    # TODO: Find a better way to get a random image without downloading multiple ones
    destination_path = os.path.join('output', 'images')
    crawler = GoogleImageCrawler(storage={'root_dir': destination_path})

    shutil.rmtree(destination_path)         # Remove destination folder if it exists

    crawler.crawl(query, max_num=max_num)   # Download max_num number of images

    logging.info('Successfully downloaded image \'%s\'', query)

    # Choose a random image among the downloaded ones
    chosen_image_path = os.path.join(
        destination_path, random.choice(os.listdir(destination_path)))    

    copy_image(chosen_image_path)           # Copy and paste the chosen image
    keyboard.press_and_release('ctrl + v')

    logging.info('Successfully copy-pasted image \'%s\'', query)

    # Remove and recreate destination folder
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

            # Asks for the image search query
            print(f'Reading image name, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            clear_input_field()
            image_name = keystrokes_to_string(
                keystrokes).replace(submit_hotkey, '')

            logging.info("Searching for image: '%s'", image_name)

            # Download the image and copy paste it
            get_and_copy_image(image_name,
                               Settings.get_setting('image.pool_size'))
        except Exception:                                                       # pylint: disable=broad-except
            logging.error("Exception occurred in Image", exc_info=True)


if __name__ == '__main__':
    Settings.load_settings()
    listen_image()
