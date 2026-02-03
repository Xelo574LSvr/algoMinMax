import tkinter as tk
from tkinter import ttk  # Pour la barre de progression
import time
from Partie import Partie
from Evaluation import Evaluation

class MorpionInterface:
    """
    Classe principale de l'interface graphique.
    Gère le menu, le jeu classique et la simulation rapide IA vs IA.
    """

    def __init__(self):
        """Initialise la fenêtre, les variables d'état et lance la boucle principale."""
        self.root = tk.Tk()
        self.jeu = Partie()
        self.mode_actuel = None
        
        # --- Variables d'état ---
        self.nom_joueur_cache = "Joueur 1"
        self.stats = {"Alpha": 0, "Beta": 0, "Nuls": 0, "Total": 0}
        
        # Variables pour la simulation
        self.target_games = 1
        self.games_played = 0

        # --- Configuration Fenêtre ---
        self.root.title("Tic Tac Toe - 2026")
        self.centrer_fenetre(600, 800)
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # --- Styles ---
        self.color_bg = "#2c3e50"
        self.color_accent = "#1abc9c"
        self.color_ia = "#3498db"
        self.color_txt = "#ecf0f1"
        self.font_titre = ("Helvetica", 36, "bold")
        self.font_status = ("Helvetica", 20, "bold")
        self.font_button = ("Helvetica", 14, "bold")
        
        self.frame_principale = tk.Frame(self.root, bg=self.color_bg)
        self.frame_principale.pack(expand=True, fill="both")
        
        self.afficher_menu()
        self.root.mainloop()
    
    def valider_nom(self, texte_futur):
        """Limite la saisie du pseudo à 20 caractères."""
        return len(texte_futur) <= 20

    def nettoyer_interface(self):
        """Supprime tous les widgets présents dans la frame principale."""
        for widget in self.frame_principale.winfo_children():
            widget.destroy()

    def centrer_fenetre(self, w, h):
        """Centre la fenêtre au milieu de l'écran."""
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # --- MENU ---

    def afficher_menu(self):
        """Affiche l'écran d'accueil du jeu."""
        self.nettoyer_interface()
        # Reset des stats à chaque retour au menu
        self.stats = {"Alpha": 0, "Beta": 0, "Nuls": 0, "Total": 0}

        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="MORPION", font=self.font_titre, fg="white", bg=self.color_bg).pack(pady=(0, 50))
        btn_style = {"font": self.font_button, "bg": self.color_accent, "fg": "white", "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        
        tk.Button(container, text="JOUEUR VS ORDINATEUR", command=self.setup_joueur_vs_ia, **btn_style).pack(pady=15)
        tk.Button(container, text="SIMULATION IA VS IA", command=self.setup_ia_vs_ia, **btn_style).pack(pady=15)

    def setup_joueur_vs_ia(self):
        """Page de configuration du pseudo pour le mode Humain vs IA."""
        self.mode_actuel = 1
        self.nettoyer_interface()
        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="Votre Pseudo", font=("Helvetica", 28, "bold"), fg="white", bg=self.color_bg).pack(pady=(5, 30))
        
        # Enregistrement de la validation (limite 30 car.)
        vcmd = (self.root.register(self.valider_nom), '%P')
        
        self.entry_pseudo = tk.Entry(container, font=("Helvetica", 22), justify="center",
                                     validate="key", validatecommand=vcmd)
        self.entry_pseudo.pack(pady=10, ipady=10)
        self.entry_pseudo.insert(0, "Joueur 1")
        
        # On utilise sauvegarder_et_lancer pour capter le nom avant que le widget soit détruit
        tk.Button(container, text="LANCER", font=self.font_button, bg=self.color_accent, fg="white", width=20, 
                  command=self.sauvegarder_et_lancer).pack(pady=40)

    def sauvegarder_et_lancer(self):
        """Sauvegarde le pseudo et lance le jeu contre l'IA."""
        self.nom_joueur_cache = self.entry_pseudo.get()
        self.lancer_jeu_humain()

    # --- NOUVELLE PAGE DE CONFIGURATION IA VS IA ---

    def setup_ia_vs_ia(self):
        """Page pour choisir le nombre de simulations."""
        self.mode_actuel = 2
        self.nettoyer_interface()
        
        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="SIMULATION", font=("Helvetica", 28, "bold"), fg="white", bg=self.color_bg).pack(pady=(0, 20))
        tk.Label(container, text="Nombre de parties à jouer :", font=("Helvetica", 14), fg="#bdc3c7", bg=self.color_bg).pack(pady=10)
        
        self.slider_games = tk.Scale(container, from_=1, to=1000, orient="horizontal", length=400, 
                                     bg=self.color_bg, fg=self.color_accent, troughcolor="#34495e",
                                     highlightthickness=0, font=("Helvetica", 12, "bold"))
        self.slider_games.set(10) 
        self.slider_games.pack(pady=20)
        
        btn_style = {"font": self.font_button, "bg": self.color_accent, "fg": "white", "width": 20, "height": 2, "bd": 0, "cursor": "hand2"}
        tk.Button(container, text="LANCER SIMULATION", command=self.lancer_simulation_rapide, **btn_style).pack(pady=30)

    # --- GESTION DU JEU HUMAIN ---

    def lancer_jeu_humain(self):
        """Initialise la grille graphique pour le mode Humain vs IA."""
        self.nettoyer_interface()
        self.jeu.reinitialiserGrille()
        self.jeu.choixJoueurDepart()
        joueur1_commence = self.jeu.get_isTourJoueur()
        
        if joueur1_commence:
            self.symbole_humain, self.symbole_ia = "X", "O"
            txt_status, col_status = f"Au tour de : {self.nom_joueur_cache} (X)", self.color_accent
        else:
            self.symbole_humain, self.symbole_ia = "O", "X"
            txt_status, col_status = "L'IA (X) commence...", self.color_ia

        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        self.label_status = tk.Label(container, text=txt_status, font=self.font_status, fg=col_status, bg=self.color_bg)
        self.label_status.pack(pady=(0, 40))
        
        self.grille_frame = tk.Frame(container, bg="#34495e", padx=10, pady=10)
        self.grille_frame.pack()
        
        self.boutons = []
        for r in range(3):
            ligne = []
            for c in range(3):
                btn = tk.Button(self.grille_frame, text=" ", font=("Helvetica", 45, "bold"), width=4, height=1, bg="white", fg=self.color_bg,
                                command=lambda r=r, c=c: self.clic_sur_case(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)
                ligne.append(btn)
            self.boutons.append(ligne)

        if not joueur1_commence:
            self.root.after(800, self.jouer_tour_ia_vs_humain)

    def clic_sur_case(self, r, c):
        """Gère le clic de l'utilisateur sur une case."""
        if self.mode_actuel == 1:
            if "L'IA" in self.label_status.cget("text"): return
            if self.jeu.jouer_coup(r, c, self.symbole_humain):
                self.boutons[r][c].config(text=self.symbole_humain, fg=self.color_accent if self.symbole_humain == "X" else self.color_ia)
                if self.verifier_fin_humain(): return
                self.label_status.config(text=f"L'IA ({self.symbole_ia}) réfléchit...", fg=self.color_ia if self.symbole_ia == "O" else self.color_accent)
                self.root.after(500, self.jouer_tour_ia_vs_humain)

    def jouer_tour_ia_vs_humain(self):
        """Réponse de l'IA via l'algorithme d'évaluation."""
        coord = self.jeu.jouer_coup_ia(self.symbole_ia, self.symbole_humain)
        if coord:
            r, c = coord
            color = self.color_accent if self.symbole_ia == "X" else self.color_ia
            self.boutons[r][c].config(text=self.symbole_ia, fg=color)
            if self.verifier_fin_humain(): return
            col = self.color_accent if self.symbole_humain == "X" else self.color_ia
            self.label_status.config(text=f"Au tour de : {self.nom_joueur_cache} ({self.symbole_humain})", fg=col)

    def verifier_fin_humain(self):
        """Vérifie si la partie joueur vs IA est finie."""
        if self.jeu.verifier_victoire(self.symbole_humain):
            self.afficher_popup_fin(f"VICTOIRE !\n{self.nom_joueur_cache}")
            return True
        if self.jeu.verifier_victoire(self.symbole_ia):
            self.afficher_popup_fin(f"VICTOIRE !\nL'IA")
            return True
        flat = [c for row in self.jeu.get_grille() for c in row]
        if " " not in flat:
            self.afficher_popup_fin("MATCH NUL !")
            return True
        return False

    # --- SIMULATION RAPIDE ---

    def lancer_simulation_rapide(self):
        """Prépare l'écran de chargement pour la simulation."""
        self.target_games = self.slider_games.get()
        self.games_played = 0
        self.nettoyer_interface()
        
        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="CALCUL EN COURS...", font=("Helvetica", 24, "bold"), fg=self.color_accent, bg=self.color_bg).pack(pady=20)
        self.lbl_progress = tk.Label(container, text=f"Partie 0 / {self.target_games}", font=("Helvetica", 16), fg="white", bg=self.color_bg)
        self.lbl_progress.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(container, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=20)
        
        self.root.after(100, self.executer_batch_simulation)

    def executer_batch_simulation(self):
        """Exécute les parties par petits lots pour ne pas figer la fenêtre."""
        batch_size = 5
        for _ in range(batch_size):
            if self.games_played >= self.target_games: break
            
            self.jeu.reinitialiserGrille()
            self.jeu.choixJoueurDepart()
            j1_commence = self.jeu.get_isTourJoueur()
            symbole_alpha = "X" if j1_commence else "O"
            
            fini, tour_actuel = False, "X"
            while not fini:
                flat = [case for ligne in self.jeu.get_grille() for case in ligne]
                if " " not in flat:
                    self.stats["Nuls"] += 1
                    fini = True
                    break
                
                adversaire = "O" if tour_actuel == "X" else "X"
                cerveau = Evaluation(ai_player=tour_actuel, human_player=adversaire)
                idx = cerveau.trouver_meilleur_coup(flat)
                
                if idx != -1:
                    r, c = idx // 3, idx % 3
                    self.jeu.jouer_coup(r, c, tour_actuel)
                    if self.jeu.verifier_victoire(tour_actuel):
                        fini = True
                        if tour_actuel == symbole_alpha: self.stats["Alpha"] += 1
                        else: self.stats["Beta"] += 1
                    tour_actuel = adversaire
                else:
                    fini = True
                    self.stats["Nuls"] += 1
            
            self.games_played += 1
            self.stats["Total"] += 1

        self.lbl_progress.config(text=f"Partie {self.games_played} / {self.target_games}")
        self.progress_bar["value"] = (self.games_played / self.target_games) * 100
        self.root.update_idletasks()
        
        if self.games_played < self.target_games:
            self.root.after(10, self.executer_batch_simulation)
        else:
            self.afficher_popup_fin("SIMULATION TERMINÉE")

    # --- POPUP FINALE ---

    def afficher_popup_fin(self, msg):
        """Affiche le résultat et le bilan (si mode simulation)."""
        popup = tk.Toplevel(self.root)
        popup.title("Bilan")
        w, h = 450, 420
        x = (self.root.winfo_screenwidth()//2) - (w//2)
        y = (self.root.winfo_screenheight()//2) - (h//2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.configure(bg="#34495e")
        popup.grab_set()

        tk.Label(popup, text="RÉSULTAT", font=("Helvetica", 14, "bold"), fg=self.color_accent, bg="#34495e").pack(pady=(20, 5))
        tk.Label(popup, text=msg, font=("Helvetica", 16), fg="white", bg="#34495e").pack(pady=10)
        
        # --- CONDITION : On affiche les stats uniquement en mode Simulation (IA VS IA) ---
        if self.mode_actuel == 2:
            txt_stats = f"Alpha: {self.stats['Alpha']} | Beta: {self.stats['Beta']} | Nuls: {self.stats['Nuls']}\n(Total: {self.stats['Total']})"
            tk.Label(popup, text=txt_stats, font=("Helvetica", 12), fg="#bdc3c7", bg="#34495e").pack(pady=(0, 20))
        else:
            # Petit espace vide pour garder l'esthétique en mode Humain
            tk.Label(popup, text="", bg="#34495e").pack(pady=10)

        btn_s = {"font": ("Helvetica", 11), "width": 25, "bg": self.color_accent, "fg": "white"}
        
        # Commande de rejouer dynamique selon le mode
        if self.mode_actuel == 1:
            cmd_rejouer = lambda: [popup.destroy(), self.lancer_jeu_humain()]
            txt_btn = "REJOUER"
        else:
            cmd_rejouer = lambda: [popup.destroy(), self.setup_ia_vs_ia()]
            txt_btn = "NOUVELLE SIMULATION"

        tk.Button(popup, text=txt_btn, command=cmd_rejouer, **btn_s).pack(pady=5)
        
        btn_s["bg"] = "#95a5a6"
        tk.Button(popup, text="MENU", command=lambda: [popup.destroy(), self.afficher_menu()], **btn_s).pack(pady=5)
        
        btn_s["bg"] = "#e74c3c"
        tk.Button(popup, text="QUITTER", command=self.root.destroy, **btn_s).pack(pady=5)