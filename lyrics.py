from time import sleep
import keyboard
from helpers import get_lyrics

if __name__ == '__main__':
    while True:
        keyboard.wait('alt + 5')
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
                elif e.name not in ['enter', 'esc']:
                    song_name += e.name

        print(f"-Searching for song: {song_name}")
        lyrics = get_lyrics(song_name).split('\n')
        
        for l in lyrics:
            keyboard.write(l)
            keyboard.press_and_release('enter')
            sleep(0.4)
