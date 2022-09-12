from time import sleep
import requests
import keyboard
import os
from helpers import copy_file

def get_image_link(query):
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

    querystring = {"q":query,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}

    headers = {
        "X-RapidAPI-Key": "40c9d9e5fdmshf9fb7e6826835fbp16a5bcjsn298d5e17cee1",
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    link = response['value'][0]['url']
    
    return link

def save_image(link: str):
    extension = 'jpg'
    with open(os.path.join('output', 'audio', f'tmp_pic.{extension}'), 'wb') as handle:
        response = requests.get(link, stream=True)

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
        image_name = ''
        for e in recorded:
            if e.event_type == keyboard.KEY_DOWN:
                if e.name == 'space':
                    image_name += ' '
                elif e.name == 'backspace':
                    image_name = image_name[:-1]
                elif e.name not in ['enter', 'esc']:
                    image_name += e.name
        
        print(f"Searching for image: {image_name}")
        filename = save_image(get_image_link(image_name))
        copy_file(filename)
        keyboard.press_and_release('ctrl + v')
        sleep(1)
        keyboard.press('enter')
        
