from time import sleep
import keyboard
from bs4 import BeautifulSoup
import requests

def get_lyrics_link(query):
    res = list(requests.get(f"https://genius.com/api/search/multi?per_page=5&q={query}").json()['response']['sections'])
    
    for r in res:
        if r['type'] == 'song':
            for rr in r['hits']:
                if rr['type'] == 'song':
                    return rr['result']['url']

def get_lyrics(query):
    link = get_lyrics_link(query)
    page = requests.get(link).text.replace('<i>', '').replace('</i>', '').replace('<b>', '').replace('</b>', '')
    soup = BeautifulSoup(page, 'html.parser')
    lyrics = soup.findAll('div', {'data-lyrics-container': 'true'})
    lyrics = "".join([s.get_text('\n') for s in lyrics])
    result = ''
    delete_mode = False

    for c in lyrics:
        if c in ['[', '(']:
            delete_mode = True

        if c in [']', ')']:
            delete_mode = False

        if (c == '\n' and delete_mode):
            continue

        result += c

    return result


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
