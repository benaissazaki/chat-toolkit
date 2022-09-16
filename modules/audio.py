''' Downloads audio from Youtube video then opens the folder containing it'''

import subprocess
import os
import keyboard
import pytube
from moviepy.audio.io.AudioFileClip import AudioFileClip
from helpers import keystrokes_to_string, clear_input_field
from settings import Settings


def mp4_to_mp3(filename, output_path):
    ''' Convert mp4 video to mp3 audio '''

    try:
        video = AudioFileClip(filename)
        video.write_audiofile(output_path)
        video.close()
        os.remove(filename)
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


def listen_audio():
    ''' Main infinite loop '''

    launch_hotkey = Settings.get_setting('audio.launch_hotkey')
    submit_hotkey = Settings.get_setting('audio.submit_hotkey')
    while True:
        try:
            keyboard.wait(launch_hotkey)
            clear_input_field()

            print(f'Reading song title, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            clear_input_field()
            song_name = keystrokes_to_string(
                keystrokes).replace(submit_hotkey, '')

            print(f"Searching for song: {song_name}")
            audio_filepath = download_audio(song_name)
            if audio_filepath is not None:
                path = os.path.abspath(audio_filepath)
                subprocess.run(
                    f'explorer /select, "{path}"', check=False)
        except Exception as exception:                                                          # pylint: disable=broad-except
            print(
                f'Unidentified error in listen_audio: {type(exception).__name__}')
            print(exception)


if __name__ == '__main__':
    listen_audio()
