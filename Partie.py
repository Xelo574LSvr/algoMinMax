import random

from Ordinateur import Ordinateur
from Joueur import Joueur


class Partie:

    def __init__(self):
        self.__isTourJoueur = None
        self.__joueur1 = None
        self.__joueur2 = None
        self.__grille = [
            ["X", " ", " "],
            [" ", "X", "O"],
            [" ", " ", " "]
        ]
        self.choixJoueurDepart()

    def choixJoueurDepart(self):
        entier = random.randint(1, 100)
        if entier <= 50:
            self.__isTourJoueur = 1
        else:
            self.__isTourJoueur = 2

    def changerTourJoueur(self):
        if self.__isTourJoueur == 1:
            self.__isTourJoueur = 2
        else :
            self.__isTourJoueur = 1

    def lancementPartie(self):
        print("Vous allez démarrer une partie de Morpion")
        print()

        print("Voici les différents modes de jeux que vous pouvez lancer :")
        print("1 : joueur contre ordinateur")
        print("2 : ordinateur contre ordinateur")
        print()

        print("Veuillez choisir le mode de jeu : (ne taper que le numéro du mode de jeu)")
        choixModeJeu = input()

        if choixModeJeu == "1":
            pseudo = input("Veuillez entrer un pseudo : ")
            self.__joueur1 = Joueur(pseudo, "X")
        elif choixModeJeu == "2":
            self.__joueur1 = Ordinateur("X")

        self.__joueur2 = Ordinateur("O")

        if self.__joueur1:
            print(f"Joueur 1 : {self.__joueur1.nom} ({self.__joueur1.forme})")

        if self.__joueur2:
            print(f"Joueur 2 : {self.__joueur2} ({self.__joueur2.forme})")

        print("\nDébut de la partie !")

        self.afficherEtatPartie()


    # Affichage de la grille de la partie
    def afficherEtatPartie(self):
        print(str(self.__grille[0][0]) + "  | " + str(self.__grille[0][1]) + " |  " + str(self.__grille[0][2]))
        print("---+---+---")
        print(str(self.__grille[1][0]) + "  | " + str(self.__grille[1][1]) + " |  " + str(self.__grille[1][2]))
        print("---+---+---")
        print(str(self.__grille[2][0]) + "  | " + str(self.__grille[2][1]) + " |  " + str(self.__grille[2][2]))



    # Getters
    def get_isTourJoueur(self):
        return self.__isTourJoueur

    def get_joueur1(self):
        return self.__joueur1

    def get_joueur2(self):
        return self.__joueur2

    def get_grille(self):
        return self.__grille