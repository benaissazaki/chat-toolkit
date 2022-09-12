''' Launches all main loops in their own threads '''

from threading import Thread
import keyboard
from image import listen_image
from audio import listen_audio
from lyrics import listen_lyrics

if __name__ == '__main__':
    image_thread = Thread(target=listen_image, daemon=True)
    audio_thread = Thread(target=listen_audio, daemon=True)
    lyrics_thread = Thread(target=listen_lyrics, daemon=True)

    image_thread.start()
    audio_thread.start()
    lyrics_thread.start()

    keyboard.wait('alt + *')
