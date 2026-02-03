import tkinter as tk
from tkinter import messagebox
import time
from Partie import Partie
from Evaluation import Evaluation

class MorpionInterface:
    """
    Classe principale de l'interface graphique.
    Elle gère l'affichage, les interactions utilisateur et le chef d'orchestre du jeu.
    """

    def __init__(self):
        """Initialise la fenêtre, les variables d'état et lance la boucle principale."""
        
        # En Python, 'self' représente l'objet lui-même. C'est comme 'this' en Java/C++.
        # On stocke tout dans 'self' pour que les variables soient accessibles partout dans la classe.
        
        # Création de la fenêtre principale (la racine)
        self.root = tk.Tk()
        
        # On instancie la logique du jeu (le cerveau qui ne gère pas l'affichage)
        self.jeu = Partie()
        self.mode_actuel = None
        
        # --- Variables d'état ---
        self.nom_joueur_cache = "Joueur 1"
        
        # Ces variables changent à chaque partie selon le tirage au sort.
        # Elles permettent de savoir qui joue "X" et qui joue "O".
        self.symbole_humain = "X" 
        self.symbole_ia = "O"
        self.tour_ia_vs_ia = "X" # Dans ce code, X commence TOUJOURS. On décide juste QUI est X.

        # --- Configuration de la Fenêtre ---
        self.root.title("Tic Tac Toe - 2026")
        # Appel de notre fonction perso pour centrer
        self.centrer_fenetre(600, 800)
        # On empêche de redimensionner la fenêtre (Largeur, Hauteur) -> (False, False)
        self.root.resizable(False, False)
        # On met la couleur de fond
        self.root.configure(bg="#2c3e50")
        
        # --- Styles (Constantes graphiques) ---
        # On définit les couleurs ici pour ne pas avoir à les changer partout si on change d'avis
        self.color_bg = "#2c3e50"
        self.color_accent = "#1abc9c"   # Couleur pour X (Premier joueur)
        self.color_ia = "#3498db"       # Couleur pour O (Second joueur)
        self.color_txt = "#ecf0f1"
        self.font_titre = ("Helvetica", 36, "bold")
        self.font_status = ("Helvetica", 20, "bold")
        self.font_button = ("Helvetica", 14, "bold")
        
        # --- Conteneur Principal ---
        # Une Frame est une "boîte" vide dans laquelle on va mettre nos boutons/textes
        self.frame_principale = tk.Frame(self.root, bg=self.color_bg)
        # pack() est une façon de placer l'objet. expand=True signifie "prend toute la place dispo"
        self.frame_principale.pack(expand=True, fill="both")
        
        # On lance l'affichage du menu
        self.afficher_menu()
        
        # C'est la ligne la plus importante : elle lance la boucle infinie qui attend les clics.
        # Le code s'arrête ici tant qu'on ne ferme pas la fenêtre.
        self.root.mainloop()

    def nettoyer_interface(self):
        """Supprime tous les widgets de la fenêtre pour changer d'écran."""
        # winfo_children() retourne la liste de tout ce qu'il y a dans la frame (boutons, labels...)
        for widget in self.frame_principale.winfo_children():
            widget.destroy() # On les détruit un par un

    def centrer_fenetre(self, w, h):
        """Calcule la position x,y pour centrer la fenêtre sur l'écran."""
        # On récupère la taille de l'écran de l'utilisateur
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        # On applique la géométrie : "LargeurxHauteur+PositionX+PositionY"
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # --- MENU ---

    def afficher_menu(self):
        """Affiche les boutons du menu principal."""
        self.nettoyer_interface()
        
        # On crée une sous-boîte pour centrer verticalement les boutons
        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        # place() permet un positionnement précis. relx=0.5 signifie "50% de la largeur" (milieu)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Label = Texte simple
        tk.Label(container, text="MORPION", font=self.font_titre, fg="white", bg=self.color_bg).pack(pady=(0, 50))
        
        # Dictionnaire d'options pour ne pas répéter le style des boutons
        btn_style = {"font": self.font_button, "bg": self.color_accent, "fg": "white", "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        
        # command=... indique quelle fonction appeler quand on clique
        tk.Button(container, text="JOUEUR VS ORDINATEUR", command=self.setup_joueur_vs_ia, **btn_style).pack(pady=15)
        tk.Button(container, text="ORDINATEUR VS ORDINATEUR", command=self.setup_ia_vs_ia, **btn_style).pack(pady=15)

    def setup_joueur_vs_ia(self):
        """Affiche le formulaire de saisie du pseudo."""
        self.mode_actuel = 1
        self.nettoyer_interface()
        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="Votre Pseudo", font=("Helvetica", 28, "bold"), fg="white", bg=self.color_bg).pack(pady=(5, 30))
        
        # Entry = Champ de saisie texte
        self.entry_pseudo = tk.Entry(container, font=("Helvetica", 22), justify="center")
        self.entry_pseudo.pack(pady=10, ipady=10)
        self.entry_pseudo.insert(0, "Joueur 1") # Texte par défaut
        
        # Le bouton appelle 'sauvegarder_et_lancer' pour enregistrer le nom avant de détruire le champ
        tk.Button(container, text="LANCER", font=self.font_button, bg=self.color_accent, fg="white", width=20, 
                  command=self.sauvegarder_et_lancer).pack(pady=40)

    def setup_ia_vs_ia(self):
        """Lance directement le mode IA vs IA."""
        self.mode_actuel = 2
        self.nom_joueur_cache = "IA Alpha"
        # On lance directement, pas besoin d'attendre ici car lancer_jeu gère le timer
        self.lancer_jeu()

    def sauvegarder_et_lancer(self):
        """Récupère le texte du champ de saisie avant de lancer le jeu."""
        self.nom_joueur_cache = self.entry_pseudo.get()
        self.lancer_jeu()

    # --- CŒUR DU JEU ---

    def lancer_jeu(self):
        """Initialise la grille, fait le tirage au sort et démarre la partie."""
        self.nettoyer_interface()
        
        # 1. Reset logique (On remet la grille à vide dans le "cerveau")
        self.jeu.reinitialiserGrille()
        
        # 2. Tirage au sort (Nouveau tirage à chaque lancement !)
        self.jeu.choixJoueurDepart() 
        joueur1_commence = self.jeu.get_isTourJoueur()
        
        # 3. Attribution des Rôles (Celui qui gagne le tirage devient X et commence)
        if self.mode_actuel == 1:
            if joueur1_commence:
                # L'humain a gagné le tirage, il est X
                self.symbole_humain = "X"
                self.symbole_ia = "O"
                txt_status = f"Au tour de : {self.nom_joueur_cache} (X)"
                col_status = self.color_accent
            else:
                # L'IA a gagné le tirage, elle est X
                self.symbole_humain = "O"
                self.symbole_ia = "X"
                txt_status = "L'IA (X) commence..."
                col_status = self.color_ia
        else:
            # Mode IA vs IA
            self.tour_ia_vs_ia = "X" # On remet le tour à X
            if joueur1_commence:
                self.nom_ia_x = "IA Alpha"
                self.nom_ia_o = "IA Beta"
            else:
                self.nom_ia_x = "IA Beta"
                self.nom_ia_o = "IA Alpha"
            
            txt_status = f"{self.nom_ia_x} (X) réfléchit..."
            col_status = self.color_accent

        # 4. Affichage Grille
        container = tk.Frame(self.frame_principale, bg=self.color_bg)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.label_status = tk.Label(container, text=txt_status, font=self.font_status, fg=col_status, bg=self.color_bg)
        self.label_status.pack(pady=(0, 40))
        
        self.grille_frame = tk.Frame(container, bg="#34495e", padx=10, pady=10)
        self.grille_frame.pack()
        
        self.boutons = []
        # Double boucle pour créer une grille 3x3 de boutons
        for r in range(3):
            ligne = []
            for c in range(3):
                # On utilise une fonction lambda pour capturer r et c.
                # Sinon, tous les boutons croiraient qu'ils sont la case (2,2).
                btn = tk.Button(self.grille_frame, text=" ", font=("Helvetica", 45, "bold"), 
                                width=4, height=1, bg="white", fg=self.color_bg,
                                command=lambda r=r, c=c: self.clic_sur_case(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)
                ligne.append(btn)
            self.boutons.append(ligne)

        # 5. Démarrage automatique des IA
        if self.mode_actuel == 1 and not joueur1_commence:
            # Si c'est l'IA (X) qui commence contre l'humain
            # after(800, ...) attend 800ms avant de lancer la fonction, pour ne pas jouer instantanément
            self.root.after(800, self.jouer_tour_ia_vs_humain)
            
        elif self.mode_actuel == 2:
            # Si c'est IA vs IA, on lance la boucle immédiatement
            self.root.after(800, self.boucle_ia_vs_ia)

    # --- LOGIQUE DE JEU ---

    def clic_sur_case(self, r, c):
        """Gère le clic du joueur humain sur une case."""
        # Uniquement pour le mode Humain
        if self.mode_actuel == 1:
            # On vérifie que c'est bien le tour de l'humain en lisant le texte affiché
            if "L'IA" in self.label_status.cget("text") or "Ordinateur" in self.label_status.cget("text"):
                return # On bloque le clic, ce n'est pas son tour !
            
            # On tente de jouer le coup dans le "cerveau" (Partie)
            if self.jeu.jouer_coup(r, c, self.symbole_humain):
                # Si valide, on met à jour l'affichage
                self.boutons[r][c].config(text=self.symbole_humain, fg=self.color_accent if self.symbole_humain == "X" else self.color_ia)
                
                # On vérifie si la partie est finie
                if self.verifier_fin_partie(): return
                
                # Si non, on lance le tour de l'IA
                self.label_status.config(text=f"L'IA ({self.symbole_ia}) réfléchit...", fg=self.color_ia if self.symbole_ia == "O" else self.color_accent)
                self.root.after(500, self.jouer_tour_ia_vs_humain)

    def jouer_tour_ia_vs_humain(self):
        """Demande à l'IA de calculer et jouer son coup."""
        # On appelle l'IA via la classe Partie
        coord = self.jeu.jouer_coup_ia(self.symbole_ia, self.symbole_humain, type_ia=1)
        
        if coord:
            r, c = coord
            color = self.color_accent if self.symbole_ia == "X" else self.color_ia
            self.boutons[r][c].config(text=self.symbole_ia, fg=color)
            
            if self.verifier_fin_partie(): return
            
            # On rend la main au joueur
            txt = f"Au tour de : {self.nom_joueur_cache} ({self.symbole_humain})"
            col = self.color_accent if self.symbole_humain == "X" else self.color_ia
            self.label_status.config(text=txt, fg=col)

    def boucle_ia_vs_ia(self):
        """Boucle récursive qui fait jouer les deux IA l'une après l'autre."""
        if self.mode_actuel != 2: return
        # Sécurité supplémentaire si fin de partie
        if self.verifier_fin_partie(): return 

        grille = self.jeu.get_grille()
        flat_board = [c for row in grille for c in row]

        # On détermine qui joue (X ou O)
        joueur_courant = self.tour_ia_vs_ia
        joueur_adverse = "O" if joueur_courant == "X" else "X"

        type_ia_a_utiliser = 1 if joueur_courant == "X" else 2
        
        # Mise à jour texte
        nom_ia = self.nom_ia_x if joueur_courant == "X" else self.nom_ia_o
        col = self.color_accent if joueur_courant == "X" else self.color_ia
        self.label_status.config(text=f"{nom_ia} ({joueur_courant}) réfléchit...", fg=col)

        # On passe le type d'IA à la méthode
        coord = self.jeu.jouer_coup_ia(joueur_courant, joueur_adverse, type_ia=type_ia_a_utiliser)
        

        if coord:
            r, c = coord
            self.jeu.jouer_coup(r, c, joueur_courant)
            self.boutons[r][c].config(text=joueur_courant, fg=col)
            
            if self.verifier_fin_partie(): return

            # Changement de tour
            self.tour_ia_vs_ia = joueur_adverse
            # On boucle : la fonction s'appelle elle-même après 800ms
            self.root.after(800, self.boucle_ia_vs_ia)

    def verifier_fin_partie(self):
        """Vérifie les conditions de victoire ou nul et affiche la popup si besoin."""
        # Victoire X
        if self.jeu.verifier_victoire("X"):
            if self.mode_actuel == 1:
                nom = self.nom_joueur_cache if self.symbole_humain == "X" else "L'IA"
            else:
                nom = self.nom_ia_x
            self.afficher_popup_fin(f"VICTOIRE !\n{nom} (X)")
            return True
        
        # Victoire O
        if self.jeu.verifier_victoire("O"):
            if self.mode_actuel == 1:
                nom = self.nom_joueur_cache if self.symbole_humain == "O" else "L'IA"
            else:
                nom = self.nom_ia_o
            self.afficher_popup_fin(f"VICTOIRE !\n{nom} (O)")
            return True
        
        # Match Nul (si aucune case vide)
        flat = [c for row in self.jeu.get_grille() for c in row]
        if " " not in flat:
            self.afficher_popup_fin("MATCH NUL !")
            return True
            
        return False

    def afficher_popup_fin(self, msg):
        """Affiche une fenêtre modale avec le résultat."""
        # Toplevel crée une fenêtre au-dessus de la principale
        popup = tk.Toplevel(self.root)
        popup.title("Fin")
        w, h = 450, 420
        x = (self.root.winfo_screenwidth()//2) - (w//2)
        y = (self.root.winfo_screenheight()//2) - (h//2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.configure(bg="#34495e")
        # grab_set empêche de cliquer sur la fenêtre principale tant que la popup est ouverte
        popup.grab_set()

        tk.Label(popup, text="RÉSULTAT", font=("Helvetica", 14, "bold"), fg=self.color_accent, bg="#34495e").pack(pady=30)
        tk.Label(popup, text=msg, font=("Helvetica", 16), fg="white", bg="#34495e").pack(pady=20)
        
        btn_s = {"font": ("Helvetica", 11), "width": 25, "bg": self.color_accent, "fg": "white"}
        
        # Le bouton REJOUER relance tout proprement via lancer_jeu
        tk.Button(popup, text="REJOUER", command=lambda:[popup.destroy(), self.lancer_jeu()], **btn_s).pack(pady=5)
        
        btn_s["bg"] = "#95a5a6"
        tk.Button(popup, text="MENU", command=lambda:[popup.destroy(), self.afficher_menu()], **btn_s).pack(pady=5)
        
        btn_s["bg"] = "#e74c3c"
        tk.Button(popup, text="QUITTER", command=self.root.destroy, **btn_s).pack(pady=5)