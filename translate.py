''' Translate to any language on the fly using googletrans '''

from time import sleep
import keyboard
from googletrans import Translator
from settings import Settings
from helpers import keystrokes_to_string


def translate(language, text):
    ''' Translate @text to @language '''

    translator = Translator()

    try:
        translated = translator.translate(text, language).text
        return translated
    except Exception:                                                # pylint: disable=broad-except
        print('Cannot access Google translate')
        return None


def listen_translate():
    ''' Main infinite loop '''

    launch_hotkey = Settings.get_setting('translate.launch_hotkey')
    submit_language_hotkey = Settings.get_setting(
        'translate.submit_language_hotkey')
    submit_text_hotkey = Settings.get_setting('translate.submit_text_hotkey')

    while True:
        try:
            keyboard.wait(launch_hotkey)
            sleep(0.3)
            keyboard.press_and_release('ctrl + a')
            keyboard.press_and_release('backspace')

            print(
                f'Enter the destination language then press {submit_language_hotkey}')
            keystrokes = keyboard.record(until=submit_language_hotkey)
            keyboard.press_and_release('ctrl + a')
            sleep(0.5)
            keyboard.press_and_release('backspace')
            destination_language = keystrokes_to_string(
                keystrokes).replace(submit_language_hotkey, '')

            print(
                f'Enter the message you wish to translate the press {submit_text_hotkey}')
            keystrokes = keyboard.record(until=submit_text_hotkey)
            keyboard.press_and_release('ctrl + a')
            sleep(0.5)
            keyboard.press_and_release('backspace')
            text_to_translate = keystrokes_to_string(
                keystrokes).replace(submit_text_hotkey, '')

            translated = translate(destination_language, text_to_translate)

            if translated is not None:
                keyboard.write(translated)
                keyboard.press_and_release('enter')

        except Exception as exception:                                                  # pylint: disable=broad-except
            print(
                f'Unidentified error in listen_translate: {type(exception).__name__}')
            print(exception)


if __name__ == '__main__':
    Settings.load_settings()
    listen_translate()
