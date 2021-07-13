import pygame
import tetris.settings as settings
import tetris.gamemodes as gamemodes


pygame.init()

clock = pygame.time.Clock()
game_admin = gamemodes.GameMode

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption(settings.TITLE)

pygame.event.post(
    pygame.event.Event(pygame.USEREVENT, customType='tetris_mode'))

run = True

while run:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.USEREVENT:
            if event.customType == 'tetris_mode':
                game_admin = gamemodes.TetrisMode(screen, settings)

    game_admin.loop(events)

    pygame.display.update()

    clock.tick(settings.FPS)

pygame.quit()
