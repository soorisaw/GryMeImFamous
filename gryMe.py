from tkinter import *
from random import randint
import sys
sys.setrecursionlimit(5000)


"""********************************* Gestion de Nemo sur touche du clavier *****************************************"""
def Clavier(event):
    global nemoX, nemoY
    touche = event.keysym
    print(touche)
    # déplacement vers le haut
    if touche == 'z':
        can.move(nemo, 0, -10)
    # déplacement vers le bas
    if touche == 's':
        can.move(nemo, 0, 10)
    # déplacement vers la droite
    if touche == 'd':
        can.move(nemo, 10, 0)
    # déplacement vers la gauche
    if touche == 'q':
        can.move(nemo, -10, 0)

    # limite déplacement:
        # gauche
    if can.coords(nemo)[0] <= 0:
        can.move(nemo, 700, 0)
        # droite
    if can.coords(nemo)[0] >= 700:
        can.move(nemo, -700, 0)
        # en haut:
    if can.coords(nemo)[1] <= -10:
        can.move(nemo, 0, 10)
        # en bas:
    if can.coords(nemo)[1] >= 460:
        can.move(nemo, 0, -10)

"""********************************************* Functions *********************************************************"""
# invocation de la vague ennemis;
def summon():

    # creation des ennemis:
    # poisky_1:
    poisky_1 = can.create_image(randint(700, 950), randint(20, 420), image=poisky_Img, anchor="center", tag="wave")
    # poisky_2:
    poisky_2 = can.create_image(randint(700, 950), randint(20, 420), image=poisky_Img, anchor="center", tag="wave")
    # poishy_1:
    poishy_1 = can.create_image(randint(700, 950), randint(20, 420), image=poishy_Img, anchor="center")
    # poishy_2:
    poishy_2 = can.create_image(randint(700, 950), randint(20, 420), image=poishy_Img, anchor="center")
    # shark_1:
    shark_1 = can.create_image(950, randint(20, 420), image=shark_Img, anchor="center", tag="wave")
    # shark_2:
    shark_2 = can.create_image(randint(900, 950), randint(20, 420), image=shark_Img, anchor="center", tag="wave")

    # déclenchement des mouvements ennemi:
    # gentil:
    wave_moveBeEat(can, poishy_1)
    wave_moveBeEat(can, poishy_2)
    # méchant:
    #poisky
    wave_moveEater(can, poisky_1)
    wave_moveEater(can, poisky_2)
    #shark
    wave_moveWithReborn(can, shark_1) # re-forme une nouvelle vague.
    wave_moveEater(can, shark_2)

"""*********************************** les 3 methode de déplacement et collision Ia/nemo*********************************"""
# le seul ennemi (hostile) a faire renaitre la vague:
def wave_moveWithReborn(can, Ia):
    x0, y0, x1, y1 = can.bbox(Ia)
    if x1 <= 0:
        can.delete(Ia)
        can.after(10, wave_moveWithReborn, can, Ia)
        summon()
    else:
        can.move(Ia, randint(-10, -5), 0)
        can.after(speed, wave_moveWithReborn, can, Ia)

# Hostile:
def wave_moveEater(can, Ia):
    w0, s0, w1, s1 = can.bbox(Ia)
    collisionEater(nemo, Ia)
    if s1 <= 0:
        can.delete(Ia)
        can.after(10, wave_moveEater, can, Ia)
    else:
        can.move(Ia, randint(-10, -5), 0)
        can.after(speed, wave_moveEater, can, Ia)

def collisionEater(nemo, Ia):
    nemo_XY = can.bbox(nemo)
    Ia_XY = can.bbox(Ia)
    can.after(1, collisionEater, can, Ia_XY,nemo_XY)
    if nemo_XY[2] >= Ia_XY[0] and nemo_XY[1] > Ia_XY[1] and nemo_XY[1] < Ia_XY[3] and nemo_XY[3] < Ia_XY[3] and nemo_XY[0] < Ia_XY[2]:
        can.delete(nemo)
        can.after(1000, can, Ia, Ia_XY)

# edible:
def wave_moveBeEat(can, Ia):
    l0, h0, l1, h1 = can.bbox(Ia)
    collisionBeEat(nemo, Ia)
    if h1 <= 0:
        can.delete(Ia)
        can.after(10, wave_moveBeEat, can, Ia)
    else:
        can.move(Ia, randint(-10, -5), 0)
        can.after(speed, wave_moveBeEat, can, Ia)

def collisionBeEat(nemo, Ia):
    global score, speed
    labScore.config(text='score: ' + str(score))
    nemo_XY = can.bbox(nemo)
    Ia_XY = can.bbox(Ia)
    can.after(1, collisionBeEat, can, Ia_XY,nemo_XY)
    if nemo_XY[1] > Ia_XY[1] and nemo_XY[1] < Ia_XY[3] and nemo_XY[2] >= Ia_XY[0] and nemo_XY[0] < Ia_XY[0]:
        can.delete(Ia)
        score += 1
        speed -= 2# on augmente la vitess a chaque ennemi mangé
        can.after(1000, can, Ia, Ia_XY)




"""*********************************************************************************************************************"""
# fonction start/stop:
def start():
    global flag
    flag += 1
    if flag == 1:
        Clavier(touche)


def stop():
    global flag
    flag = 0

"""************************************************ VAR ***************************************************************"""

flag = 0
score = 0

sizeX = 700
sizeY = 500

speed = 50


"""************************************************** Canevas *******************************************************"""

# Création de la fenêtre:
gryMe = Tk()
gryMe.title("Gry Me I'm Famous")
# Image de fond
photo = PhotoImage(file="gryMeBack.gif")
# Création du canevas:
can = Canvas(gryMe, bg="light blue", width=sizeX, height=sizeY)
item = can.create_image(0,0,anchor=NW, image=photo)

can.grid(row=2, column=0)
# Création du lien entre la souris, le clavier et le canvas:
can.bind("<Button-1>")
can.focus_set()
gryMe.bind('<Key>', Clavier)

# Création du label "Score":
labScore = Label(gryMe, text="Nombre de Points: " + str(score))
labScore.grid(row=3, column=0)



"""**************************************** Création des boutons ***********************************************"""

# Création du bouton "Débuter la Partie":
Button(gryMe, text="Débuter la Partie", command=start).grid(row=0, column=0)
# Création du bouton "Pause":
Button(gryMe, text="pause", command=stop).grid(row=1, column=0)
# Création du bouton "Quitter":
Button(gryMe, text="Quitter", command=gryMe.destroy).grid(row=4, column=0)

"""************************************************** Avatar ********************************************************"""

# creation de nemo:
nemoImg = PhotoImage(file = 'nemo.gif')
nemo = can.create_image(10, 250, image = nemoImg, anchor = "nw")
#nemo_x0, nemo_y0, nemo_x1, nemo_y1 = can.bbox(nemo)

# creation des ennemis:
# poisky:
poisky_Img = PhotoImage(file='redPoisky.gif')
# poishy:
poishy_Img = PhotoImage(file='hippo.gif')
# shark:
shark_Img = PhotoImage(file='shark.gif')



"""******************************** Action, Moteur, ça tourne !!! ****************************************************"""

summon()

"""**************************************************** The End ;) **************************************************"""
gryMe.mainloop()
