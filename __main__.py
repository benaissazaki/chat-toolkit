''' Launches all main loops in their own threads '''

import sys
from threading import Thread
from json import JSONDecodeError
from pathlib import Path
import keyboard
from helpers import check_internet_access, configure_logging
from modules.image import listen_image
from modules.audio import listen_audio
from modules.lyrics import listen_lyrics
from modules.jokes import listen_jokes
from modules.translate import listen_translate
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

    configure_logging()

    IMAGE_HOTKEY = Settings.get_setting('image.launch_hotkey')
    AUDIO_HOTKEY = Settings.get_setting('audio.launch_hotkey')
    LYRICS_HOTKEY = Settings.get_setting('lyrics.launch_hotkey')
    JOKES_HOTKEY = Settings.get_setting('jokes.launch_hotkey')
    TRANSLATE_HOTKEY = Settings.get_setting('translate.launch_hotkey')

    EXIT_HOTKEY = Settings.get_setting('exit_hotkey')

    image_thread = Thread(target=listen_image, daemon=True)
    audio_thread = Thread(target=listen_audio, daemon=True)
    lyrics_thread = Thread(target=listen_lyrics, daemon=True)
    jokes_thread = Thread(target=listen_jokes, daemon=True)
    translate_thread = Thread(target=listen_translate, daemon=True)

    image_thread.start()
    audio_thread.start()
    lyrics_thread.start()
    jokes_thread.start()
    translate_thread.start()

    print(f'Press {IMAGE_HOTKEY} to search and send an image')
    print(f'Press {AUDIO_HOTKEY} to search and send a song')
    print(f'Press {LYRICS_HOTKEY} to search and send a song\'s lyrics')
    print(f'Press {JOKES_HOTKEY} to send a random joke')
    print(f'Press {TRANSLATE_HOTKEY} to send a translated message')

    print(f'\nThe systems are running.\nPress {EXIT_HOTKEY} to exit\n')
    keyboard.wait(EXIT_HOTKEY)
