import turtle as t
import math as m

def labyFromFile(fn) :
    """
    Lecture d'un labyrinthe dans le fichier de nom fn
    Read a maze from the file named fn.
    """
    f = open(fn)
    laby = []
    indline = 0
    for fileline in f:
        labyline = []
        inditem = 0
        for item in fileline:
            # empty cell / case vide
            if item == ".":
                labyline.append(0)
            # wall / mur
            elif item == "#":
                labyline.append(1)
            # entrance / entree
            elif item == "x":
                labyline.append(0)
                mazeIn = [indline, inditem]
            # exit / sortie
            elif item == "X":
                labyline.append(0)
                mazeOut = [indline, inditem]
            # discard "\n" char at the end of each line
            inditem += 1
        laby.append(labyline)
        indline += 1
    f.close()
    return laby, mazeIn, mazeOut

laby1 = "C:\\Users\\calov\\PycharmProjects\\pythonProject\\laby0.laby"
[laby, entry_co, exit_co] = labyFromFile(laby1)
dicoJeu={
    'laby': laby,
    'entry': entry_co,
    'exit': exit_co,
}

def affichetextuel(dicoJeu):
    x = 0
    for ligne in dicoJeu['laby']:
        y = 0
        for elmt in ligne:
            coord = [x, y]
            if dicoJeu['entry'] == coord:
                print("x", end='')
            elif coord == dicoJeu['exit']:
                print("o", end='')
            else:
                if elmt == 1:
                    print('#', end='')
                elif elmt == 0:
                    print(' ', end='')
            y += 1
        x += 1
        print()

def square(coleur):
    t.color(coleur)
    t.begin_fill()
    for _ in range(4):
        t.forward(50)
        t.right(90)
    t.end_fill()
    t.speed(0)


def afficheGraphique(dicoJeu):
    t.up()
    t.goto(-300, 300)
    t.down()
    x = 0
    for ligne in dicoJeu['laby']:  # ligne prend la valeur de chacune des trois listes dans la "grande liste" Laby
        y = 0
        for elmt in ligne:  # elements individuelles de chaque liste, les 1 et 0
            coord = [x, y]
            if coord == dicoJeu['entry']:
                print(square("red"), t.forward(50))
            elif coord == dicoJeu['exit']:
                print(square("green"), t.forward(50))
            else:
                if elmt == 1:
                    print(square("blue"), t.forward(50))
                elif elmt == 0:
                    print(t.up(), t.forward(50), t.down())
            y += 1
        x += 1
        t.up()
        t.goto(-300, 300 - (50 * x))
        t.down()

def pixel2cell(x, y):
    x += 300;
    y -= 300
    xcell = abs(m.floor(x / 50))
    ycell = abs(m.floor(y / 50)) - 1
    return (ycell, xcell)


def testClic(x, y):
    """reçoit les coordonnées d’un clic, les convertit, et affiche la ligne et la colonne correspondante du labyrinthe
(ou un message d’erreur si clic hors du labyrinthe)"""
    Coords = pixel2cell(x, y)
    if Coords[0] in range(len(dicoJeu['laby']) + 1) and Coords[1] in range(16):
        print("ligne: ", Coords[0], "colonne: ", Coords[1], "type: ", typeCellule(Coords[0], Coords[1]))
    else:print("Click hors labyrinth, essayez a nouveau")

def typeCellule(x, y):
    """reçoit les coordonnées (ligne et colonne)
d’une case du labyrinthe, et qui renvoie son type : entrée, sortie, passage, mur. """
    if dicoJeu['entry'] == [x, y]:
        return "entree"
    elif dicoJeu['exit'] == [x, y]:
        return "sortie"
    else:
        if dicoJeu['laby'][x][y] == 1:
            return "mur"
        elif dicoJeu['laby'][x][y] == 0:
            type=typePassage(voisin(x,y))
            return "passage", type

def voisin(x, y):
    """reçoit les coordonnées (ligne et colonne) d’une case du labyrinthe, et qui renvoie la liste
     des coordonnées des cases voisines (haut, bas, gauche, droite)"""
    voisin = []
    if x > 0:
        voisin.append([x - 1, y])
    if x < len(dicoJeu['laby']) - 1:
        voisin.append([x + 1, y])
    if y > 0:
        voisin.append([x, y - 1])
    if y < len(dicoJeu['laby'][0]) - 1:
        voisin.append([x, y + 1])
    return voisin

def typePassage(listeVoisins):
    """indiquer si une case « passage » est une impasse, un passage standard, ou un carrefour. """
    if len(listeVoisins) == 1:
        return "impasse"
    elif len(listeVoisins) == 2:
        return "passage"
    elif len(listeVoisins) == 3:
        return "carrefour"
    elif len(listeVoisins) == 4:
        return "carrefour"

def cell2pixel(i,j):
    """i réalise la conversion inverse (coordonnées du centre de la cellule i-j)"""
    x = -300 + (50 * j) + 25
    y = 300 - (50 * i) - 25
    return (x, y)


# prog principal
#print (affichetextuel(dicoJeu))

print(afficheGraphique(dicoJeu))


t.onscreenclick(testClic)
t.mainloop()