''' Helper functions common to multiple modules '''

from io import BytesIO
import os
import subprocess
import logging
from typing import List
from time import sleep
import keyboard
import requests
from PIL import Image
from win32 import win32clipboard
from settings import Settings


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
    except Exception as exception:                                                   # pylint: disable=broad-except
        print('Couldnt copy image to clipboard')
        print(exception)
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
    cursor = 0
    for keystroke in keystrokes:
        if keystroke.event_type == keyboard.KEY_DOWN:
            if keystroke.name == 'space':
                result = result[:cursor] + ' ' + result[cursor:]
                cursor += 1
            elif keystroke.name == 'backspace':
                result = result[:cursor-1] + result[cursor:]
                cursor -= 1
            elif keystroke.name in ['gauche', 'left']:
                cursor = cursor - 1 if cursor > 0 else cursor
            elif keystroke.name in ['droite', 'right']:
                cursor = cursor + 1 if cursor < len(result) else cursor
            elif keystroke.name not in ['enter', 'esc', 'maj', 'verr.maj']:
                result = result[:cursor] + keystroke.name + result[cursor:]
                cursor += 1
    return result


def check_internet_access():
    ''' Send get request to google to check internet access '''

    try:
        requests.get('https://www.google.com',
                     timeout=Settings.get_setting('request_timeout'))
        return True
    except requests.exceptions.RequestException:
        return False


def clear_input_field():
    ''' Clear the currently selected input field '''

    sleep(0.3)
    keyboard.press_and_release('ctrl + a')
    sleep(0.5)
    keyboard.press_and_release('backspace')


def configure_logging():
    ''' Configure the application's logging from Settings  '''

    logging_level = logging.getLevelName(Settings.get_setting('logging_level'))
    log_filename = Settings.get_setting('log_filename')
    log_format = Settings.get_setting('log_format')

    logging.basicConfig(level=logging_level, filename=log_filename, filemode='a', format=log_format)
