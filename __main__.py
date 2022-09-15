''' Launches all main loops in their own threads '''

import sys
from threading import Thread
from json import JSONDecodeError
from pathlib import Path
import keyboard
from helpers import check_internet_access
from image import listen_image
from audio import listen_audio
from lyrics import listen_lyrics
from jokes import listen_jokes
from settings import Settings

if __name__ == '__main__':
    if not check_internet_access():
        print('No internet connection detected, program will close.')
        sys.exit(1)

    print('Creating output folder...')
    Path('output/audio').mkdir(parents=True, exist_ok=True)
    Path('output/images').mkdir(parents=True, exist_ok=True)

    try:
        Settings.load_settings()
        print('Loading settings from settings.json\n')
    except FileNotFoundError:
        print('settings.json not found, will use default settings\n')
    except JSONDecodeError:
        print('Cannot decode settings.json, will use default settings\n')

    IMAGE_HOTKEY = Settings.get_setting('image.launch_hotkey')
    AUDIO_HOTKEY = Settings.get_setting('audio.launch_hotkey')
    LYRICS_HOTKEY = Settings.get_setting('lyrics.launch_hotkey')
    JOKES_HOTKEY = Settings.get_setting('jokes.launch_hotkey')

    EXIT_HOTKEY = Settings.get_setting('exit_hotkey')

    image_thread = Thread(target=listen_image, daemon=True)
    audio_thread = Thread(target=listen_audio, daemon=True)
    lyrics_thread = Thread(target=listen_lyrics, daemon=True)
    jokes_thread = Thread(target=listen_jokes, daemon=True)

    if Settings.get_setting('rapidapi_key') is not None:
        image_thread.start()
        print(f'Press {IMAGE_HOTKEY} to search and send an image')

        jokes_thread.start()
        print(f'Press {JOKES_HOTKEY} to send a random joke')
    else:
        print('rapidapi_key not found in settings.json, some modules won\'t start')

    audio_thread.start()
    lyrics_thread.start()

    print(f'Press {AUDIO_HOTKEY} to search and send a song')
    print(f'Press {LYRICS_HOTKEY} to search and send a song\'s lyrics')

    print(f'\nThe systems are running.\nPress {EXIT_HOTKEY} to exit\n')
    keyboard.wait(EXIT_HOTKEY)
