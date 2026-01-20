import sys

class MorpionConsole:
    def __init__(self):
        # Codes couleurs pour la console
        self.RED = '\033[91m'
        self.BLUE = '\033[94m'
        self.GREEN = '\033[92m'
        self.RESET = '\033[0m'
        self.BOLD = '\033[1m'

        # Rôles (Ta convention)
        self.MIN_PLAYER = 'o' # Cherche -10 (Rouge)
        self.MAX_PLAYER = 'x' # Cherche +10 (Bleu)

    def est_gagnant(self, joueur, board):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(board[x] == board[y] == board[z] == joueur for x, y, z in wins)

    def est_plein(self, board):
        return ' ' not in board

    def _format_board_line(self, board):
        """Affiche le plateau en une seule ligne compacte pour l'arbre"""
        # Remplace les espaces par des points pour la visibilité
        compact = "".join([c if c != ' ' else '.' for c in board])
        return f"[{compact[:3]}|{compact[3:6]}|{compact[6:]}]"

    def minimax_ascii(self, board, profondeur, is_min_turn, prefix="", is_last=True):
        """
        Fonction récursive qui calcule le score ET dessine l'arbre
        """
        # 1. Gestion de l'affichage de la branche
        marker = "└── " if is_last else "├── "
        current_prefix = prefix + marker
        
        # Préparation du préfixe pour les enfants (si on est le dernier, on laisse un vide, sinon une barre)
        child_prefix = prefix + ("    " if is_last else "│   ")

        # 2. Vérification des états terminaux
        if self.est_gagnant(self.MIN_PLAYER, board):
            score = -10 
            print(f"{current_prefix}{self.RED}{self._format_board_line(board)} VICTOIRE MIN ({score}){self.RESET}")
            return score

        if self.est_gagnant(self.MAX_PLAYER, board):
            score = 10
            print(f"{current_prefix}{self.BLUE}{self._format_board_line(board)} VICTOIRE MAX ({score}){self.RESET}")
            return score
            
        if self.est_plein(board):
            score = 0
            print(f"{current_prefix}{self.RESET}{self._format_board_line(board)} NUL ({score}){self.RESET}")
            return score
            
        # Limite de sécurité (pour ne pas inonder la console si on part d'un plateau vide)
        if profondeur >= 3:
            print(f"{current_prefix}{self.RESET}{self._format_board_line(board)} ... (Stop Profondeur){self.RESET}")
            return 0 # Estimation neutre

        # 3. Affichage du noeud courant (si ce n'est pas une feuille)
        joueur_courant = "MIN (o)" if is_min_turn else "MAX (x)"
        couleur = self.RED if is_min_turn else self.BLUE
        print(f"{current_prefix}{couleur}{self._format_board_line(board)} {joueur_courant} cherche...{self.RESET}")

        # 4. Récursion (Génération des enfants)
        coups_possibles = [i for i, c in enumerate(board) if c == ' ']
        scores = []
        
        for index, coup in enumerate(coups_possibles):
            board[coup] = self.MIN_PLAYER if is_min_turn else self.MAX_PLAYER
            
            # Est-ce le dernier enfant de la liste ? (pour le dessin)
            is_last_child = (index == len(coups_possibles) - 1)
            
            score = self.minimax_ascii(board, profondeur + 1, not is_min_turn, child_prefix, is_last_child)
            scores.append(score)
            
            board[coup] = ' ' # Backtracking

        # 5. Calcul et retour du résultat pour ce noeud
        if is_min_turn:
            final_score = min(scores) if scores else 0
        else:
            final_score = max(scores) if scores else 0
            
        # Optionnel : Afficher le score remonté à la fin de la ligne du noeud parent
        # (Un peu complexe à faire proprement en console séquentielle, on se contente de retourner la valeur)
        return final_score

    def lancer_demonstration(self):
        print(f"\n{self.BOLD}--- ARBRE DE DÉCISION MORPION (ASCII) ---{self.RESET}")
        print("Convention : " + self.RED + "MIN (o) cherche -10" + self.RESET + " | " + self.BLUE + "MAX (x) cherche +10" + self.RESET)
        print("Légende plateau : [Ligne1|Ligne2|Ligne3]\n")

        # --- SCÉNARIO : MIN peut gagner ou faire une erreur ---
        # x x .
        # o o .
        # . . .
        scenario = ['x', 'o', ' ', 'o', 'x', ' ', ' ', ' ', ' ']
        
        print("Situation de départ : C'est à MIN (o) de jouer.")
        self.minimax_ascii(scenario, 0, True) # True car c'est à Min


class MorpionHeuristique:
    def __init__(self):
        self.MIN_PLAYER = 'o' 
        self.MAX_PLAYER = 'x'
        
        # Emojis
        self.ICO = {
            'x': '❌',
            'o': '🔴',
            ' ': '⬜'
        }

    def afficher_grille(self, board):
        """Affiche la grille en format 3x3 bien propre"""
        b = [self.ICO[c] for c in board]
        print(f"\n  {b[0]} {b[1]} {b[2]}")
        print(f"  {b[3]} {b[4]} {b[5]}")
        print(f"  {b[6]} {b[7]} {b[8]}\n")

    def evaluer_etat(self, board):
        """Fonction Heuristique : Donne une température du jeu"""
        score = 0
        lignes = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

        for indices in lignes:
            # On regarde ce qu'il y a dans la ligne
            contenu = [board[i] for i in indices]
            nb_max = contenu.count(self.MAX_PLAYER)
            nb_min = contenu.count(self.MIN_PLAYER)

            # Si la ligne est "sale" (contient les deux symboles), elle vaut 0
            if nb_max > 0 and nb_min > 0:
                continue

            # Calcul des points pour MAX (Positif)
            if nb_max == 3: return 1000 # Victoire (Valeur énorme pour écraser le reste)
            if nb_max == 2: score += 10 # 2 alignés
            if nb_max == 1: score += 1  # 1 placé

            # Calcul des points pour MIN (Négatif)
            if nb_min == 3: return -1000
            if nb_min == 2: score -= 10
            if nb_min == 1: score -= 1
            
        return score

    def demo_evaluation(self):
        print("\n=== TEST DE L'ÉVALUATION HEURISTIQUE ===\n")
        
        # SCÉNARIO 1 : Avantage MAX (Deux X alignés sans blocage)
        # x x .
        # . o .
        # . . .
        b1 = ['x', 'x', ' ', ' ', 'o', ' ', ' ', ' ', ' ']
        print(f"Grille 1 : {self.afficher_grille(b1)}")
        print(f"Score calculé : {self.evaluer_etat(b1)}")
        print("Analyse : +10 (ligne haut) + 1 (colonne gauche) - 1 (centre) = +10 environ\n")

        # SCÉNARIO 2 : Avantage MIN (Deux O alignés + Un O isolé)
        # o o .
        # . x .
        # . . o
        b2 = ['o', 'o', ' ', ' ', 'x', ' ', ' ', ' ', 'o']
        print(f"Grille 2 : {self.afficher_grille(b2)}")
        print(f"Score calculé : {self.evaluer_etat(b2)}")
        print("Analyse : Doit être négatif (avantage Rouge)\n")

        # SCÉNARIO 3 : Équilibre parfait
        # x . .
        # . o .
        # . . .
        b3 = ['x', 'x', 'x', ' ', 'o', 'o', ' ', ' ', ' ']
        print(f"Grille 3 : {self.afficher_grille(b3)}")
        print(f"Score calculé : {self.evaluer_etat(b3)}")
        print("Analyse : +1 pour X, -1 pour O. Total attendu = 0\n")

if __name__ == "__main__":
    app = MorpionHeuristique()
    app.demo_evaluation()
    
