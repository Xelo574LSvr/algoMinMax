import random
from Ordinateur import Ordinateur
from Joueur import Joueur
from Evaluation import Evaluation


class Partie:

    def __init__(self):
        self.__isTourJoueur1 = None
        self.__joueur1 = None
        self.__joueur2 = None
        self.__grille = []

    def choixJoueurDepart(self):
        entier = random.randint(1, 100)
        self.__isTourJoueur1 = (entier <= 50)

    def changerTourJoueur(self):
        self.__isTourJoueur1 = not self.__isTourJoueur1

    def lancementPartie(self):
        print("Vous allez démarrer une partie de Morpion")
        print()

        choixModeJeu = 0
        while choixModeJeu != "1" and choixModeJeu != "2":
            print("Voici les différents modes de jeux que vous pouvez lancer :")
            print("1 : joueur contre ordinateur")
            print("2 : ordinateur contre ordinateur")
            choixModeJeu = input("Veuillez choisir le mode de jeu : ")

        self.choixJoueurDepart()

        if choixModeJeu == "1":
            pseudo = input("Veuillez entrer un pseudo : ")
            self.__joueur1 = Joueur(pseudo, self.choixFormeJoueur())
        elif choixModeJeu == "2":
            self.__joueur1 = Ordinateur(self.choixFormeJoueur())

        # Changement temporaire pour définir la forme du J2
        self.changerTourJoueur()
        self.__joueur2 = Ordinateur(self.choixFormeJoueur())
        # On remet le tour correct
        self.changerTourJoueur()

        self.afficher_info_joueurs()
        print("\nDébut de la partie !")

        self.reinitialiserGrille()
        self.afficherEtatPartie()

        # Déroulement de la partie
        partie_en_cours = True
        while partie_en_cours:
            joueur_actuel = self.__joueur1 if self.__isTourJoueur1 else self.__joueur2
            adversaire = self.__joueur2 if self.__isTourJoueur1 else self.__joueur1

            print(f"\nC'est au tour de {self.get_nom_joueur(joueur_actuel)} ({joueur_actuel.forme})")

            if isinstance(joueur_actuel, Ordinateur):
                # --- LOGIQUE IA ---
                ia_cerveau = Evaluation(joueur_actuel.forme, adversaire.forme)

                flat_board = self.get_grille_flat()

                coup_index = ia_cerveau.trouver_meilleur_coup(flat_board)

                ligne = coup_index // 3
                colonne = coup_index % 3

                print(f"L'ordinateur joue en case {coup_index + 1}")
                self.__grille[ligne][colonne] = joueur_actuel.forme

            else:
                # --- LOGIQUE HUMAIN ---
                coup_valide = False
                while not coup_valide:
                    try:
                        choix = int(input("Entrez le numéro de la case (1-9) : "))
                        if 1 <= choix <= 9:
                            ligne = (choix - 1) // 3
                            colonne = (choix - 1) % 3
                            if self.__grille[ligne][colonne] == " ":
                                self.__grille[ligne][colonne] = joueur_actuel.forme
                                coup_valide = True
                            else:
                                print("Case déjà occupée !")
                        else:
                            print("Chiffre doit être entre 1 et 9.")
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")

            self.afficherEtatPartie()

            if self.verifier_victoire(joueur_actuel.forme):
                print(f"\nBRAVO ! {self.get_nom_joueur(joueur_actuel)} a gagné !")
                partie_en_cours = False
            elif self.est_match_nul():
                print("\nMatch nul ! La grille est pleine.")
                partie_en_cours = False
            else:
                self.changerTourJoueur()

    def get_nom_joueur(self, joueur):
        if isinstance(joueur, Joueur):
            return joueur.nom
        return "Ordinateur"

    def afficher_info_joueurs(self):
        print(f"Joueur 1 : {self.get_nom_joueur(self.__joueur1)} ({self.__joueur1.forme})")
        print(f"Joueur 2 : {self.get_nom_joueur(self.__joueur2)} ({self.__joueur2.forme})")

    def choixFormeJoueur(self):
        return "X" if self.__isTourJoueur1 else "O"

    def afficherEtatPartie(self):
        print("\n")
        g = self.__grille
        print(f" {g[0][0]} | {g[0][1]} | {g[0][2]} ")
        print("---+---+---")
        print(f" {g[1][0]} | {g[1][1]} | {g[1][2]} ")
        print("---+---+---")
        print(f" {g[2][0]} | {g[2][1]} | {g[2][2]} ")
        print("\n")

    def reinitialiserGrille(self):
        self.__grille = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

    def get_grille_flat(self):
        """Convertit la grille 2D en liste 1D pour l'IA"""
        return [case for ligne in self.__grille for case in ligne]

    def est_match_nul(self):
        return " " not in self.get_grille_flat()

    def verifier_victoire(self, forme):
        g = self.__grille
        # Lignes
        for i in range(3):
            if g[i][0] == g[i][1] == g[i][2] == forme: return True
        # Colonnes
        for j in range(3):
            if g[0][j] == g[1][j] == g[2][j] == forme: return True
        # Diagonales
        if g[0][0] == g[1][1] == g[2][2] == forme: return True
        if g[0][2] == g[1][1] == g[2][0] == forme: return True

        return False

    # Getters
    def get_isTourJoueur(self):
        return self.__isTourJoueur1

    def get_joueur1(self):
        return self.__joueur1

    def get_joueur2(self):
        return self.__joueur2

    def get_grille(self):
        return self.__grille