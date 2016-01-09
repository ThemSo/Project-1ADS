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
                addx = -gutter//2
            else:
                addx = 0

            if iy < (len(y)+1)//2:
                addy = -gutter//2
            else:
                addy = gutter//4
            draw_x = ((ix*height_square)+padding+addx)+round((height_square-30)/2)
            draw_y = ((iy*height_square)+padding+addy)+round((height_square-30)/2)

            screen.blit(img[x], (draw_x, draw_y))


running = True
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
gutter = 6
padding = 20
columns = 6
plateau = bases(columns)
animation = False

pygame.init()

screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
img = [pygame.image.load('img/0.png'), pygame.image.load('img/1.png'), pygame.image.load('img/2.png')]
pygame.display.set_caption('Pentago')
render()


# retourne la position du click tel que :
# pos = pos_click_plateau(mouse_pos)
# y = pos[0]
# x = pos[1]
# et donc :
# plateau[y][x]
# retourne la valeur de la case cliquée
def pos_click_plateau(pos):
    height = screen_size[1]
    height_cadrant = round((height-padding*2)/2)
    x, y = pos[0]-padding, pos[1]-padding
    height_square = round(((height-(padding*2)-gutter)/len(plateau)))
    if y >= height_cadrant-gutter/2:
        if height_cadrant+gutter/2 > y:
            y = -1
        else:
            y -= gutter//2

    if x >= height_cadrant-gutter/2:
        if height_cadrant+gutter/2 > x:
            x = -1
        else:
            x -= gutter//2
    x //= height_square
    y //= height_square
    if columns > x >= 0 and columns > y >= 0:
        return x, y
    return -1, -1

def player_pion(mouse_pos, player):
    pos = pos_click_plateau(mouse_pos)
    x = pos[0]
    y = pos[1]
    if plateau[y][x] == 0 and x != -1:
        plateau[y][x] = player
    render()


while running:
    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONUP:
        print(pos_click_plateau(pygame.mouse.get_pos()))
    if event.type == pygame.QUIT:
        running = False
    elif animation:
        render()
        clock.tick(60)

pygame.quit()
