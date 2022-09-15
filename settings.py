''' Settings configuration '''

import json


class Settings():
    ''' Class that handles the settings '''

    settings_dict = {}
    default_settings = {
        'exit_hotkey': 'alt + *',
        'request_timeout': 5,
        'rapidapi_key': None,
        'image': {
            'launch_hotkey': 'alt + 4',
            'submit_hotkey': 'enter'
        },
        'lyrics': {
            'launch_hotkey': 'alt + 5',
            'submit_hotkey': 'enter'
        },
        'audio': {
            'launch_hotkey': 'alt + 3',
            'submit_hotkey': 'enter'
        },
        'jokes': {
            'launch_hotkey': 'alt + 2'
        },
        'translate': {
            'launch_hotkey': 'alt + t',
            'submit_language_hotkey': '<',
            'submit_text_hotkey': '<'
        }
    }

    @staticmethod
    def load_settings():
        ''' Load settings from settings.json file '''

        with open('settings.json', 'r', encoding='utf-8') as settings_file:
            Settings.settings_dict = json.load(settings_file)

    @staticmethod
    def get_setting(setting: str):
        '''
            Gets a setting from the dict or returns the default value.
                @setting is in the form "key.key.key" e.g: image.apikey
        '''
        setting = setting.split('.')
        result = Settings.settings_dict
        try:
            for key in setting:
                result = result[key]
        except KeyError:
            result = Settings.default_settings
            try:
                for key in setting:
                    result = result[key]
            except KeyError as exc:
                raise Exception(f'Setting {setting} does not exist') from exc

        return result
