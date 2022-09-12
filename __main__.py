''' Launches all main loops in their own threads '''

from threading import Thread
from image import listen_image
from audio import listen_audio
from lyrics import listen_lyrics

if __name__ == '__main__':
    image_thread = Thread(target=listen_image)
    audio_thread = Thread(target=listen_audio)
    lyrics_thread = Thread(target=listen_lyrics)

    image_thread.start()
    audio_thread.start()
    lyrics_thread.start()

    image_thread.join()
    audio_thread.join()
    lyrics_thread.join()
