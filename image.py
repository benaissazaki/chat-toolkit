''' Downloads image then copy-pastes it '''

import os
from time import sleep
import requests
import keyboard
from helpers import copy_file, keystrokes_to_string

def get_image_link(query: str) -> str:
    ''' Searches for @query with Websearch API and returns the url of the first result '''

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

    querystring = {"q":query,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}

    headers = {
        "X-RapidAPI-Key": "40c9d9e5fdmshf9fb7e6826835fbp16a5bcjsn298d5e17cee1",
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=2)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException:
        print('Cannot access the Websearch API')
        return None
    link = response['value'][0]['url']
    return link

def save_image(link: str) -> str:
    ''' Downloads the image from @link and returns its filepath '''

    if link is None:
        print('Cannot download image')
        return None

    extension = 'jpg'
    with open(os.path.join('output', 'images', f'tmp_pic.{extension}'), 'wb') as handle:
        try:
            response = requests.get(link, stream=True, timeout=2)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            print('Cannot download image')
            return None

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    return os.path.join('output', 'images', f'tmp_pic.{extension}')


def listen_image(hotkey: str = 'alt + 4'):
    ''' Main infinite loop '''

    print(f'Enter \'{hotkey}\' to search for an image')
    while True:
        keyboard.wait(hotkey)
        keyboard.press_and_release('backspace')

        print('Reading image name...')
        keystrokes = keyboard.record(until='enter')
        image_name = keystrokes_to_string(keystrokes)

        print(f"Searching for image: {image_name}")

        filename = save_image(get_image_link(image_name))

        if filename is None:
            continue

        print(f'{image_name} image found')
        copy_file(filename)
        keyboard.press_and_release('ctrl + v')
        sleep(1)

if __name__ == '__main__':
    listen_image()
