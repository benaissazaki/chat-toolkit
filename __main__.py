''' Launches all main loops in their own threads '''

from json import JSONDecodeError
import sys
from threading import Thread
import keyboard
from helpers import check_internet_access
from image import listen_image
from audio import listen_audio
from lyrics import listen_lyrics
from settings import Settings

if __name__ == '__main__':
    if not check_internet_access():
        print('No internet connection detected, program will close.')
        sys.exit(1)


    try:
        Settings.load_settings()
    except FileNotFoundError:
        print('settings.json not found, will use default settings')
    except JSONDecodeError:
        print('Cannot decode settings.json, will use default settings')

    IMAGE_HOTKEY = Settings.get_setting('image.launch_hotkey')
    AUDIO_HOTKEY = Settings.get_setting('audio.launch_hotkey')
    LYRICS_HOTKEY = Settings.get_setting('lyrics.launch_hotkey')

    EXIT_HOTKEY = Settings.get_setting('exit_hotkey')

    image_thread = Thread(target=listen_image, args=[IMAGE_HOTKEY], daemon=True)
    audio_thread = Thread(target=listen_audio, args=[AUDIO_HOTKEY], daemon=True)
    lyrics_thread = Thread(target=listen_lyrics, args=[LYRICS_HOTKEY], daemon=True)

    if Settings.get_setting('image.api_key') is not None:
        image_thread.start()
        print(f'Press {IMAGE_HOTKEY} to search and send an image')
    else:
        print('image.api_key not found in settings.json, will not start the image module')

    audio_thread.start()
    lyrics_thread.start()

    print(f'Press {AUDIO_HOTKEY} to search and send a song')
    print(f'Press {LYRICS_HOTKEY} to search and send a song\'s lyrics')

    print(f'\nThe systems are running.\nPress {EXIT_HOTKEY} to exit')
    keyboard.wait(EXIT_HOTKEY)
