j = 5
plateau = [
	[0, 1, 1, 1, 1, 0],
	[1, 0, 1, 1, 0, 1],
	[1, 1, 1, 0, 1, 1],
	[1, 1, 0, 0, 1, 1],
	[1, 0, 1, 1, 1, 1],
	[0, 1, 1, 1, 1, 0],
]


def start_game():
    global x
    global y
    global p
    y = int(input("\nNombre de colonnes du plateau : "))
    x = int(input("Nombre de lignes du plateau : "))
    p = int(input("Nombre de pions à aligner : "))
    if y <= 5 or x <= 5 or p < 5:
        print("\nCa risque de ne pas etre tres amusant...")
        start_game()
        return False
    plateau = [[0 for i in range(0, y)] for i in range(0, x)]


# affiche le tableau pour vérifier le bon fonctionnement des sous-programmes
def afficher_tableau(plateau):
    for ligne in plateau:
        for x in ligne:
            print(x, '', end='')
        print('')

# verification des condition de victoire horyzontales
def victoire_horyzontal (column, plateau, player, n, p, j):
    plateau
    p = 0
    for i in n [column] :
        if i != player :
            if p >= j:
                return  True
            else :
                p = 0
        else :
            p += 1
            if p >= j:
                return True
    return False

# verification des conditions de victoires verticales
def victoire_vertical (plateau, column, player, n, p, j):
    plateau
    p = 0
    for i in plateau :
        if i[column] != player:
            if p >= j:
                return True
            else:
                p = 0
        else:
            p = 0
            if p >= j:
                return True
    return False

# verification des condition de victoire diagonale du bas à gauche vers le haut droit
def victoire_diagonal1(plateau, player):
    for i in range(0, x+y):
        p = 0
        for x in range (-x, y*2):
            if 0 <= i-x < len(plateau[0]) and 0 <= x < len(plateau):
                if plateau[x][i-x] != player:
                    if p >= j:
                        return True
                    else:
                        p = 0
                else:
                    p += 1
                    if p >= j:
                        return True
    return False

# verification des conditions de victoire diagonale allant du haut à gauche vers le bas à droite
def vicoire_diagonal2 (plateau, player):
    for i in range (-y, y*2):
        p = 0
        for x in range (0, x+y):
            if 0 <= x < len(plateau) and 0 <= x+i < len(plateau[0]):
                if plateau[x][x+i] != player:
                    if p >= j:
                        return True
                    else:
                        p = 0
                else:
                    p += 1
                    if p >= j:
                        return True
    return False

# test de victoire si les conditions d'alignement return
def test_win(plateau, columnx, columny, player):
    if victoire_horyzontal(plateau, columny, player) or victoire_vertical(plateau, columnx, player) or victoire_diagonal1(plateau, player) or vicoire_diagonal2(plateau, player):
        return True
    return False
