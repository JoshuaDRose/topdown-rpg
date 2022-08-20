""" Game.py """
import os
import time
import glob
import math

from io import TextIOWrapper

import pygame

import lib

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

def load_save_file() -> TextIOWrapper:
    """
        load latest save file
    """
    files = []
    for _ in glob.glob(SAVE):
        files.append(_)
    with open(files[len(files) - 1], 'r') as file:
        return file

def make_save_file() -> None:
    """
        Create a save file
    """
    save_files = []
    for _ in os.path.abspath(SAVE):
        save_files.append(_)
    file_save = str(len(save_files)) + '.save'
    try:
        with open(file_save, 'w') as _:
            pass
    except PermissionError as exc:
        raise PermissionError from exc

def verify_save() -> bool:
    """
        Verify file location exists
    """
    try:
        if os.getcwd() == SAVE:
            return True
        return os.path.exists(SAVE)
    except PermissionError as exc:
        raise PermissionError from exc

def save() -> bool:
    """
        save game state
    """
    save_verified = verify_save()
    return save_verified

def switch_context(ctx):
    """
        ctx: Window context from __main__.screens
    """
    try:
        screens[ctx] = not screens[ctx]
    except KeyError as exc:
        raise KeyError from exc

def main():
    """
        Main loop - menu, options, game
    """

    mouse_visible = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(mouse_visible)
    cursor = lib.Cursor((SIZE[0] / 2, SIZE[1] / 2))
    level = lib.level.Level()

    if verify_save():
        switch_context("menu")

    if screens['menu']:
        running = True

        play_text_color = pygame.Color("grey")
        play_text = {"text": lib.h1("PLAY", (play_text_color))}
        play_text["rect"] = play_text["text"].get_rect(center=(SIZE[0] / 2, SIZE[1] / 2))
        delta_time = time.time()

        while running:
            delta_time = time.time()
            mouse_position = pygame.mouse.get_pos()
            SCREEN.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    cursor.mousepos = pygame.mouse.get_pos()
                    cursor.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_RETURN:
                        switch_context("game")
                        switch_context("menu")
                        running = False
                if play_text["rect"].collidepoint(mouse_position):
                    play_text_color = pygame.Color("white")
                    play_text["text"] = lib.h1("PLAY", play_text_color)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        switch_context("game")
                        switch_context("menu")
                        running = False
                else:
                    play_text_color = pygame.Color("grey")
                    play_text["text"] = lib.h1("PLAY", play_text_color)


            play_text["rect"].y = (SIZE[1] / 2 - play_text["text"].get_height() / 2) + math.sin(delta_time * 4) * 6
            SCREEN.blit(play_text["text"], play_text["rect"])
            SCREEN.blit(cursor.image, cursor.rect)

            pygame.display.update()
            clock.tick(60)

    if screens['game']:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    cursor.mousepos = pygame.mouse.get_pos()
                    cursor.update()
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            level.run()

            SCREEN.blit(cursor.image, cursor.rect)
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main()
