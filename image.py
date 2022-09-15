''' Downloads image then copy-pastes it '''

import os
from typing import List
import requests
import keyboard
from helpers import copy_image, keystrokes_to_string
from settings import Settings


def get_image_link(query: str) -> str:
    ''' Searches for @query with Websearch API and returns the url of the first result '''

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

    querystring = {"q": query, "pageNumber": "1",
                   "pageSize": "10", "autoCorrect": "true"}

    headers = {
        "X-RapidAPI-Key": Settings.get_setting('image.api_key'),
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url,
                                headers=headers,
                                params=querystring,
                                timeout=Settings.get_setting('request_timeout'))
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException:
        print('Cannot access the Websearch API')
        return None
    links = [image['url'] for image in response['value']]
    return links


def save_image(links: List[str]) -> str:
    ''' Downloads the image from @link and returns its filepath '''

    if links is None:
        print('Cannot download image')
        return None

    extension = 'jpg'
    valid_image_found = False
    with open(os.path.join('output', 'images', f'tmp_pic.{extension}'), 'wb') as handle:
        for link in links:
            try:
                response = requests.get(link,
                                        stream=True,
                                        timeout=Settings.get_setting('request_timeout'))
                response.raise_for_status()
                valid_image_found = True
            except requests.exceptions.RequestException:
                print(f'Cannot download image {link}')
                continue

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
            break
    return os.path.join('output', 'images', f'tmp_pic.{extension}') if valid_image_found else None


def listen_image():
    ''' Main infinite loop '''

    launch_hotkey = Settings.get_setting('image.launch_hotkey')
    submit_hotkey = Settings.get_setting('image.submit_hotkey')
    while True:
        try:
            keyboard.wait(launch_hotkey)
            keyboard.press_and_release('backspace')

            print(f'Reading image name, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            image_name = keystrokes_to_string(keystrokes)

            print(f"Searching for image: {image_name}")

            filename = save_image(get_image_link(image_name))

            if filename is None:
                continue

            print(f'{image_name} image found')

            if not copy_image(filename):
                continue
            keyboard.press_and_release('ctrl + v')
        except Exception as exception:                                                  # pylint: disable=broad-except
            print(
                f'Unidentified error in listen_image: {type(exception).__name__}')
            print(exception)


if __name__ == '__main__':
    listen_image()
