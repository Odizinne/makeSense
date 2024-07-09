import subprocess

def start_steam():
    subprocess.run(["steam.exe"], shell=True)
    print("Steam started")

start_steam()