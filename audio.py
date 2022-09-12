import subprocess
import os
import keyboard
import pytube
import moviepy.editor as mp

def mp4_to_mp3(filename, output_path):
    video = mp.AudioFileClip(filename)
    video.write_audiofile(output_path)
    video.close()

def download_audio(query):
    s: pytube.YouTube = pytube.Search(query).results[0]
    s.streams.filter(type='audio')[0].download(output_path=os.path.join('output', 'audio'), filename='tmp.mp4')
    mp4_to_mp3(os.path.join('output','audio', 'tmp.mp4'), os.path.join('output', 'audio', 'tmp.mp3'))
    

if __name__ == '__main__':
    while True:
        keyboard.wait('alt + 3')
        keyboard.press_and_release('backspace')
        print('Magic key pressed')
        recorded = keyboard.record(until='enter')
        song_name = ''
        for e in recorded:
            if e.event_type == keyboard.KEY_DOWN:
                if e.name == 'space':
                    song_name += ' '
                elif e.name == 'backspace':
                    song_name = song_name[:-1]
                elif e.name not in ['enter', 'esc', 'maj', 'ctrl']:
                    song_name += e.name
        
        print(f"Searching for song: {song_name}")
        download_audio(song_name)

        path = os.path.abspath(os.path.join('output', 'audio', 'tmp.mp3'))
        subprocess.Popen(f'explorer /select,"{path}"')

