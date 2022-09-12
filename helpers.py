from bs4 import BeautifulSoup
import requests
import subprocess

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


def copy_file(file):
    cmd = f"Set-Clipboard -path {file}"
    subprocess.run(["powershell", "-command", cmd], shell=True)  # windows specific


if __name__ == '__main__':
   print(get_lyrics('twice the feels'))
