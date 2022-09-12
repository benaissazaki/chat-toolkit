''' Downloads audio from Youtube video then opens the folder containing it'''

import subprocess
import os
import keyboard
import pytube
import moviepy.editor as mp


def mp4_to_mp3(filename, output_path):
    ''' Convert mp4 video to mp3 audio '''
    video = mp.AudioFileClip(filename)
    video.write_audiofile(output_path)
    video.close()


def download_audio(query):
    ''' Download first video matching @query then converts it to mp3 '''
    first_result: pytube.YouTube = pytube.Search(query).results[0]
    first_result.streams.filter(type='audio')[0].download(
        output_path=os.path.join('output', 'audio'), filename='tmp.mp4')
    mp4_to_mp3(os.path.join('output', 'audio', 'tmp.mp4'),
               os.path.join('output', 'audio', 'tmp.mp3'))


if __name__ == '__main__':
    while True:
        keyboard.wait('alt + 3')
        keyboard.press_and_release('backspace')
        print('Magic key pressed')
        recorded = keyboard.record(until='enter')
        SONG_NAME = ''
        for e in recorded:
            if e.event_type == keyboard.KEY_DOWN:
                if e.name == 'space':
                    SONG_NAME += ' '
                elif e.name == 'backspace':
                    SONG_NAME = SONG_NAME[:-1]
                elif e.name not in ['enter', 'esc', 'maj', 'ctrl']:
                    SONG_NAME += e.name

        print(f"Searching for song: {SONG_NAME}")
        download_audio(SONG_NAME)

        path = os.path.abspath(os.path.join('output', 'audio', 'tmp.mp3'))
        subprocess.Popen(f'explorer /select,"{path}"')
