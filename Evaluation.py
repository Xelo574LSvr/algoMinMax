import sys


class Evaluation:

    def __init__(self, ai_player, human_player):
        self.MAX_PLAYER = ai_player
        self.MIN_PLAYER = human_player

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