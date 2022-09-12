''' Searches for song lyrics then types them in the keyboard '''

from time import sleep
import keyboard
from bs4 import BeautifulSoup
import requests


def get_lyrics_link(query: str) -> str:
    ''' Get links to the @query song Genius lyrics page (takes first search result) '''

    results = list(requests.get(
        f"https://genius.com/api/search/multi?per_page=5&q={query}", timeout=2000)
        .json()['response']['sections']
    )

    for result in results:
        if result['type'] == 'song':
            for hit in result['hits']:
                if hit['type'] == 'song':
                    return hit['result']['url']

    return None


def get_lyrics(query):
    ''' Get lyrics to @query song '''

    link = get_lyrics_link(query)
    page = requests.get(link, timeout=2000).text.replace('<i>', '').replace(
        '</i>', '').replace('<b>', '').replace('</b>', '')
    soup = BeautifulSoup(page, 'html.parser')
    raw_lyrics = soup.findAll('div', {'data-lyrics-container': 'true'})
    raw_lyrics = "".join([s.get_text('\n') for s in raw_lyrics])

    cleaned_lyrics = ''
    delete_mode = False

    for character in raw_lyrics:
        if character in ['[', '(']:
            delete_mode = True

        if character in [']', ')']:
            delete_mode = False

        if (character == '\n' and delete_mode):
            continue

        cleaned_lyrics += character

    return cleaned_lyrics


if __name__ == '__main__':
    while True:
        keyboard.wait('alt + 5')
        keyboard.press_and_release('backspace')
        print('Magic key pressed')
        recorded = keyboard.record(until='enter')
        SONG_NAME = ''
        for e in recorded:
            if e.event_type == keyboard.KEY_DOWN:
                if e.name == 'space':
                    SONG_NAME += ' '
                elif e.name == 'backspace':
                    SONG_NAME = SONG_NAME[:-1]
                elif e.name not in ['enter', 'esc']:
                    SONG_NAME += e.name

        print(f"-Searching for song: {SONG_NAME}")
        lyrics = get_lyrics(SONG_NAME).split('\n')

        for l in lyrics:
            keyboard.write(l)
            keyboard.press_and_release('enter')
            sleep(0.4)
