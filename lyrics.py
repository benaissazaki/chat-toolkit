''' Searches for song lyrics then types them in the keyboard '''

from time import sleep
import keyboard
from bs4 import BeautifulSoup
import requests

from helpers import keystrokes_to_string


def get_lyrics_link(query: str) -> str:
    ''' Get links to the @query song Genius lyrics page (takes first search result) '''

    results = list(requests.get(
        f"https://genius.com/api/search/multi?per_page=5&q={query}", timeout=2)
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


def listen_lyrics(hotkey: str = 'alt + 5'):
    ''' Main infinite loop '''

    while True:
        keyboard.wait(hotkey)
        keyboard.press_and_release('backspace')

        print('Reading song title for lyrics...')
        keystrokes = keyboard.record(until='enter')
        song_name = keystrokes_to_string(keystrokes)

        print(f"-Searching for song lyrics: {song_name}")
        lyrics = get_lyrics(song_name).split('\n')

        for line in lyrics:
            keyboard.write(line)
            keyboard.press_and_release('enter')
            sleep(0.4)

if __name__ == '__main__':
    listen_lyrics()
