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


def listen_audio():
    ''' Main infinite loop '''
    while True:
        keyboard.wait('alt + 3')
        keyboard.press_and_release('backspace')
        print('Reading song title...')
        keystrokes = keyboard.record(until='enter')
        song_name = ''
        for keystroke in keystrokes:
            if keystroke.event_type == keyboard.KEY_DOWN:
                if keystroke.name == 'space':
                    song_name += ' '
                elif keystroke.name == 'backspace':
                    song_name = song_name[:-1]
                elif keystroke.name not in ['enter', 'esc', 'maj', 'ctrl']:
                    song_name += keystroke.name

        print(f"Searching for song: {song_name}")
        download_audio(song_name)

        path = os.path.abspath(os.path.join('output', 'audio', 'tmp.mp3'))
        subprocess.Popen(f'explorer /select,"{path}"')

if __name__ == '__main__':
    listen_audio()
