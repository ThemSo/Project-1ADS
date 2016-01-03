import pygame


def bases(n):
    plateau = [[0 for i in range(n)] for i in range(n)]
    return plateau


def render():
    screen.fill(BLACK)
    draw_plateau(plateau, 6, 60)
    pygame.display.flip()


def draw_plateau(plateau, gutter, padding):
    height = screen_size[1]
    height_cadrant = (height-padding*2)//2
    pygame.draw.rect(screen, RED, (padding, padding, height_cadrant-(gutter//2), height_cadrant-(gutter//2)), 0)
    pygame.draw.rect(screen, RED, (padding+height_cadrant+(gutter//2), padding, height_cadrant-(gutter//2), height_cadrant-(gutter//2)), 0)
    pygame.draw.rect(screen, RED, (padding+height_cadrant+(gutter//2), padding+height_cadrant+(gutter//2), height_cadrant-(gutter//2), height_cadrant-(gutter//2)), 0)
    pygame.draw.rect(screen, RED, (padding, padding+height_cadrant+(gutter//2), height_cadrant-(gutter//2), height_cadrant-(gutter//2)), 0)
    height_square = round(((height-(padding*2))/len(plateau)))
    for iy, y in enumerate(plateau):
        for ix, x in enumerate(y):

            if ix < (len(y)+1)//2:
                addx = -gutter//4
            else:
                addx = gutter//4

            if iy < (len(y)+1)//2:
                addy = -gutter//4
            else:
                addy = gutter//4

            if x == 1:
                color = WHITE
            elif x == 2:
                color = BLACK
            else:
                color = DARK_RED

            pygame.draw.circle(screen, color, ((ix*height_square+height_square//2)+padding+addx, (iy*height_square+height_square//2)+padding+addy), height_square//4, 0)


def set_size(w, h):
    global screen_size, screen
    screen_size = (w, h)
    screen = pygame.display.set_mode(screen_size)


pygame.init()
set_size(700, 400)
running = True
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
plateau = bases(6)
pygame.display.set_caption('Pentago')

render()

while running:
    event = pygame.event.wait ()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.VIDEORESIZE:
        set_size(event.w, event.h)
        render()
pygame.quit ()