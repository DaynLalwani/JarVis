# RUN THIS AND CLICK WIN + ENTER TO RUN JARVIS WHENEVER YOU WANT

import keyboard
import importlib


def run():
    import main
    importlib.reload(main)

keyboard.add_hotkey("ctrl+alt+j",run)

print("Backround Service Running . click WIN+enter to open Jarvis . Click Esc to close ...")

keyboard.wait("esc")
keyboard.unhook_all()
