from Evaluation import Evaluation
from IAnumero2 import MorpionAlphaBeta
import random

class Partie:
    def __init__(self):
        self.reinitialiserGrille()
        self.__isTourJoueur1 = None # True = Joueur 1, False = Joueur 2

    def reinitialiserGrille(self):
        self.__grille = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        
    def choixJoueurDepart(self):
        """Tirage au sort du premier joueur"""
        entier = random.randint(1, 100)
        self.__isTourJoueur1 = (entier <= 50)

    def get_isTourJoueur(self):
        return self.__isTourJoueur1

    def jouer_coup(self, r, c, symbole):
        """Tente de jouer un coup. Retourne True si réussi, False sinon."""
        if 0 <= r < 3 and 0 <= c < 3:
            if self.__grille[r][c] == " ":
                self.__grille[r][c] = symbole
                return True
        return False

    def jouer_coup_ia(self, symbole_ia, symbole_adversaire, type_ia=1, difficulte=9):
        """Demande à l'IA de calculer et jouer le meilleur coup sur la grille actuelle"""
        flat_board = [case for ligne in self.__grille for case in ligne]

        if type_ia == 2:
            cerveau = MorpionAlphaBeta(ai_player=symbole_ia, human_player=symbole_adversaire)
        else:
            cerveau = Evaluation(ai_player=symbole_ia, human_player=symbole_adversaire)
        
        index = cerveau.trouver_meilleur_coup(flat_board, depth_limit=difficulte)
        
        if index != -1:
            r = index // 3
            c = index % 3
            self.__grille[r][c] = symbole_ia
            return r, c
        return None

    def verifier_victoire(self, forme):
        """Vérifie si la forme donnée (X ou O) a gagné"""
        g = self.__grille
        for i in range(3):
            if g[i][0] == g[i][1] == g[i][2] == forme: return True
        for j in range(3):
            if g[0][j] == g[1][j] == g[2][j] == forme: return True
        if g[0][0] == g[1][1] == g[2][2] == forme: return True
        if g[0][2] == g[1][1] == g[2][0] == forme: return True
        return False

    def get_grille(self):
        return self.__grille

    def est_match_nul(self):
        """Vérifie si la grille est complètement remplie sans vainqueur."""
        for ligne in self.__grille:
            if " " in ligne:
                return False # Il reste une case vide
        return True # Aucune case vide trouvée

    def simuler_partie_ia_vs_ia(self, symbole_alpha, symbole_beta):
        """
        Joue une partie complète entre IA Alpha (IA 1 : forte) et IA Beta (IA 2 : faible)
        de manière purement logique et transparente pour l'interface.
        Retourne le vainqueur ("Alpha", "Beta") ou "Nul".
        """
        tour_actuel = "X" # X commence toujours
        
        # On instancie les IA une seule fois pour toute la partie
        cerveau_alpha = Evaluation(ai_player=symbole_alpha, human_player=symbole_beta)
        cerveau_beta = MorpionAlphaBeta(ai_player=symbole_beta, human_player=symbole_alpha)
        
        while True: # La boucle tourne jusqu'à ce qu'un return l'arrête
            if self.est_match_nul():
                return "Nul"
                
            flat = [case for ligne in self.__grille for case in ligne]
            
            if tour_actuel == symbole_alpha:
                idx = cerveau_alpha.trouver_meilleur_coup(flat)
            else:
                idx = cerveau_beta.trouver_meilleur_coup(flat)
                
            if idx != -1:
                r, c = idx // 3, idx % 3
                self.jouer_coup(r, c, tour_actuel)
                
                if self.verifier_victoire(tour_actuel):
                    return "Alpha" if tour_actuel == symbole_alpha else "Beta"
                    
                tour_actuel = "O" if tour_actuel == "X" else "X"
            else:
                return "Nul" 