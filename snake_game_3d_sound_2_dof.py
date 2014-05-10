import pygame
import random
from openal.audio import SoundSink, SoundSource, SoundListener
from openal.loaders import load_wav_file
from pygame.locals import QUIT, K_LEFT, K_RIGHT, KEYDOWN
import sys

__author__ = 'vamc'

#Initialize OpenAL related components
sound_sink = SoundSink()
sound_source = SoundSource()
listener = SoundListener()
sound_sink.activate()
sound_sink._listener = listener

source_sound_file = "asw.wav"
sound_data = load_wav_file(source_sound_file)
sound_source.queue(sound_data)
sound_source.looping = True

#initialize pygame and screen
pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0, 255, 0))
pygame.display.set_caption('Snake to the sound')

#Create Snake
snake_xpos = [300, 300, 300]
snake_ypos = [300, 290, 280]
snake_cell_size = 20
snake_image = pygame.Surface((snake_cell_size, snake_cell_size))
snake_image.fill((64, 0, 0))

#Create Apple
apple_size = 20
apple_pos = (random.randint(0, screen_width - apple_size), random.randint(0, screen_height - apple_size))
apple_image = pygame.Surface((apple_size, apple_size))
apple_image.fill((255, 0, 0))  # Apple should be red.

# Rationalize distance
new_xposition = lambda inp: (60.0 * inp)/screen_width
new_yposition = lambda inp: (60.0 * inp)/screen_height

sound_sink.play(sound_source)

#Heading direction of snake: 0: Up; 1: Right; 2: Down; 3: Left
snake_direction = 0  # Default

#Init clock
clock = pygame.time.Clock()

while True:
    clock.tick(5)  # Controls the speed of game. Increase to make snake run.
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)

        # Get pressed key and update snake's direction accordingly.
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if snake_direction == 0:
                    snake_direction = 1
                    listener.orientation = [1, 0, 0, 0, 1, 0]
                elif snake_direction == 1:
                    snake_direction = 2
                    listener.orientation = [0, 0, 1, 0, 1, 0]
                elif snake_direction == 2:
                    snake_direction = 3
                    listener.orientation = [-1, 0, 0, 0, 1, 0]
                elif snake_direction == 3:
                    snake_direction = 0
                    listener.orientation = [0, 0, -1, 0, 1, 0]

            if event.key == K_LEFT:
                if snake_direction == 0:
                    snake_direction = 3
                    listener.orientation = [-1, 0, 0, 0, 1, 0]
                elif snake_direction == 1:
                    snake_direction = 0
                    listener.orientation = [0, 0, -1, 0, 1, 0]
                elif snake_direction == 2:
                    snake_direction = 1
                    listener.orientation = [1, 0, 0, 0, 1, 0]
                elif snake_direction == 3:
                    snake_direction = 2
                    listener.orientation = [0, 0, 1, 0, 1, 0]

    # Find if snake touched apple
    if (snake_xpos[0] + snake_cell_size > apple_pos[0]) and (snake_xpos[0] < apple_pos[0] + apple_size) and \
       (snake_ypos[0] + snake_cell_size > apple_pos[1]) and (snake_ypos[0] < apple_pos[1] + apple_size):
        # Place a new apple somewhere.
        apple_pos = (random.randint(0, screen_width - apple_size), random.randint(0, screen_height - apple_size))

        sound_source.position = (new_xposition(apple_pos[0]), 0, new_yposition(apple_pos[1]))

        # Snake's size should increase. Add some garbage element to snake_xpos and snake_ypos.
        # This cell would be placed at it's respective position later.
        snake_xpos.append(404)
        snake_ypos.append(404)

    # # Update position of snake's tail.
    # # Each cell should take position of cell in front of it.
    index = len(snake_xpos) - 1
    while index > 0:
        snake_xpos[index] = snake_xpos[index - 1]
        snake_ypos[index] = snake_ypos[index - 1]
        index -= 1

    # Update position of snake's head.
    if snake_direction == 0:
        snake_ypos[0] -= snake_cell_size
    if snake_direction == 1:
        snake_xpos[0] += snake_cell_size
    if snake_direction == 2:
        snake_ypos[0] += snake_cell_size
    if snake_direction == 3:
        snake_xpos[0] -= snake_cell_size

    if snake_xpos[0] < 0:
        snake_xpos[0] = screen_width
    if snake_xpos[0] > screen_width:
        snake_xpos[0] = 0

    if snake_ypos[0] < 0:
        snake_ypos[0] = screen_height
    if snake_ypos[0] > screen_height:
        snake_ypos[0] = 0

    listener.position = (new_xposition(snake_xpos[0]), 0, new_yposition(snake_ypos[0]))

    # Render image of apple and snake on screen
    screen.fill((0, 255, 0))
    screen.blit(apple_image, apple_pos)
    for (x, y) in zip(snake_xpos, snake_ypos):
        screen.blit(snake_image, (x, y))

    print sound_source.position, listener.position
    sound_sink.update()
    pygame.display.update()