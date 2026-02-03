import sys


class MorpionAlphaBeta:
    def __init__(self):
        self.MIN_PLAYER = 'o'
        self.MAX_PLAYER = 'x'
        self.ICO = {'x': '❌', 'o': '🔴', ' ': '⬜'}

        # Identités (définies au lancement)
        self.ia_symbol = 'x'
        self.humain_symbol = 'o'

    def afficher_grille(self, board):
        b = [self.ICO[c] for c in board]
        print(f"\n  {b[0]} {b[1]} {b[2]}")
        print(f"  {b[3]} {b[4]} {b[5]}")
        print(f"  {b[6]} {b[7]} {b[8]}\n")

    def est_plein(self, board):
        return ' ' not in board

        # --- Permet d'évaluer l'état de jeu ---

    def evaluer_etat(self, board):
        score = 0
        lignes = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

        # Qui a l'initiative ?
        nb_x = board.count(self.MAX_PLAYER)
        nb_o = board.count(self.MIN_PLAYER)
        tour_a_max = (nb_x == nb_o)

        for indices in lignes:
            contenu = [board[i] for i in indices]
            nb_max = contenu.count(self.MAX_PLAYER)
            nb_min = contenu.count(self.MIN_PLAYER)

            if nb_max > 0 and nb_min > 0: continue

            # Pour MAX (IA)
            if nb_max == 3: return 1000
            if nb_max == 2:
                score += 50 if tour_a_max else 10
            elif nb_max == 1:
                score += 1

            # Pour MIN (Adversaire)
            if nb_min == 3: return -1000
            if nb_min == 2:
                score -= 50 if not tour_a_max else 10
            elif nb_min == 1:
                score -= 1

        return score

        # --- Algorithme min max ---

    def minimax(self, board, profondeur, is_max, depth_limit):
        score = self.evaluer_etat(board)
        if score == 1000: return 1000 - profondeur
        if score == -1000: return -1000 + profondeur
        if self.est_plein(board): return 0

        if profondeur >= depth_limit:
            return score

        if is_max:
            best = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.MAX_PLAYER
                    val = self.minimax(board, profondeur + 1, False, depth_limit)
                    board[i] = ' '
                    best = max(best, val)
            return best
        else:
            best = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.MIN_PLAYER
                    val = self.minimax(board, profondeur + 1, True, depth_limit)
                    board[i] = ' '
                    best = min(best, val)
            return best

    def trouver_meilleur_coup(self, board):
        meilleur_score = -float('inf')
        meilleur_coup = -1

        coups_possibles = [i for i, x in enumerate(board) if x == ' ']

        # Petit message console optionnel
        # print(f"L'IA ({self.MAX_PLAYER}) réfléchit ({len(coups_possibles)} options)...")

        for coup in coups_possibles:
            board[coup] = self.MAX_PLAYER
            score = self.minimax(board, 0, False, 1)
            board[coup] = ' '

            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup

        return meilleur_coup

    def choisir_camp(self):
        print("\n--- MODE COMPÉTITION (IA INVINCIBLE) ---")
        print("Qui commence ?")
        print("1. Moi (Je joue les X)")
        print("2. L'IA (Elle joue les X)")
        while True:
            c = input("Choix : ")
            if c == '1':
                self.humain_symbol = 'x';
                self.ia_symbol = 'o'
                return False
            elif c == '2':
                self.humain_symbol = 'o';
                self.ia_symbol = 'x'
                return True

    def jouer(self):
        tour_ia = self.choisir_camp()
        board = [' '] * 9

        while True:
            self.afficher_grille(board)

            # Vérifs Fin
            eval_finale = self.evaluer_etat(board)
            if eval_finale == 1000: print("🤖 L'IA A GAGNÉ !"); break
            if eval_finale == -1000: print("👏 TU AS GAGNÉ !"); break  # (Impossible théoriquement)
            if self.est_plein(board): print("🤝 MATCH NUL !"); break

            if tour_ia:
                coup = self.trouver_meilleur_coup(board)
                board[coup] = self.ia_symbol
                print(f"L'IA joue en {coup}")
            else:
                while True:
                    try:
                        case = int(input(f"Ton coup ({self.ICO[self.humain_symbol]}) : "))
                        if 0 <= case <= 8 and board[case] == ' ':
                            board[case] = self.humain_symbol
                            break
                    except:
                        pass

            tour_ia = not tour_ia


if __name__ == "__main__":
    # On lance directement la version invincible
    jeu = MorpionAlphaBeta()
    jeu.jouer()