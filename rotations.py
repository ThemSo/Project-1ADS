plateau = [
    [0, 1, 1, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
]

# affiche le tableau pour vérifier le bon fonctionnement des sous-programmes


def afficher_tableau(plateau):
    for ligne in plateau:
        for x in ligne:
            print(x, '', end='')
        print('')


# numéros des cotés
#  ___
# |1|3|
# |2|4|
#  ---
#
# rotation d'un plateau
# rotation_plateau(liste, nombre_de_ligne, numero_du_cote, True = horaire
# et False = antihoraire)
def rotation_plateau(plateau, m, n, sens):
    x, y, maxx, maxy = 0, 0, m // 2, m // 2

    if n % 2 == 0:
        x = m // 2
        maxx = m
    if n > 2:
        y = m // 2
        maxy = m
    tmp = [[0 for i in range(m // 2)] for i in range(m // 2)]
    tmpy = maxy
    while tmpy > y:
        tmpx = maxx
        while tmpx > x:
            if not sens:
                tmp[maxy - tmpy][tmpx - x - 1] = plateau[tmpx - 1][tmpy - 1]
            else:
                tmp[tmpy - y - 1][maxx - tmpx] = plateau[tmpx - 1][tmpy - 1]
            tmpx -= 1
        tmpy -= 1

    for nx, vx in enumerate(tmp):
        for ny, vy in enumerate(vx):
            plateau[nx + x][ny + y] = vy

    return plateau


print("\n------------------\nAvant rotation:\n")

afficher_tableau(plateau)

print("\n------------------\nAprès rotation:\n")

# numéros des cotés
#  ___
# |1|3|
# |2|4|
#  ---
#
# rotation_plateau(plateau, nombre_de_lignes, numero_du_cote, True =
# rotation horaire et False = antihoraire)
plateau = rotation_plateau(plateau, 8, 1, True)
afficher_tableau(plateau)

print('')
