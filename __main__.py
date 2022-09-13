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

    image_thread = Thread(target=listen_image, daemon=True)
    audio_thread = Thread(target=listen_audio, daemon=True)
    lyrics_thread = Thread(target=listen_lyrics, daemon=True)

    image_thread.start()
    audio_thread.start()
    lyrics_thread.start()

    print('\nAll systems are running.\n')

    keyboard.wait('alt + *')
