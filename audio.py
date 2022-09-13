''' Downloads audio from Youtube video then opens the folder containing it'''

import subprocess
import os
import keyboard
import pytube
import moviepy.editor as mp
from helpers import keystrokes_to_string


def mp4_to_mp3(filename, output_path):
    ''' Convert mp4 video to mp3 audio '''

    try:
        video = mp.AudioFileClip(filename)
        video.write_audiofile(output_path)
        video.close()
        return output_path

    except Exception:                               # pylint: disable=broad-except
        print('Cannot convert audio to mp3')
        return None


def download_audio(query):
    ''' Download first video matching @query then converts it to mp3 '''

    try:
        first_result: pytube.YouTube = pytube.Search(query).results[0]
        first_result.streams.filter(type='audio')[0].download(
            output_path=os.path.join('output', 'audio'), filename='tmp.mp4')
    except pytube.exceptions.PytubeError:
        print('Cannot download song from Youtube')
        return None

    result = mp4_to_mp3(os.path.join('output', 'audio', 'tmp.mp4'),
                        os.path.join('output', 'audio', 'tmp.mp3'))

    return result


def listen_audio(hotkey: str = 'alt + 3'):
    ''' Main infinite loop '''

    print(f'Enter \'{hotkey}\' to search for a song')
    while True:
        try:
            keyboard.wait(hotkey)
            keyboard.press_and_release('backspace')

            print('Reading song title...')
            keystrokes = keyboard.record(until='enter')
            song_name = keystrokes_to_string(keystrokes)

            print(f"Searching for song: {song_name}")
            audio_filepath = download_audio(song_name)
            if audio_filepath is not None:
                path = os.path.abspath(audio_filepath)
                subprocess.run(
                    f'explorer /select, "{path}\\haha"', check=False, capture_output=True)
        except Exception as exception:                                                          # pylint: disable=broad-except
            print(
                f'Unidentified error in listen_audio: {type(exception).__name__}')
            print(exception)


if __name__ == '__main__':
    listen_audio()
