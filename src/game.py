import os
import glob
import math
import random

import lib

from io import *

import pygame

from pygame.locals import *

HOME = os.path.expanduser("~")
SAVE = os.path.join(HOME, ".topdown")
SCREEN = pygame.display.set_mode((960, 540), 0, 32) # Assuming the display is 1920 x 1080
pygame.display.set_caption(HOME)

screens = {
        "menu": False,
        "game": False,
        "options": False
        }

def load_saveFile() -> TextIOWrapper:
    """
        load latest save file
    """
    files = []
    for n in glob.glob(SAVE):
        files.append(n)
    if files:
        return open(files[len(files)-1], 'r')

def make_saveFile() -> None:
    """
        Create a save file
    """
    save_files = []
    for n in os.path.walk(SAVE):
        save_files.append(n)
    file_save = str(len(save_files))+'.save'
    try:
        file = open(file_save, 'w')
    except PermissionError:
        raise PermissionError

def verify_save() -> bool:
    """
        Verify file location exists
    """
    try:
        return os.path.exists(SAVE)
    except PermissionError:
        raise PermissionError

def save() -> bool:
    """
        save game state
    """
    verify_save = False
    try:
        verify_save = verify_save()
    except PermissionError:
        return None
    if verify_save:
        # Saving
        pass
    else:
        make_saveFile()

def switch_context(ctx) -> dict:
    """
        ctx: Window context from __main__.screens
    """
    try:
        screens[ctx] = not screens[ctx]
    except KeyError:
        raise KeyError

def main():
    """
        Main loop - menu, options, game
    """

    global SCREEN

    tick = 0


    if screens['menu']:
        # Menu loop
        while 1:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    break
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        break
                    if ev.key == K_q:
                        break

if __name__ == "__main__":
    main()
