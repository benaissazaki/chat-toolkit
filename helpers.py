import subprocess

def copy_file(file):
    cmd = f"Set-Clipboard -path {file}"
    subprocess.run(["powershell", "-command", cmd], shell=True)  # windows specific
