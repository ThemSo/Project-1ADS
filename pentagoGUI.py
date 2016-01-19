import pygame
import os.path
import math
import json
import time


# retourne une liste bi-dimensionnelle de n*n
def bases(n):
    tmp = [[0 for i in range(n)] for i in range(n)]
    return tmp


# rassemble les fonctions qui affichent des choses à l'écran
def render(rotation):

    # dessine le fond noir
    screen.fill(BLACK)

    # si le joueur doit tourner un plateau, affiche les flêches
    if STEP == 2:
        draw_arrow()

    # dessin du plateau
    draw_plateau(plateau, rotation)

    # indique le nom du joueur devant jouer
    draw_turn_player()

    # dessine le pion à poser
    if STEP == 1 and not animation:
        screen.blit(img[PLAYER], pygame.rect.Rect(
            mouse_pos[0] - 15, mouse_pos[1] - 15, 30, 30))

    if animation and STEP == 3:
        draw_win(win_top)

    # dessin de l'interface
    draw_interface()

    # actualisation de la fenêtre
    pygame.display.flip()


# retourne True si une condition de victoire est détectée horizontalement
# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2
def victory_horizontal(n, l, p, j):
    for y in range(n):
        v = 0
        for x in range(n):
            if l[y][x] == j:
                v += 1
            else:
                v = 0
            if v >= p:
                return True
    return False


# retourne True si une condition de victoire est détectée verticalement
# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2
def victory_vertical(n, l, p, j):
    for x in range(n):
        v = 0
        for y in range(n):
            if l[y][x] == j:
                v += 1
            else:
                v = 0
            if v >= p:
                return True
    return False


# retourne True si une condition de victoire est détectée en diagonal : /
# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2
def victory_diagonal1(n, l, p, j):
    for i in range(n * 2):
        x, y, v = i, 0, 0
        while x >= 0 and y < n:
            if n > y >= 0 and n > x >= 0:
                if l[y][x] == j:
                    v += 1
                else:
                    v = 0
                if v >= p:
                    return True
            x -= 1
            y += 1
    return False


# retourne True si une condition de victoire est détectée en diagonal : \
# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2
def victory_diagonal2(n, l, p, j):
    for i in range(n * 2):
        x, y, v = i, n - 1, 0
        while x >= 0 and y >= 0:
            if n > y >= 0 and n > x >= 0:
                if l[y][x] == j:
                    v += 1
                else:
                    v = 0
                if v >= p:
                    return True
            x -= 1
            y -= 1
    return False


# retourne True si au moins une condition de victoire est détectée
# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2
def test_win(n, l, p, j):
    global STEP
    # test de toutes les conditions de victoire
    if victory_horizontal(n, l, p, j) or victory_vertical(n, l, p, j) or victory_diagonal1(n, l, p, j) or victory_diagonal2(n, l, p, j):
        # en cas de victoire:
        STEP = 3
        # réinitialise la sauvegarde
        file = open("cache", "w")
        file.write("")
        file.close()

        # lancement du son de victoire
        sound[1].play()

        # lancement de l'animation de victoire
        animate_win()

        # réinitialisation de la taille du plateau si elle n'est pas correct
        if padding > padding_step_1:
            resize_plateau(time.time() * 1000,
                           padding_step_1 - padding_step_2, 600)
        return True
    elif test_match_nul(l):
        STEP = 3

        # réinitialise la sauvegarde
        file = open("cache", "w")
        file.write("")
        file.close()

        if padding > padding_step_1:
            resize_plateau(time.time() * 1000,
                           padding_step_1 - padding_step_2, 600)
        return True
    return False


# test si match nul
# l = (list) plateau
def test_match_nul(l):
    # si aucuns des éléments du plateau ne vaut "0", return False
    for y in range(len(l)):
        for x in range(len(l)):
            if l[y][x] == 0:
                return False
    # sinon
    return True


# numéros des cotés :
#  ___
# |1|3|
# |2|4|
#  ---
#
# rotation d'un plateau
# rotation_plateau(liste, nombre_de_ligne, numero_du_cote, True = horaire
# et False = antihoraire)
def rotation_plateau(plateau_tmp, m, n, sens):
    x, y, maxx, maxy = 0, 0, m // 2, m // 2
    # récuperation du morceau du plateau contenant le cadrant à tourner dans
    # une liste temporaire,
    if n % 2 == 0:
        x = m // 2
        maxx = m
    if n > 2:
        y = m // 2
        maxy = m
    tmp = [[0 for i in range(m // 2)] for i in range(m // 2)]

    # lecture de la liste temporaire dans un autre sens
    tmpy = maxy
    while tmpy > y:
        tmpx = maxx
        while tmpx > x:
            if not sens:
                tmp[maxy - tmpy][tmpx - x -
                                 1] = plateau_tmp[tmpx - 1][tmpy - 1]
            else:
                tmp[tmpy - y - 1][maxx -
                                  tmpx] = plateau_tmp[tmpx - 1][tmpy - 1]
            tmpx -= 1
        tmpy -= 1

    # réinsertion de la liste temporaire dans la liste "plateau" principale
    for nx, vx in enumerate(tmp):
        for ny, vy in enumerate(vx):
            plateau_tmp[nx + x][ny + y] = vy

    # retourne il liste contenant le plateau après rotation d'un cadrant
    return plateau_tmp


# dessine les flèches permettant la rotation d'un cadrant
def draw_arrow():
    height = screen_size[1] - (padding_step_2 * 2)
    screen.blit(img_arrow, (padding_step_2, padding_step_2 - 30))
    screen.blit(pygame.transform.flip(img_arrow, True, False),
                (padding_step_2 - 30 + height, padding_step_2 - 30))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(
        img_arrow, 90), True, True), (padding_step_2 + height, padding_step_2))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(img_arrow, 90),
                                      True, False), (padding_step_2 + height, padding_step_2 + height - 30))
    screen.blit(pygame.transform.flip(img_arrow, True, True),
                (padding_step_2 + height - 30, padding_step_2 + height))
    screen.blit(pygame.transform.flip(img_arrow, False, True),
                (padding_step_2, padding_step_2 + height))
    screen.blit(pygame.transform.rotate(img_arrow, 90),
                (padding_step_2 - 30, padding_step_2 + height - 30))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(
        img_arrow, 90), False, True), (padding_step_2 - 30, padding_step_2))


# tourne un cadrant lors d'un clique sur une flèche
def click_arrows(mouse_pos):
    global plateau
    global columns
    global STEP
    global PLAYER
    height = screen_size[1] - (padding_step_2 * 2)
    x, y = mouse_pos[0], mouse_pos[1]
    action = False
    rotation = False
    cadrant = 1

    # détection des cliques sur les flêches
    if padding_step_2 + 30 >= x >= padding_step_2 >= y >= padding_step_2 - 30:
        cadrant = 1
        rotation = True
        action = True
    elif padding_step_2 + height >= x >= padding_step_2 + height - 30 \
            and padding_step_2 >= y >= padding_step_2 - 30:
        cadrant = 3
        action = True
    elif padding_step_2 + height + 30 >= x >= padding_step_2 + height \
            and padding_step_2 + 30 >= y >= padding_step_2:
        cadrant = 3
        rotation = True
        action = True
    elif padding_step_2 + height + 30 >= x >= padding_step_2 + \
            height >= y >= padding_step_2 + height - 30:
        cadrant = 4
        action = True
    elif padding_step_2 + height + 30 >= y >= padding_step_2 + \
            height >= x >= padding_step_2 + height - 30:
        cadrant = 4
        rotation = True
        action = True
    elif padding_step_2 + 30 >= x >= padding_step_2 and \
            padding_step_2 + height + 30 >= y >= padding_step_2 + height:
        cadrant = 2
        action = True
    elif padding_step_2 >= x >= padding_step_2 - 30 and \
            padding_step_2 + height >= y >= padding_step_2 + height - 30:
        cadrant = 2
        rotation = True
        action = True
    elif padding_step_2 + 30 >= y >= padding_step_2 \
            >= x >= padding_step_2 - 30:
        cadrant = 1
        rotation = False
        action = True

    # si une flêche à été cliquée
    if action:
        sound[0].play()
        render((0, 0))
        STEP = 1
        if rotation:
            angle = 90
        else:
            angle = -90

        # lancement de l'animation de rotation du cadrant
        rotate_cadrant(time.time() * 1000, cadrant, angle, 1000)

        # rotation du cadrant dans la list "plateau"
        plateau = rotation_plateau(plateau, columns, cadrant, rotation)

        # lancement de l'animation de redimensionnement du plateau
        resize_plateau(time.time() * 1000,
                       padding_step_1 - padding_step_2, 600)

        # détection de victoire
        if not test_win(columns, plateau, nb_pions, PLAYER):
            # passage au tour suivant et sauvegarde du jeu
            PLAYER = 1 if PLAYER == 2 else 2
            save()


# retourne la position d'un point après rotation
# cx = (int) position en x de l'axe de rotation
# cy = (int) position en y de l'axe de rotation
# x et y = (int) position en x et y du point avant rotation
# angle = (int) angle de la rotation en degrés
def point_rotate(cx, cy, x, y, angle):
    radians = (math.pi / 180) * -angle
    cos = math.cos(radians)
    sin = math.sin(radians)
    nx = (cos * (x - cx)) + (sin * (y - cy)) + cx
    ny = (cos * (y - cy)) - (sin * (x - cx)) + cy
    return nx, ny


# dessine le plateau
# plateau = (list) list contenant les éléments du plateau
# rotate = (tuple) cadrant à tourner lors d'une animation: (nb_cadrant,
# angle_en_degres)
def draw_plateau(plateau, rotate):
    # dessin des cadrants
    height = screen_size[1]
    height_cadrant = round((height - padding * 2) / 2)
    mid_GUTTER = round(GUTTER / 2)

    if rotate[0] == 1 and rotate[1] != 0:
        cx, cy = padding + ((height_cadrant - mid_GUTTER) //
                            2), padding + ((height_cadrant - mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant -
                         mid_GUTTER, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant - mid_GUTTER,
                         padding + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding, padding +
                         height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding, padding),
            (padding + height_cadrant - mid_GUTTER, padding),
            (padding + height_cadrant - mid_GUTTER,
             padding + height_cadrant - mid_GUTTER),
            (padding, padding + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    if rotate[0] == 3 and rotate[1] != 0:
        cx, cy = padding + height_cadrant + \
            ((height_cadrant + mid_GUTTER) // 2), padding + \
            ((height_cadrant - mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding + height_cadrant +
                         mid_GUTTER, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant +
                         height_cadrant, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + height_cadrant,
                         padding + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER,
                         padding + height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding + height_cadrant + mid_GUTTER, padding),
            (padding + height_cadrant + mid_GUTTER +
             height_cadrant - mid_GUTTER, padding),
            (padding + height_cadrant + mid_GUTTER + height_cadrant -
             mid_GUTTER, padding + height_cadrant - mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER,
             padding + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    if rotate[0] == 4 and rotate[1] != 0:
        cx, cy = padding + height_cadrant + \
            ((height_cadrant + mid_GUTTER) // 2), padding + \
            height_cadrant + ((height_cadrant + mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER,
                         padding + height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER + height_cadrant -
                         mid_GUTTER, padding + height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER,
                         padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER, padding +
                         height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding + height_cadrant + mid_GUTTER,
             padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER + height_cadrant -
             mid_GUTTER, padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER,
             padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER, padding +
             height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    if rotate[0] == 2 and rotate[1] != 0:
        cx, cy = padding + ((height_cadrant - mid_GUTTER) // 2), padding + \
            height_cadrant + ((height_cadrant + mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding, padding +
                         height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant - mid_GUTTER,
                         padding + height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant - mid_GUTTER, padding +
                         height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding, padding + height_cadrant +
                         mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding, padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant - mid_GUTTER,
             padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant - mid_GUTTER, padding +
             height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER),
            (padding, padding + height_cadrant +
             mid_GUTTER + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    # dessin des pions sur les cadrants
    height_square = ((height - (padding * 2)) / len(plateau))
    for iy, y in enumerate(plateau):
        for ix, x in enumerate(y):

            if ix < (len(y) + 1) // 2:
                addx = -GUTTER // 4
            else:
                addx = GUTTER // 4

            if iy < (len(y) + 1) // 2:
                addy = -GUTTER // 4
            else:
                addy = GUTTER // 4

            draw_x = ((ix * height_square) + padding + addx) + \
                (height_square - 30) / 2
            draw_y = ((iy * height_square) + padding + addy) + \
                (height_square - 30) / 2

            # en cas de rotation d'un cadrant
            if rotate[1] != 0 and rotate[0] != 0:
                pos_pion = 1
                #  ___
                # |1|3|
                # |2|4|
                #  ---
                if ix >= (len(y) + 1) // 2:
                    pos_pion += 2
                if iy >= (len(y) + 1) // 2:
                    pos_pion += 1

                # si le cadrant actuel possède un angle
                if pos_pion == rotate[0]:

                    # réassigne la position des pions en fonction de l'angle
                    new_pos_pion = point_rotate(
                        cx, cy, draw_x + 15, draw_y + 15, rotate[1])
                    draw_x = new_pos_pion[0] - 15
                    draw_y = new_pos_pion[1] - 15

            screen.blit(img[x], (draw_x, draw_y))


# retourne la position du click tel que :
# pos = pos_click_plateau(mouse_pos)
# y = pos[0]
# x = pos[1]
# et donc :
# plateau[y][x]
# retourne la valeur de la case cliquée
def pos_click_plateau(pos):
    height = screen_size[1]
    height_cadrant = round((height - padding * 2) / 2)
    x, y = pos[0] - padding, pos[1] - padding
    height_square = round(((height - (padding * 2) - GUTTER) / len(plateau)))
    if y >= height_cadrant - GUTTER / 2:
        if height_cadrant + GUTTER / 2 > y:
            y = -1
        else:
            y -= GUTTER // 2

    if x >= height_cadrant - GUTTER / 2:
        if height_cadrant + GUTTER / 2 > x:
            x = -1
        else:
            x -= GUTTER // 2
    x //= height_square
    y //= height_square
    if columns > x >= 0 and columns > y >= 0:
        return round(x), round(y)
    return -1, -1


# animation du redimensionnement du plateau
# start = (int) timestamp en millisecondes du lancement de l'animation
# end_value = (int) valeur finale de padding
# duration = (int) durée de l'animation en millisecondes
def resize_plateau(start, end_value, duration):
    global padding
    global animation
    global mouse_pos

    # réassigne la variable "mouse_pos" pour ne pas afficher le pion à
    # afficher à la fin de l'animation
    mouse_pos = (-100, -100)

    # valeur de départ
    start_value = padding

    # temps actuel dans l'animation
    current_time = time.time() * 1000

    # bloque la boucle de rendu classique
    animation = True
    while current_time - start <= duration:

        # actualisation du temps actuel
        current_time = time.time() * 1000

        # dessin du jeu en fonction du nouveau padding
        padding = round(ease(current_time - start,
                             start_value, end_value, duration))
        render((0, 0))

    # réactive la boucle de rendu normale
    animation = False


# animation de la rotation des cadrants
# start = (int) timestamp en millisecondes du lancement de l'animation
# cadrant = (int entre 1 et 4) numéro du cadrant
# end_value = (int) valeur finale de padding
# duration = (int) durée de l'animation en millisecondes
def rotate_cadrant(start, cadrant, end_value, duration):
    global padding
    global animation
    global mouse_pos

    # réassigne la variable "mouse_pos" pour ne pas afficher le pion à
    # afficher à la fin de l'animation
    mouse_pos = (-100, -100)

    # valeur de départ
    start_value = 0

    # temps actuel dans l'animation
    current_time = time.time() * 1000
    animation = True

    # temps que le temps de l'animation n'est pas écoulé
    while current_time - start <= duration:
        # actualisation du temps actuel
        current_time = time.time() * 1000

        # dessin du jeu en fonction de l'angle de rotation d'un cadrant
        render(
            (cadrant, round(ease(current_time - start, start_value, end_value, duration))))

    # réactive la boucle de rendu normale
    animation = False


# retourne une valeur sur une courbe en demi-cloche,
#     en fonction du temps écoulé et de deux valeurs:
# t = (int) temps actuel
# b = (number) valeur de depart
# c = (number) valeur finale
# d = (number) durée
def ease(t, b, c, d):
    t = t / d - 1
    return c * (t * t * t + 1) + b


# sauvegarde la partie en cours dans le fichier "cache", en JSON
def save():
    # ouverture du fichier "cache" en écriture
    file = open("cache", "w")
    # declaration d'un dictionnaire contenant les données du jeu en cours
    data = {'plateau': plateau, 'step': STEP, 'player': PLAYER,
            'columns': columns, 'nb_pions': nb_pions}
    # écrit les données, parsées en JSON
    file.write(json.dumps(data))
    file.close()


# charge une partie en cours à partir du fichier "cache"
def load():
    global PLAYER
    global plateau
    global STEP
    global columns
    global new_columns
    global nb_pions
    global new_nb_pions

    # si le fichier de sauvegarde existe
    if os.path.isfile("cache"):

        # lecture du fichier de sauvegarde
        file = open("cache", "r")
        data = file.read()

        # si le fichier n'est pas vide
        if data != '':

            # Parsing du fichier JSON
            data = json.loads(data)

            # si les données sauvegardée sont corrects
            if 'player' in data and data['player'] != '':
                if 'step' in data and data['step'] != '' and 'nb_pions' in data and data['nb_pions'] != '':
                    if 'plateau' in data and data['plateau'] != '' and 'columns' in data and data['columns'] != '':
                        # réinitialisation des variables
                        STEP = data['step']
                        PLAYER = data['player']
                        plateau = data['plateau']
                        columns = data['columns']
                        nb_pions = data['nb_pions']
                        new_columns = columns
                        new_nb_pions = nb_pions
        file.close()


# relance une nouvelle partie
def new_game():
    global PLAYER
    global plateau
    global STEP
    global columns
    global nb_pions

    # réinitialise le fichier "cache"
    file = open("cache", "w")
    file.write("")
    file.close()

    # réinitialise le joueur, l'étape du jeu, et le plateau
    STEP = 1
    PLAYER = 1 if PLAYER == 2 else 2
    columns = new_columns
    nb_pions = new_nb_pions
    plateau = bases(new_columns)
    render((0, 0))

    # redimensionne la taille du plateau si besoin
    if padding != padding_step_1:
        resize_plateau(time.time() * 1000,
                       padding_step_1 - padding_step_2, 600)


# pose un pion sur le plateau
# mouse_pos = (tuple) position en x et y de la souris tel que (x, y)
# player = (1 ou 2) identifiant du joueur
def pose_pion(mouse_pos, player):
    pos = pos_click_plateau(mouse_pos)
    x = pos[0]
    y = pos[1]
    if plateau[y][x] == 0 and x != -1:
        global STEP
        sound[0].play()
        plateau[y][x] = player
        if not test_win(columns, plateau, nb_pions, player):
            STEP = 2
            resize_plateau(time.time() * 1000,
                           padding_step_2 - padding_step_1, 600)
            save()


# dessine l'interface de parametrage de parties
def draw_interface():
    if screen_size[1] <= mouse_pos[0] <= screen_size[1] + 250 - padding_step_1 and padding_step_1 * 4 + 51 + 128 + 85 <= mouse_pos[1] <= padding_step_1 * 4 + 51 + 128 + 85 + 45:
        screen.blit(img_button_reset[1], (screen_size[
            1], padding_step_1 * 4 + 51 + 128 + 85))
    else:
        screen.blit(img_button_reset[0], (screen_size[
            1], padding_step_1 * 4 + 51 + 128 + 85))

    screen.blit(img_interface[0], (screen_size[1], padding_step_1 * 2 + 51))
    screen.blit(img_interface[1], (screen_size[1],
                                   padding_step_1 * 3 + 51 + 128))

    # nombre de colonnes (texte)
    font = pygame.font.Font(None, 40)
    color_active = (255, 255, 255)
    color_inactive = (100, 100, 100)

    color = color_active if new_columns == 4 else color_inactive
    text = font.render("4", 1, color)
    screen.blit(text, (screen_size[1]+32, 140))

    color = color_active if new_columns == 6 else color_inactive
    text = font.render("6", 1, color)
    screen.blit(text, (screen_size[1]+111, 140))

    color = color_active if new_columns == 8 else color_inactive
    text = font.render("8", 1, color)
    screen.blit(text, (screen_size[1]+192, 140))

    # nombre de pions à aligner (texte)
    draw_nb_pions()


def draw_nb_pions():
    font = pygame.font.Font(None, 30)
    color_active = (255, 255, 255)
    color_inactive = (100, 100, 100)
    color_forbidden = (50, 50, 50)
    for i in range(3,9):
        if new_nb_pions == i:
            color = color_active
        elif i > new_columns:
            color = color_forbidden
        else:
            color = color_inactive
        text = font.render(str(i), 1, color)
        screen.blit(text, (screen_size[1]+15+(40*(i-3)), 257))


# detection du clique sur l'interface
def click_interface(mouse_pos):
    global new_columns
    global new_nb_pions
    if screen_size[1] <= mouse_pos[0] <= screen_size[1] + 250 - padding_step_1:
        if 114 <= mouse_pos[1] <= 191:
            if mouse_pos[0] <= screen_size[1] + 79:
                new_columns = 4
            elif mouse_pos[0] <= screen_size[1] + 160:
                new_columns = 6
            else:
                new_columns = 8
        if 248 <= mouse_pos[1] <= 284:
            new_nb_pions = ((mouse_pos[0]-screen_size[1]-(padding_step_1))//((250 - padding_step_1- padding_step_1)//6))+3
        if new_nb_pions > new_columns:
                new_nb_pions = new_columns
        if padding_step_1 * 4 + 51 + 128 + 85 <= mouse_pos[1] <= padding_step_1 * 4 + 51 + 128 + 85 + 45:
            sound[0].play()
            new_game()


# dessine l'indication permettant de savoir qui doit jouer
def draw_turn_player():
    screen.blit(img_turn[PLAYER - 1], (screen_size[1], padding_step_1))


def draw_win(win_top):
    screen.blit(img_win, (screen_size[1] // 2 - 90, win_top))


def animate_win():
    global win_top
    global animation
    duration = 2000
    mouse_pos = (-100, -100)
    end_value = -screen_size[1]-180
    start_value = screen_size[1]
    start = time.time() * 1000
    current_time = time.time() * 1000
    animation = True
    while current_time - start <= duration:
        current_time = time.time() * 1000
        win_top = round(((screen_size[1]+180)/duration)*(current_time-start))-180
        render((0, 0))
        clock.tick(60)
    animation = False


running = True

# définition des couleurs
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# GUTTER = l'espace entre les cadrants
GUTTER = 8

# JOUEUR = joueur en cours par défaut
PLAYER = 1

# STEP = étape du jeu où :
#    1 = pose d'un pion
#    2 = rotation d'un cadrant
#    3 = victoire
STEP = 1

# marge autour du plateau en fonction de l'étape STEP
padding_step_1 = 8
padding_step_2 = 45

# nombre de colonnes par defaut du plateau
columns = 6

# nombre de pion à aligner par defaut
nb_pions = 5

# position de la souris par defaut
mouse_pos = (0, 0)

# aucunes animations en cours = False
animation = False

# définition du plateau en fonction du nombre de colonne
plateau = bases(columns)

# parametres de nouvelle partie
new_columns = 6
new_nb_pions = 5

# chargement du jeu à partir du fichier "cache"
load()
if STEP == 2:
    padding = padding_step_2
else:
    padding = padding_step_1

# initiation du module pygame
pygame.init()

# définition de la fenêtre
screen_size = (800, 550)
win_top = screen_size[1]
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption('Pentago')
clock = pygame.time.Clock()

# chargement des fichiers image
img = [pygame.image.load(
    'img/0.png'), pygame.image.load('img/1.png'),
    pygame.image.load('img/2.png')]
img_arrow = pygame.image.load('img/arrow.png')
img_button_reset = [pygame.image.load(
    'img/button_reset.png'), pygame.image.load('img/button_reset_hover.png')]
img_interface = [pygame.image.load(
    'img/nb_columns.png'), pygame.image.load('img/nb_pions.png')]
img_turn = [pygame.image.load('img/turn1.png'),
            pygame.image.load('img/turn2.png')]
img_win = pygame.image.load('img/win.png')

# chargement des fichiers audio
sound = [pygame.mixer.Sound("songs/drop.wav"),
         pygame.mixer.Sound("songs/applause.wav")]

while running:
    # si aucunes animations en cours
    if not animation:
        # initialisation des events
        event = pygame.event.wait()

        # lors d'un clique
        if event.type == pygame.MOUSEBUTTONUP:
            # gestion des cliques sur l'interface
            click_interface(pygame.mouse.get_pos())

            # si le joueur doit poser un pion
            if STEP == 1:
                pose_pion(pygame.mouse.get_pos(), PLAYER)

            # sinon, si le joueur doit tourner un cadrant
            elif STEP == 2:
                click_arrows(pygame.mouse.get_pos())

        # detection des mouvements de souris
        if event.type == pygame.MOUSEMOTION:
            # position de la souris dans la variable "mouse_pos"
            mouse_pos = event.pos

        # lorsque la fenêtre est redimensionnée
        if event.type == pygame.VIDEORESIZE:
            # redimensionnement de la fenêtre en gardant le bon ratio (Y+250,Y)
            screen_size = (round(event.size[1] + 250), round(event.size[1]))
            screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

        # dessin du jeu dans la fenêtre
        render((0, 0))

        # gestion du framerate
        clock.tick(60)

    # sort de la boucle si le joueur quitte le jeu
    if event.type == pygame.QUIT:
        running = False

# fermeture du jeu
pygame.quit()
