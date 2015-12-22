from random import randint


def start_game():
    global X
    global Y
    global Z
    Y = int(input("\nNombre de colonnes du plateau : "))
    X = int(input("Nombre de lignes du plateau : "))
    Z = int(input("Nombre de pions à aligner : "))
    if Y <= 3 or X <= 3 or Z < 2:
        print("\nCa risque de ne pas etre tres amusant...")
        start_game()
        return False
    plateau = [[0 for i in range(0, Y)] for i in range(0, X)]
    draw_game(plateau)
    play_player(plateau)


# dessin du plateau (2.2)
def draw_game(plateau):
    print()
    for y in plateau:
        print("|", end="")
        for x in y:
            if x == -1:
                player = 'o'
            elif x == 1:
                player = 'x'
            else:
                player = ' '
            print(player, "|", sep="", end="")
        print("")

    for i in plateau[0]:
        print(" -", sep="", end="")
    print()
    for i, x in enumerate(plateau[0]):
        print(" ", i+1, sep="", end="")
    print()


# calcul du nombre de pions dans une colonne (2.3.1)
def height_column(plateau, column):
    return len(plateau[column-1])-plateau[column-1].count(0)


# calcule si une colonne est pleine et retourne un booléen (2.3.2)
def is_full_column(plateau, column):
    for i in plateau:
        if i[column-1] == 0:
            return False
    return True

# pose d'un pion par le joueur (2.3.3)
def play_player(plateau):
    print("\nDans quelle colonne voulez-vous poser votre pion (entre 1 et ", len(plateau[0]),")", sep="", end="")
    column = int(input(": "))
    if column > len(plateau[0]) or column < 1:
        print("Votre pion viens de tomber a cote du plateau...")
        play_player(plateau)
        return False
    elif is_full_column(plateau, column):
        print("Il semblerait que cette colonne soit deja pleine.")
        play_player(plateau)
        return False
    else:
        drop(plateau, column, 1)


# pose d'un pion par l'ordinateur (2.3.4)
def play_computer(plateau):
    column = randint(1, len(plateau[0]))
    print("\nL'ordinateur joue dans la colonne", column)
    drop(plateau, column, -1) if not is_full_column(plateau, column) else play_computer(plateau)


# pose d'un pion
def drop(plateau, column, player):
    i = len(plateau)-1
    while i >= 0:
        if plateau[i][column-1] == 0:
            plateau[i][column-1] = player
            break
        else:
            i -= 1
    if player == -1:
        draw_game(plateau)
    if test_win(plateau, column-1, i, player):
        if player == 1:
            draw_game(plateau)
            print("\nVous avez gagne !!")
        else:
            print("\nL'ordinateur a gagne !")
    else:
        play_computer(plateau) if player == 1 else play_player(plateau)


# verification des conditions de victoires horizontales (2.4.1)
def victory_horizontal(plateau, column, player):
    victory = 0
    for i in plateau[column]:
        if i != player:
            if victory >= Z:
                return True
            else:
                victory = 0
        else:
            victory += 1
            if victory >= Z:
                return True

    return False


# verification des conditions de victoires verticales (2.4.2)
def victory_vertical(plateau, column, player):
    victory = 0
    for i in plateau:
        if i[column] != player:
            if victory >= Z:
                return True
            else:
                victory = 0
        else:
            victory += 1
            if victory >= Z:
                return True
    return False


# verification des condition de victoire diagonale du bas à gauche vers le haut droit (2.4.3)
def victory_diagonal1(plateau, player):
    for i in range(0, X+Y):
        victory = 0
        for x in range(-Y, Y*2):
            if 0 <= i-x < len(plateau[0]) and 0 <= x < len(plateau):
                if plateau[x][i-x] != player:
                    if victory >= Z:
                        return True
                    else:
                        victory = 0
                else:
                    victory += 1
                    if victory >= Z:
                        return True
    return False


# verification des condition de victoire diagonale du haut à gauche vers le bas droit (2.4.4)
def victory_diagonal2(plateau, player):
    for i in range(-Y, Y*2):
        victory = 0
        for x in range(0, X+Y):
            if 0 <= x < len(plateau) and 0 <= x+i < len(plateau[0]):
                # print(x, x+i)
                if plateau[x][x+i] != player:
                    if victory >= Z:
                        return True
                    else:
                        victory = 0
                else:
                    victory += 1
                    if victory >= Z:
                        return True
    return False


# test de victoire, return True si le player en argument a gagne (2.4.5)
def test_win(plateau, columnx, columny, player):
    if victory_horizontal(plateau, columny, player) or victory_vertical(plateau, columnx, player) or victory_diagonal1(plateau, player) or victory_diagonal2(plateau, player):
        return True
    return False


start_game()