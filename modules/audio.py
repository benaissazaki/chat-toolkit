''' Downloads audio from Youtube video then opens the folder containing it'''

import logging
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
        # Open the mp4 video's audio track
        video = AudioFileClip(filename)

        # Save video's audio track as mp3
        video.write_audiofile(output_path)
        video.close()

        # Remove mp4 video
        os.remove(filename)
        return output_path

    except Exception:                                           # pylint: disable=broad-except
        logging.error('Cannot convert %s to %s',
                      filename,
                      output_path,
                      exc_info=True)
        return None


def download_audio(query):
    ''' Download first video matching @query then converts it to mp3 '''

    try:
        # Download first youtube result and save it as tmp.mp4
        first_result: pytube.YouTube = pytube.Search(query).results[0]
        first_result.streams.filter(type='audio')[0].download(
            output_path=os.path.join('output', 'audio'), filename='tmp.mp4')
    except pytube.exceptions.PytubeError:
        logging.error('Cannot download %s from Youtube', query)
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
            logging.info('Summoned Audio')


            # Asks for song title
            print(f'Reading song title, press {submit_hotkey} to submit')
            keystrokes = keyboard.record(until=submit_hotkey)
            clear_input_field()
            song_name = keystrokes_to_string(
                keystrokes).replace(submit_hotkey, '')

            logging.info('Searching for song \'%s\'', song_name)

            audio_filepath = download_audio(song_name)
            if audio_filepath is not None:
                logging.info("Downloaded song '%s' in \'%s\'",
                             song_name,
                             audio_filepath)
                path = os.path.abspath(audio_filepath)

                # Open the folder containing the downloaded audio in file explorer
                subprocess.run(
                    f'explorer /select, "{path}"', check=False)

        except Exception:                                                          # pylint: disable=broad-except
            logging.error("Exception occurred in Audio", exc_info=True)


if __name__ == '__main__':
    Settings.load_settings()
    listen_audio()
