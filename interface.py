import tkinter as tk
from tkinter import messagebox
import time
from Partie import Partie
from Evaluation import Evaluation  # On importe l'IA

class MorpionInterface:
    """
    Classe principale gérant l'Interface Graphique (GUI) du jeu Tic Tac Toe.
    Elle fait le lien entre l'utilisateur (clics, affichage), la logique (Partie) et l'IA (Evaluation).
    """

    def __init__(self):
        # 1. Création de la fenêtre racine (root)
        self.root = tk.Tk()
        
        # 2. Instanciation de la logique du jeu
        self.jeu = Partie()
        self.mode_actuel = None  # 1 = Joueur vs IA, 2 = IA vs IA
        self.tour_ia_vs_ia = "X" # Pour savoir quelle IA doit jouer en mode 2
        
        # --- Configuration de la fenêtre ---
        self.root.title("Tic Tac Toe - 2026")
        
        # Centrage de la fenêtre (600x800)
        self.centrer_fenetre(600, 800)
        
        # On empêche le redimensionnement pour conserver le design
        self.root.resizable(False, False)
        
        # Couleur de fond globale (Bleu nuit)
        self.root.configure(bg="#2c3e50")
        
        # --- Définition de la Charte Graphique (Styles) ---
        self.color_bg = "#2c3e50"       # Fond principal
        self.color_accent = "#1abc9c"   # Vert Émeraude (Joueur / X)
        self.color_ia = "#3498db"       # Bleu (IA / O)
        self.color_txt = "#ecf0f1"      # Blanc cassé (Texte)
        
        # Polices d'écriture
        self.font_titre = ("Helvetica", 36, "bold")
        self.font_status = ("Helvetica", 20, "bold")
        self.font_button = ("Helvetica", 14, "bold")
        
        # --- Création du Conteneur Principal ---
        self.frame_principale = tk.Frame(self.root, bg=self.color_bg)
        self.frame_principale.pack(expand=True, fill="both")
        
        # Lancement du Menu
        self.afficher_menu()
        
        # 3. Lancement de la boucle événementielle
        self.root.mainloop()

    def nettoyer_interface(self):
        """Supprime tous les widgets de la frame principale pour changer de page."""
        for widget in self.frame_principale.winfo_children():
            widget.destroy()

    def afficher_menu(self):
        """Affiche le menu principal."""
        self.nettoyer_interface()
        
        menu_container = tk.Frame(self.frame_principale, bg=self.color_bg)
        menu_container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(menu_container, text="MORPION", font=self.font_titre, 
                 fg="white", bg=self.color_bg).pack(pady=(0, 50))
        
        btn_style = {"font": self.font_button, "bg": self.color_accent, "fg": "white", 
                     "width": 25, "height": 2, "bd": 0, "cursor": "hand2", "activebackground": "#16a085"}
        
        tk.Button(menu_container, text="JOUEUR VS ORDINATEUR", 
                  command=self.setup_joueur_vs_ia, **btn_style).pack(pady=15)
        
        tk.Button(menu_container, text="ORDINATEUR VS ORDINATEUR", 
                  command=self.setup_ia_vs_ia, **btn_style).pack(pady=15)

    def setup_joueur_vs_ia(self):
        """Configuration Mode 1 : Saisie du pseudo."""
        self.mode_actuel = 1
        self.nettoyer_interface()
        
        setup_container = tk.Frame(self.frame_principale, bg=self.color_bg)
        setup_container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(setup_container, text="PRÉPAREZ-VOUS", font=("Helvetica", 12, "bold"),
                 fg=self.color_accent, bg=self.color_bg).pack()
        
        tk.Label(setup_container, text="Votre Pseudo", font=("Helvetica", 28, "bold"), 
                 fg="white", bg=self.color_bg).pack(pady=(5, 30))
        
        self.entry_pseudo = tk.Entry(setup_container, font=("Helvetica", 22), 
                                     justify="center", bd=0, highlightthickness=3,
                                     highlightbackground="#34495e", highlightcolor=self.color_accent)
        self.entry_pseudo.pack(pady=10, ipady=10)
        self.entry_pseudo.insert(0, "Joueur 1")
        self.entry_pseudo.focus_set()
        
        tk.Button(setup_container, text="LANCER LE MATCH", font=self.font_button, 
                  bg=self.color_accent, fg="white", width=20, height=2, bd=0,
                  command=self.lancer_jeu, cursor="hand2").pack(pady=40)

    def setup_ia_vs_ia(self):
        """Configuration Mode 2 : Lancement direct."""
        self.mode_actuel = 2
        self.entry_pseudo = type('obj', (object,), {'get': lambda: "IA Alpha"})()
        self.lancer_jeu()
        # On attend 1s avant de lancer la boucle des IA
        self.root.after(1000, self.boucle_ia_vs_ia)

    def lancer_jeu(self):
        """Initialisation de la grille graphique et logique."""
        self.nom_joueur = self.entry_pseudo.get()
        
        # Réinit logique
        self.jeu.reinitialiserGrille()
        self.tour_ia_vs_ia = "X" # Reset du tour IA
        
        self.nettoyer_interface()
        
        game_container = tk.Frame(self.frame_principale, bg=self.color_bg)
        game_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Label d'état
        self.label_status = tk.Label(game_container, text=f"Au tour de : {self.nom_joueur}", 
                                     font=self.font_status, fg=self.color_accent, bg=self.color_bg)
        self.label_status.pack(pady=(0, 40))
        
        # Grille
        self.grille_frame = tk.Frame(game_container, bg="#34495e", padx=10, pady=10)
        self.grille_frame.pack()
        
        self.boutons = []
        for r in range(3):
            ligne = []
            for c in range(3):
                btn = tk.Button(self.grille_frame, text=" ", font=("Helvetica", 45, "bold"), 
                                width=4, height=1, bg="white", fg=self.color_bg,
                                activebackground="#ecf0f1", bd=0, relief="flat",
                                command=lambda r=r, c=c: self.clic_sur_case(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)
                ligne.append(btn)
            self.boutons.append(ligne)

    # --- LOGIQUE DE JEU ET IA ---

    def verifier_fin_partie(self):
        """Vérifie si quelqu'un a gagné ou s'il y a match nul."""
        # On vérifie les victoires X et O
        if self.jeu.verifier_victoire("X"):
            gagnant = self.nom_joueur if self.mode_actuel == 1 else "IA Alpha (X)"
            self.afficher_popup_fin(f"VICTOIRE !\n{gagnant}")
            return True
        
        if self.jeu.verifier_victoire("O"):
            gagnant = "Ordinateur (O)" if self.mode_actuel == 1 else "IA Beta (O)"
            self.afficher_popup_fin(f"VICTOIRE !\n{gagnant}")
            return True
            
        # Match nul ? (si la grille est pleine)
        flat_board = [c for row in self.jeu.get_grille() for c in row]
        if " " not in flat_board:
            self.afficher_popup_fin("MATCH NUL !")
            return True
            
        return False

    def clic_sur_case(self, r, c):
        """Action du Joueur Humain (Mode 1)."""
        if self.mode_actuel == 1:
            grille = self.jeu.get_grille()
            
            # Si la case est vide
            if grille[r][c] == " ":
                # 1. Action Joueur (X)
                grille[r][c] = "X"
                self.boutons[r][c].config(text="X", fg=self.color_accent)
                
                # Vérif fin
                if self.verifier_fin_partie(): return
                
                # 2. Tour de l'IA (O)
                self.label_status.config(text="L'IA réfléchit...", fg=self.color_ia)
                self.root.after(500, self.jouer_tour_ia_vs_humain)

    def jouer_tour_ia_vs_humain(self):
        """L'IA (O) joue contre l'Humain (X)."""
        grille = self.jeu.get_grille()
        flat_board = [c for row in grille for c in row]
        
        # L'IA est O (Max), Humain est X (Min)
        cerveau = Evaluation(ai_player="O", human_player="X")
        idx = cerveau.trouver_meilleur_coup(flat_board)
        
        if idx != -1:
            r, c = idx // 3, idx % 3
            grille[r][c] = "O"
            self.boutons[r][c].config(text="O", fg=self.color_ia)
            self.label_status.config(text=f"Au tour de : {self.nom_joueur}", fg=self.color_accent)
            self.verifier_fin_partie()

    def boucle_ia_vs_ia(self):
        """Mode Spectateur : IA Alpha (X) vs IA Beta (O)."""
        if self.mode_actuel != 2: return

        grille = self.jeu.get_grille()
        flat_board = [c for row in grille for c in row]
        
        if self.tour_ia_vs_ia == "X":
            # Tour de IA Alpha
            self.label_status.config(text="IA Alpha (X) réfléchit...", fg=self.color_accent)
            # Pour Alpha: Elle est X (Max), l'autre est O (Min)
            cerveau = Evaluation(ai_player="X", human_player="O")
            idx = cerveau.trouver_meilleur_coup(flat_board)
            couleur = self.color_accent
            prochain_tour = "O"
            
        else:
            # Tour de IA Beta
            self.label_status.config(text="IA Beta (O) réfléchit...", fg=self.color_ia)
            # Pour Beta: Elle est O (Max), l'autre est X (Min)
            cerveau = Evaluation(ai_player="O", human_player="X")
            idx = cerveau.trouver_meilleur_coup(flat_board)
            couleur = self.color_ia
            prochain_tour = "X"

        # Application du coup
        if idx != -1:
            r, c = idx // 3, idx % 3
            grille[r][c] = self.tour_ia_vs_ia
            self.boutons[r][c].config(text=self.tour_ia_vs_ia, fg=couleur)
            
            # Vérif victoire avant de continuer
            if self.verifier_fin_partie(): return
            
            # Suite du match
            self.tour_ia_vs_ia = prochain_tour
            self.root.after(800, self.boucle_ia_vs_ia)

    # --- POPUP & UTILITAIRES ---

    def afficher_popup_fin(self, message_resultat):
        """Affiche le résultat final."""
        popup = tk.Toplevel(self.root)
        popup.title("Fin de partie")
        
        # Centrage popup
        w, h = 450, 420
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)
        
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.configure(bg="#34495e")
        popup.grab_set()

        tk.Label(popup, text="RÉSULTAT", font=("Helvetica", 14, "bold"), 
                 fg=self.color_accent, bg="#34495e").pack(pady=(30, 10))
        tk.Label(popup, text=message_resultat, font=("Helvetica", 16), 
                 fg="white", bg="#34495e", justify="center").pack(pady=20)

        btn_pop = {"font": ("Helvetica", 11, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        
        tk.Button(popup, text="🔄 RELANCER UNE PARTIE", bg=self.color_accent, fg="white",
                  command=lambda: [popup.destroy(), self.lancer_jeu()], **btn_pop).pack(pady=5)
        tk.Button(popup, text="🏠 MENU PRINCIPAL", bg="#95a5a6", fg="white",
                  command=lambda: [popup.destroy(), self.afficher_menu()], **btn_pop).pack(pady=5)
        tk.Button(popup, text="❌ QUITTER LE JEU", bg="#e74c3c", fg="white",
                  command=self.root.destroy, **btn_pop).pack(pady=5)

    def centrer_fenetre(self, w, h):
        """Centre la fenêtre sur l'écran."""
        ecran_w = self.root.winfo_screenwidth()
        ecran_h = self.root.winfo_screenheight()
        x = (ecran_w // 2) - (w // 2)
        y = (ecran_h // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")