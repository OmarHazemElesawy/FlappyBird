import pygame
import sys
import random

pygame.mixer.pre_init(frequency=44100, size=16, channels=1)
pygame.init()
pygame.display.set_caption("Flappy bird")
icon = pygame.image.load("sprites/yellowbird-midflap.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19__.ttf", 35)
# game variables
gravity = 0.12
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("sprites/background-day.png").convert()

floor_surface = pygame.image.load("sprites/base.png").convert()
floor_x_pos = 0

bird_upflap = pygame.image.load("sprites/yellowbird-upflap.png").convert_alpha()
bird_midflap = pygame.image.load("sprites/yellowbird-midflap.png").convert_alpha()
bird_downflap = pygame.image.load("sprites/yellowbird-downflap.png").convert_alpha()
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("sprites/pipe-green.png").convert()
pipe_list = []
# TIMER
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 300, 300, 300, 400]
game_over_surface = pygame.image.load("sprites/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 256))

flap_sound = pygame.mixer.Sound("audio/wing.wav")
death_sound = pygame.mixer.Sound("audio/hit.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")
score_sound_countdown = 100


def score_display(game_state):
    if game_state == "main game":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score1, high_score1):
    if score1 > high_score1:
        high_score1 = score1
    return high_score1


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 10, 1)
    return new_bird


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3

    return pipes


def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe_rect = pipe_surface.get_rect(midtop=(320, random_pipe))
    top_pipe_rect = pipe_surface.get_rect(midbottom=(320, random_pipe - 150))
    return bottom_pipe_rect, top_pipe_rect


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    return True


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active is True:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display("main game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        high_score = update_score(score, high_score)
        score_display("game over")
        score = 0
        screen.blit(game_over_surface, game_over_rect)
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
