import pygame


def bases(n):
    plateau = [[0 for i in range(n)] for i in range(n)]
    return plateau


def render():
    screen.fill(BLACK)
    draw_plateau(plateau)
    pygame.display.flip()


def draw_plateau(plateau):
    height = screen_size[1]
    height_cadrant = round((height-padding*2)/2)
    mid_gutter = round(gutter/2)
    pygame.draw.rect(screen, RED, (padding, padding, height_cadrant-mid_gutter, height_cadrant-mid_gutter), 0)
    pygame.draw.rect(screen, RED, (padding+height_cadrant+mid_gutter, padding, height_cadrant-mid_gutter, height_cadrant-mid_gutter), 0)
    pygame.draw.rect(screen, RED, (padding+height_cadrant+mid_gutter, padding+height_cadrant+mid_gutter, height_cadrant-mid_gutter, height_cadrant-mid_gutter), 0)
    pygame.draw.rect(screen, RED, (padding, padding+height_cadrant+mid_gutter, height_cadrant-mid_gutter, height_cadrant-mid_gutter), 0)
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
            print(addy, addx)
            draw_x = ((ix*height_square)+padding+addx)+round((height_square-30)/2)
            draw_y = ((iy*height_square)+padding+addy)+round((height_square-30)/2)

            screen.blit(img[x], (draw_x, draw_y))


running = True
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
gutter = 4
padding = 60
plateau = bases(6)
plateau = [
	[0, 1, 1, 1, 0, 1],
	[1, 0, 0, 1, 2, 0],
	[0, 0, 0, 2, 1, 1],
	[1, 0, 1, 2, 1, 1],
	[1, 2, 2, 2, 0, 0],
	[0, 1, 1, 0, 1, 1],
]

pygame.init()

screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
img = [pygame.image.load('img/0.png'), pygame.image.load('img/1.png'), pygame.image.load('img/2.png')]
pygame.display.set_caption('Pentago')
render()

while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
pygame.quit()
