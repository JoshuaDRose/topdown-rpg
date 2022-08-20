import os
import time
import glob
import math
import random
import lib
import pygame

from io import *
from pygame.locals import *

pygame.display.init()

HOME = os.path.expanduser("~")
SAVE = os.path.join(HOME, "topdown-rpg")
SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(SIZE, 0, 32)

screens = {
        "menu":    False,
        "game":    False,
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
        return open(files[len(files) - 1], 'r')

def make_saveFile() -> None:
    """
        Create a save file
    """
    save_files = []
    for n in os.path.walk(SAVE):
        save_files.append(n)
    file_save = str(len(save_files)) + '.save'
    try:
        file = open(file_save, 'w')
    except PermissionError:
        raise PermissionError

def verify_save() -> bool:
    """
        Verify file location exists
    """
    try:
        if os.getcwd() == SAVE:
            return True
        else:
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
        pass
    else:
        make_saveFile()

def switch_context(ctx):
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

    mouse_visible = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(mouse_visible)
    cursor = lib.Cursor((SIZE[0] / 2, SIZE[1] / 2))

    level = lib.Level()
    if verify_save():
        switch_context("menu")

    game_tick = 0 # only increments in game loop

    if screens['menu']:
        running = True

        play_text_color = pygame.Color("grey")
        play_text = {"text": lib.h1("PLAY", (play_text_color))}
        play_text["rect"] = play_text["text"].get_rect(center=(SIZE[0] / 2, SIZE[1] / 2))
        play_text_colliding = False

        while running:
            mp = pygame.mouse.get_pos()
            SCREEN.fill((0, 0, 0))

            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False
                if ev.type == MOUSEMOTION:
                    cursor.mousepos = pygame.mouse.get_pos()
                    cursor.update()
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        running = False
                    if ev.key == K_q:
                        running = False
                    if ev.key == K_RETURN:
                        switch_context("game")
                        switch_context("menu")
                        running = False
                if play_text["rect"].collidepoint(mp):
                    play_text_color = pygame.Color("white")
                    play_text["text"] = lib.h1("PLAY", play_text_color)
                    play_text_colliding = True
                    if ev.type == MOUSEBUTTONDOWN:
                        switch_context("game")
                        switch_context("menu")
                        running = False
                else:
                    play_text_color = pygame.Color("grey")
                    play_text["text"] = lib.h1("PLAY", play_text_color)
                    play_text_colliding = False

            play_text["rect"].y = (SIZE[1] / 2 - play_text["text"].get_height() / 2) + math.sin(time.time() * 4) * 6

            SCREEN.blit(play_text["text"], play_text["rect"])
            SCREEN.blit(cursor.image, cursor.rect)

            pygame.display.update()
            clock.tick(60)

    if screens['game']:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    cursor.mousepos = pygame.mouse.get_pos()
                    cursor.update()
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False 

            level.run()

            SCREEN.blit(cursor.image, cursor.rect)

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main()
