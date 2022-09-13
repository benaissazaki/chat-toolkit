''' Helper functions common to multiple modules '''

import os
import subprocess
from typing import List
import keyboard
import requests

def copy_file(file: str):
    ''' Copy file to clipboard (Windows only) '''

    abs_filename = os.path.abspath(file)
    cmd = f"Set-Clipboard -path {abs_filename}"
    try:
        subprocess.run(["powershell", "-command", cmd],
                   shell=True, check=True)  # windows specific
        return True
    except subprocess.CalledProcessError:
        print(f'Cannot copy file {file} to clipboard')
        return False

def keystrokes_to_string(keystrokes: List[keyboard.KeyboardEvent]) -> str:
    ''' Convert keystrokes to a string '''

    result = ''
    for keystroke in keystrokes:
        if keystroke.event_type == keyboard.KEY_DOWN:
            if keystroke.name == 'space':
                result += ' '
            elif keystroke.name == 'backspace':
                result = result[:-1]
            elif keystroke.name not in ['enter', 'esc']:
                result += keystroke.name

    return result

def check_internet_access():
    ''' Send get request to google to check internet access '''

    try:
        requests.get('https://www.google.com', timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False
