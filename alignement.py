plateau = [
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0]
]

# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2


# |
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


# __
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


# /
def victory_diagonal1(n, l, p, j):
    for i in range(n*2):
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


# \
def victory_diagonal2(n, l, p, j):
    for i in range(n*2):
        x, y, v = i, n-1, 0
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


def test_win(n, l, p, j):
    if victory_horizontal(n, l, p, j) or victory_vertical(n, l, p, j) or victory_diagonal1(n, l, p, j) or victory_diagonal2(n, l, p, j):
        return True
    return False

print(test_win(6, plateau, 2, 1))