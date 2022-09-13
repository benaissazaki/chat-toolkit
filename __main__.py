''' Launches all main loops in their own threads '''

import sys
from threading import Thread
import keyboard
from helpers import check_internet_access
from image import listen_image
from audio import listen_audio
from lyrics import listen_lyrics

if __name__ == '__main__':
    if not check_internet_access():
        print('No internet connection detected, program will close.')
        sys.exit(1)

    IMAGE_HOTKEY = 'alt + 4'
    AUDIO_HOTKEY = 'alt + 3'
    LYRICS_HOTKEY = 'alt + 5'

    EXIT_HOTKEY = 'alt + *'

    image_thread = Thread(target=listen_image, args=[IMAGE_HOTKEY], daemon=True)
    audio_thread = Thread(target=listen_audio, args=[AUDIO_HOTKEY], daemon=True)
    lyrics_thread = Thread(target=listen_lyrics, args=[LYRICS_HOTKEY], daemon=True)

    image_thread.start()
    audio_thread.start()
    lyrics_thread.start()

    print(f'Press {IMAGE_HOTKEY} to search and send an image')
    print(f'Press {AUDIO_HOTKEY} to search and send a song')
    print(f'Press {LYRICS_HOTKEY} to search and send a song\'s lyrics')

    print('\nAll systems are running.\n')

    print(f'Press {EXIT_HOTKEY} to exit')
    keyboard.wait(EXIT_HOTKEY)
