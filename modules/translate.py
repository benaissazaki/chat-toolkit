''' Translate to any language on the fly using googletrans '''

import logging
import keyboard
from googletrans import Translator
from settings import Settings
from helpers import clear_input_field, keystrokes_to_string


def translate(language, text):
    ''' Translate @text to @language '''

    translator = Translator()

    try:
        translated = translator.translate(text, language).text
        return translated
    except Exception:                                                   # pylint: disable=broad-except
        logging.error('Cannot access Google translate', exc_info=True)
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
            clear_input_field()
            logging.info('Summoned Translate')

            print(
                f'Enter the destination language then press {submit_language_hotkey}')
            keystrokes = keyboard.record(until=submit_language_hotkey)
            clear_input_field()

            destination_language = keystrokes_to_string(
                keystrokes).replace(submit_language_hotkey, '')
            logging.info('Destination language: \'%s\'', destination_language)

            print(
                f'Enter the message you wish to translate the press {submit_text_hotkey}')
            keystrokes = keyboard.record(until=submit_text_hotkey)
            clear_input_field()

            text_to_translate = keystrokes_to_string(
                keystrokes).replace(submit_text_hotkey, '')
            logging.info('Text to translate: \'%s\'', text_to_translate)

            translated = translate(destination_language, text_to_translate)

            if translated is not None:
                keyboard.write(translated)
                keyboard.press_and_release('enter')
                logging.info("Translation: '%s'", translated)

        except Exception:                                                  # pylint: disable=broad-except
            logging.error("Exception occurred in Translate", exc_info=True)


if __name__ == '__main__':
    Settings.load_settings()
    listen_translate()
