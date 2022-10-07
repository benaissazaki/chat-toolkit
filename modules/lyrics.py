''' Searches for song lyrics then types them in the keyboard '''

import logging
from time import sleep
import requests
import keyboard
from bs4 import BeautifulSoup
from helpers import keystrokes_to_string, clear_input_field
from settings import Settings


def get_lyrics_link(query: str) -> str:
    ''' Get links to the @query song's Genius lyrics page (takes first search result) '''

    try:
        response = requests.get(
            f"https://genius.com/api/search/multi?per_page=5&q={query}",
            timeout=Settings.get_setting('request_timeout')
        )
    except requests.exceptions.RequestException:
        logging.error('Cannot search lyrics from genius.com', exc_info=True)
        return None

    search_results = list(response.json()['response']['sections'])
    for result in search_results:
        if result['type'] == 'song' and len(result['hits']) > 0:
            for hit in result['hits']:
                if hit['type'] == 'song':
                    logging.info('Found lyrics in \'%s\'', hit['result']['url'])
                    return hit['result']['url']

    # If no result is found
    logging.info('No lyrics found in genius.com for \'%s\'', query)
    return None


def get_lyrics(query: str) -> str:
    ''' Get lyrics to @query song '''

    link_to_lyrics = get_lyrics_link(query)
    if link_to_lyrics is None:
        return None

    try:
        # Get lyrics page end remove <b> and <i> tags often present in lyrics themselves
        page = requests.get(link_to_lyrics, timeout=Settings.get_setting('request_timeout')) \
            .text.replace('<i>', '') \
            .replace('</i>', '').replace('<b>', '').replace('</b>', '')
    except requests.exceptions.RequestException:
        print(f'Cannot get lyrics page {link_to_lyrics}')
        return None

    soup = BeautifulSoup(page, 'html.parser')

    # Parse page to find lyrics
    raw_lyrics = soup.findAll('div', {'data-lyrics-container': 'true'})
    if len(raw_lyrics) == 0:
        print('Cannot parse lyrics page')
        return None
    raw_lyrics = "".join([s.get_text('\n') for s in raw_lyrics])
    cleaned_lyrics = clean_raw_lyrics(raw_lyrics)

    return cleaned_lyrics

def clean_raw_lyrics(raw_lyrics: str) -> str:
    ''' Nicely format raw_lyrics '''

    cleaned_lyrics = ''
    delete_linebreak_mode = False

    for character in raw_lyrics:
        if character == '[' and len(cleaned_lyrics) != 0 and cleaned_lyrics[-1] != '\n':
            # Add linebreak before '[' if it isn't there already
            cleaned_lyrics += '\n'

        if character in ['[', '(']:
            delete_linebreak_mode = True

        if character in [']', ')']:
            delete_linebreak_mode = False

        if (character == '\n' and delete_linebreak_mode):
            # Delete linebreaks between '()' and '[]'
            continue

        cleaned_lyrics += character

    return cleaned_lyrics


def listen_lyrics():
    ''' Main infinite loop '''

    # Load hotkeys from Settings
    launch_hotkey = Settings.get_setting('lyrics.launch_hotkey')
    submit_hotkey = Settings.get_setting('lyrics.submit_hotkey')

    while True:
        try:
            keyboard.wait(launch_hotkey)
            clear_input_field()
            logging.info('Summoned Lyrics')

            # Asks for the song title
            print(
                f'Reading song title for lyrics, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            clear_input_field()
            song_name = keystrokes_to_string(
                keystrokes).replace(submit_hotkey, '')

            logging.info("Searching for image: '%s'", song_name)
            lyrics = get_lyrics(song_name)
            if lyrics is None:
                continue

            # Type each line
            lyrics = lyrics.split('\n')
            for line in lyrics:
                keyboard.write(line)
                keyboard.press_and_release('enter')
                sleep(0.4)

            logging.info("Successfully typed the lyrics of '%s'", song_name)
        except Exception:                                                  # pylint: disable=broad-except
            logging.error("Exception occurred in Lyrics", exc_info=True)


if __name__ == '__main__':
    Settings.load_settings()
    listen_lyrics()
