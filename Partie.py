import random

from Ordinateur import Ordinateur
from Joueur import Joueur


class Partie:

    def __init__(self):
        self.__isTourJoueur1 = None
        self.__joueur1 = None
        self.__joueur2 = None
        self.__grille = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]

    def choixJoueurDepart(self):
        entier = random.randint(1, 100)
        print(entier)
        if entier <= 50:
            self.__isTourJoueur1 = True
        else:
            self.__isTourJoueur1 = False

    def changerTourJoueur(self):
        if self.__isTourJoueur1:
            self.__isTourJoueur1 = False
        else :
            self.__isTourJoueur1 = True

    def lancementPartie(self):
        print("Vous allez démarrer une partie de Morpion")
        print()

        print("Voici les différents modes de jeux que vous pouvez lancer :")
        print("1 : joueur contre ordinateur")
        print("2 : ordinateur contre ordinateur")
        print()

        print("Veuillez choisir le mode de jeu : (ne taper que le numéro du mode de jeu)")
        choixModeJeu = input()

        self.choixJoueurDepart()

        if choixModeJeu == "1":
            pseudo = input("Veuillez entrer un pseudo : ")
            self.__joueur1 = Joueur(pseudo, self.choixFormeJoueur())
        elif choixModeJeu == "2":
            self.__joueur1 = Ordinateur(self.choixFormeJoueur())

        # Changement du joueur a qui c'est le tour pour obtenir l'autre forme
        self.changerTourJoueur()
        self.__joueur2 = Ordinateur(self.choixFormeJoueur())
        # Remise du tour du joueur initial
        self.changerTourJoueur()

        if self.__joueur1:
            print(f"Joueur 1 : {self.__joueur1.nom} ({self.__joueur1.forme})")

        if self.__joueur2:
            print(f"Joueur 2 : {self.__joueur2} ({self.__joueur2.forme})")

        print("\nDébut de la partie !")

        print("\nLe premier joueur est ")
        print(self.__isTourJoueur1)

        self.reinitialiserGrille()
        self.afficherEtatPartie()

    def choixFormeJoueur(self):
        if self.__isTourJoueur1:
            return "X"
        else:
            return "O"

    def afficherEtatPartie(self):
        """Affiche l'état de la partie"""
        print(str(self.__grille[0][0]) + "  | " + str(self.__grille[0][1]) + " |  " + str(self.__grille[0][2]))
        print("---+---+---")
        print(str(self.__grille[1][0]) + "  | " + str(self.__grille[1][1]) + " |  " + str(self.__grille[1][2]))
        print("---+---+---")
        print(str(self.__grille[2][0]) + "  | " + str(self.__grille[2][1]) + " |  " + str(self.__grille[2][2]))

    def reinitialiserGrille(self):
        """Réinitialise la grille de la partie"""

        self.__grille = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

    # Getters
    def get_isTourJoueur(self):
        return self.__isTourJoueur1

    def get_joueur1(self):
        return self.__joueur1

    def get_joueur2(self):
        return self.__joueur2

    def get_grille(self):
        return self.__grille