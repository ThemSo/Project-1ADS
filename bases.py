# Retourne un tableau multi-dimensionnel de n par n
def bases(n):
    plateau = [[0 for i in range(n)] for i in range(n)]
    return plateau

# affiche le tableau pour vérifier le bon fonctionnement des sous-programmes
def afficher_tableau(plateau):
    print('')
    for ligne in plateau:
        for x in ligne:
            print(x, '', end='')
        print('')

plateau = bases(6)
afficher_tableau(plateau)

