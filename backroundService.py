# RUN THIS AND CLICK WIN + ENTER TO RUN JARVIS WHENEVER YOU WANT

import keyboard

def run():
    import main
keyboard.add_hotkey("win+enter",run)

print("Backround Service Running . click WIN+enter to open Jarvis . Click Esc to close ...")
keyboard.wait("esc")