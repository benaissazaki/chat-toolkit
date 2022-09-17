''' Send random jokes '''

import logging
from time import sleep
import requests
import keyboard
from settings import Settings


def get_random_joke():
    ''' Get a random joke from JokeAPI '''

    url = "https://v2.jokeapi.dev/joke/Any"

    querystring = {"format": "json", "blacklistFlags": "nsfw,explicit"}

    try:
        response = requests.get(
            url,
            params=querystring,
            timeout=Settings.get_setting('request_timeout'))
        response.raise_for_status()
        logging.info('Found joke')
        return response.json()
    except requests.exceptions.RequestException:
        logging.error('Cannot access JokeAPI', exc_info=True)
        return None


def type_joke(joke):
    ''' Type the joke into the keyboard '''

    keyboard.press_and_release('ctrl + a')
    keyboard.press_and_release('backspace')
    if joke['type'] == 'twopart':
        keyboard.write(joke['setup'])
        keyboard.press_and_release('enter')
        sleep(4)
        keyboard.write(joke['delivery'])
        keyboard.press_and_release('enter')
    else:
        keyboard.write(joke['joke'])
        keyboard.press_and_release('enter')

    logging.info('Finished typing joke')


def listen_jokes():
    ''' Main infinite loop '''

    launch_hotkey = Settings.get_setting('jokes.launch_hotkey')
    while True:
        try:
            keyboard.wait(launch_hotkey)
            logging.info('Summoned Jokes')
            logging.info('Sending random joke')
            joke = get_random_joke()

            if joke is not None:
                type_joke(joke)
        except Exception:                                                  # pylint: disable=broad-except
            logging.error("Exception occurred in Lyrics", exc_info=True)


if __name__ == '__main__':
    Settings.load_settings()
    listen_jokes()
