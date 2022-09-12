''' Downloads image then copy-pastes it '''

import os
from time import sleep
import requests
import keyboard
from helpers import copy_file

def get_image_link(query: str) -> str:
    ''' Searches for @query and returns the url of the first result '''

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

    querystring = {"q":query,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}

    headers = {
        "X-RapidAPI-Key": "40c9d9e5fdmshf9fb7e6826835fbp16a5bcjsn298d5e17cee1",
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=1000).json()
    link = response['value'][0]['url']
    return link

def save_image(link: str) -> str:
    ''' Downloads the image from @link and returns its filepath '''

    extension = 'jpg'
    with open(os.path.join('output', 'audio', f'tmp_pic.{extension}'), 'wb') as handle:
        response = requests.get(link, stream=True, timeout=1000)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    return os.path.join('output', 'audio', f'tmp_pic.{extension}')


if __name__ == '__main__':
    while True:
        keyboard.wait('alt + 4')
        keyboard.press_and_release('backspace')
        print('Magic key pressed')
        recorded = keyboard.record(until='enter')
        IMAGE_NAME = ''
        for e in recorded:
            if e.event_type == keyboard.KEY_DOWN:
                if e.name == 'space':
                    IMAGE_NAME += ' '
                elif e.name == 'backspace':
                    IMAGE_NAME = IMAGE_NAME[:-1]
                elif e.name not in ['enter', 'esc']:
                    IMAGE_NAME += e.name

        print(f"Searching for image: {IMAGE_NAME}")
        filename = save_image(get_image_link(IMAGE_NAME))
        copy_file(filename)
        keyboard.press_and_release('ctrl + v')
        sleep(1)
        keyboard.press('enter')
