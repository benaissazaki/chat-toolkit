''' Helper functions common to multiple modules '''

import subprocess

def copy_file(file: str):
    ''' Copy file to clipboard (Windows only) '''

    cmd = f"Set-Clipboard -path {file}"
    subprocess.run(["powershell", "-command", cmd], shell=True, check=True)  # windows specific
