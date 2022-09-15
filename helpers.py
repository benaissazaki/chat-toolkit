''' Helper functions common to multiple modules '''

from io import BytesIO
import os
import subprocess
from typing import List
import keyboard
import requests
from PIL import Image
from win32 import win32clipboard

def copy_image(file: str):
    ''' Copy image to the clipboard as bytes (Windows only) '''

    try:
        image = Image.open(file)
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        # pylint: disable=c-extension-no-member
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        # pylint: enable=c-extension-no-member

        return True
    except Exception:                                                   # pylint: disable=broad-except
        print('Couldnt copy image to clipboard')
        return False

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
