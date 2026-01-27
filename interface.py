import tkinter as tk
from tkinter import messagebox
import time
from Partie import Partie  

class MorpionInterface:
    """
    Classe principale gérant l'Interface Graphique (GUI) du jeu Morpion.
    Elle fait le lien entre l'utilisateur (clics, affichage) et la logique interne (Partie).
    """

    def __init__(self):
        # 1. Création de la fenêtre racine (root)
        # C'est la base de toute application Tkinter. Elle contient tous les autres widgets.
        self.root = tk.Tk()
        
        # 2. Instanciation de la logique du jeu
        # On crée un objet 'Partie' qui gardera en mémoire l'état de la grille (données).
        self.jeu = Partie()
        self.mode_actuel = None  # Variable pour savoir si on joue "Joueur vs IA" (1) ou "IA vs IA" (2)
        
        # --- Configuration de la fenêtre (Centrage Dynamique) ---
        self.root.title("Tic Tac Toe - 2026")  # Titre de la fenêtre
        
        # Définition des dimensions souhaitées pour l'application
        largeur_fenetre = 600
        hauteur_fenetre = 800
        
        # Récupération des dimensions réelles de l'écran de l'utilisateur
        largeur_ecran = self.root.winfo_screenwidth()
        hauteur_ecran = self.root.winfo_screenheight()
        
        # Calcul mathématique pour trouver le point (x, y) du coin supérieur gauche
        # afin que la fenêtre soit parfaitement centrée.
        pos_x = (largeur_ecran // 2) - (largeur_fenetre // 2)
        pos_y = (hauteur_ecran // 2) - (hauteur_fenetre // 2)
        
        # Application de la géométrie : format "LargeurxHauteur+PositionX+PositionY"
        self.root.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{pos_x}+{pos_y}")
        
        # On empêche le redimensionnement pour éviter de casser le design (responsive design limité)
        self.root.resizable(False, False)
        
        # Couleur de fond globale de la fenêtre (Bleu nuit)
        self.root.configure(bg="#2c3e50")
        
        # --- Définition de la Charte Graphique (Styles) ---
        # On stocke les couleurs et polices dans des variables pour faciliter les modifications futures
        self.color_bg = "#2c3e50"       # Fond principal
        self.color_accent = "#1abc9c"   # Vert Émeraude (Actions principales / Joueur)
        self.color_ia = "#3498db"       # Bleu (Actions de l'ordinateur)
        self.color_txt = "#ecf0f1"      # Blanc cassé (Texte)
        
        # Polices d'écriture
        self.font_titre = ("Helvetica", 36, "bold")
        self.font_status = ("Helvetica", 20, "bold")
        self.font_button = ("Helvetica", 14, "bold")
        
        # --- Création du Conteneur Principal ---
        # On utilise une Frame qui prend toute la place pour y déposer nos pages (Menu, Jeu, etc.)
        self.frame_principale = tk.Frame(self.root, bg=self.color_bg)
        self.frame_principale.pack(expand=True, fill="both")
        
        # Lancement de la première vue : Le Menu
        self.afficher_menu()
        
        # 3. Lancement de la boucle événementielle (Main Loop)
        # C'est ce qui maintient la fenêtre ouverte et attend les clics de souris.
        # Le programme reste bloqué ici tant qu'on ne ferme pas la fenêtre.
        self.root.mainloop()

    def nettoyer_interface(self):
        """
        Supprime tous les widgets présents dans la frame principale.
        Utile pour passer d'une page à l'autre (ex: du Menu vers le Jeu) sans superposer les éléments.
        """
        for widget in self.frame_principale.winfo_children():
            widget.destroy()

    def afficher_menu(self):
        """
        Affiche la page d'accueil avec les boutons de sélection de mode.
        """
        self.nettoyer_interface()
        
        # Création d'un conteneur invisible pour centrer le contenu verticalement et horizontalement
        menu_container = tk.Frame(self.frame_principale, bg=self.color_bg)
        # 'place' permet un positionnement absolu ou relatif. Ici, on place le centre du frame (anchor="center")
        # à 50% de la largeur (relx=0.5) et 50% de la hauteur (rely=0.5) du parent.
        menu_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Titre du jeu
        tk.Label(menu_container, text="MORPION", font=self.font_titre, 
                 fg="white", bg=self.color_bg).pack(pady=(0, 50))
        
        # Dictionnaire de style pour uniformiser les boutons du menu
        btn_style = {"font": self.font_button, "bg": self.color_accent, "fg": "white", 
                     "width": 25, "height": 2, "bd": 0, "cursor": "hand2", "activebackground": "#16a085"}
        
        # Bouton Mode 1 : Joueur vs IA
        tk.Button(menu_container, text="JOUEUR VS ORDINATEUR", 
                  command=self.setup_joueur_vs_ia, **btn_style).pack(pady=15)
        
        # Bouton Mode 2 : IA vs IA
        tk.Button(menu_container, text="ORDINATEUR VS ORDINATEUR", 
                  command=self.setup_ia_vs_ia, **btn_style).pack(pady=15)

    def setup_joueur_vs_ia(self):
        """
        Écran de configuration pour le Mode 1 (Saisie du pseudo).
        """
        self.mode_actuel = 1
        self.nettoyer_interface()
        
        # Conteneur centré pour le formulaire
        setup_container = tk.Frame(self.frame_principale, bg=self.color_bg)
        setup_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Labels d'instructions
        tk.Label(setup_container, text="PRÉPAREZ-VOUS", font=("Helvetica", 12, "bold"),
                 fg=self.color_accent, bg=self.color_bg).pack()
        
        tk.Label(setup_container, text="Votre Pseudo", font=("Helvetica", 28, "bold"), 
                 fg="white", bg=self.color_bg).pack(pady=(5, 30))
        
        # Champ de saisie (Entry) stylisé avec une bordure colorée
        self.entry_pseudo = tk.Entry(setup_container, font=("Helvetica", 22), 
                                     justify="center", bd=0, highlightthickness=3,
                                     highlightbackground="#34495e", highlightcolor=self.color_accent)
        self.entry_pseudo.pack(pady=10, ipady=10) # ipady augmente la hauteur interne du champ
        self.entry_pseudo.insert(0, "Joueur 1")   # Valeur par défaut
        self.entry_pseudo.focus_set()             # Donne le focus clavier directement au champ
        
        # Bouton pour lancer la partie
        tk.Button(setup_container, text="LANCER LE MATCH", font=self.font_button, 
                  bg=self.color_accent, fg="white", width=20, height=2, bd=0,
                  command=self.lancer_jeu, cursor="hand2").pack(pady=40)

    def setup_ia_vs_ia(self):
        """
        Configuration pour le Mode 2. Pas de saisie de pseudo nécessaire.
        """
        self.mode_actuel = 2
        # On crée un faux objet 'entry_pseudo' avec une méthode 'get' pour simuler la saisie d'un nom
        # Cela permet de réutiliser la méthode 'lancer_jeu' sans modification.
        self.entry_pseudo = type('obj', (object,), {'get': lambda: "IA Alpha"})()
        
        # On lance l'affichage de la grille
        self.lancer_jeu()
        
        # On programme le début de la simulation IA après 1 seconde (1000 ms) pour ne pas être trop brutal
        self.root.after(1000, self.boucle_ia_vs_ia)

    def lancer_jeu(self):
        """
        Initialise l'affichage de la grille de jeu (3x3).
        """
        # Récupération du nom du joueur (ou de l'IA selon le mode)
        self.nom_joueur = self.entry_pseudo.get()
        
        # Réinitialisation des données logiques (dans la classe Partie)
        self.jeu.reinitialiserGrille()
        self.nettoyer_interface()
        
        # Conteneur centré pour le jeu
        game_container = tk.Frame(self.frame_principale, bg=self.color_bg)
        game_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Label d'état (qui joue ?) - Dynamique
        self.label_status = tk.Label(game_container, text=f"Au tour de : {self.nom_joueur}", 
                                     font=self.font_status, fg=self.color_accent, bg=self.color_bg)
        self.label_status.pack(pady=(0, 40))
        
        # Frame spécifique pour la grille (fond plus sombre)
        self.grille_frame = tk.Frame(game_container, bg="#34495e", padx=10, pady=10)
        self.grille_frame.pack()
        
        # Création de la matrice de boutons (3x3)
        self.boutons = []
        for r in range(3): # Boucle pour les lignes (row)
            ligne = []
            for c in range(3): # Boucle pour les colonnes (column)
                # Création d'un bouton pour chaque case
                btn = tk.Button(self.grille_frame, text=" ", font=("Helvetica", 45, "bold"), 
                                width=4, height=1, bg="white", fg=self.color_bg,
                                activebackground="#ecf0f1", bd=0, relief="flat",
                                # On utilise lambda pour passer les coordonnées r et c à la fonction lors du clic
                                command=lambda r=r, c=c: self.clic_sur_case(r, c))
                # Placement en grille
                btn.grid(row=r, column=c, padx=5, pady=5)
                ligne.append(btn)
            self.boutons.append(ligne)

    def clic_sur_case(self, r, c):
        """
        Gestionnaire d'événement : Appelé quand l'utilisateur clique sur une case (Mode 1).
        """
        if self.mode_actuel == 1:
            # Vérifie si la case est vide avant de jouer
            if self.boutons[r][c]["text"] == " ":
                # Mise à jour visuelle pour le joueur (X rouge)
                self.boutons[r][c].config(text="X", fg="#e74c3c")
                
                # Changement du message de statut
                self.label_status.config(text="Au tour de : Ordinateur", fg=self.color_ia)
                
                # TODO: Ici, il faudra appeler la logique de l'ordinateur pour qu'il réponde.

    def boucle_ia_vs_ia(self):
        """
        Simulation du déroulement d'une partie Ordinateur vs Ordinateur.
        """
        if self.mode_actuel == 2:
            # Mesure du temps pour l'indicateur de performance
            start_time = time.time()
            
            # Mise à jour visuelle pour montrer que ça "réfléchit"
            self.label_status.config(text="Analyse de l'IA en cours...", fg=self.color_ia)
            
            # TODO: Remplacer ceci par l'appel réel aux algorithmes MinMax des deux IA
            
            # Calcul du temps écoulé en millisecondes
            perf_ms = (time.time() - start_time) * 1000
            
            # Construction du message de fin
            message = f"MATCH TERMINÉ\n\nVictoire de IA Alpha\nPerformance : {perf_ms:.2f} ms"
            
            # Affichage de la popup de fin après un délai de 1.5 secondes pour l'effet visuel
            self.root.after(1500, lambda: self.afficher_popup_fin(message))

    def afficher_popup_fin(self, message_resultat):
        """
        Affiche une fenêtre modale (au-dessus du jeu) avec le résultat et les options.
        """
        # Toplevel crée une nouvelle fenêtre indépendante de la principale
        popup = tk.Toplevel(self.root)
        popup.title("Fin de partie")
        popup.geometry("450x420")
        
        # Calcul pour centrer la popup par rapport à la fenêtre principale
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        # On décale légèrement (+75, +150) pour l'esthétique
        popup.geometry(f"+{main_x + 75}+{main_y + 150}")
        
        popup.configure(bg="#34495e")
        
        # grab_set() est crucial : il empêche de cliquer sur la fenêtre principale tant que la popup est ouverte
        popup.grab_set()

        # Affichage du texte de résultat
        tk.Label(popup, text="RÉSULTAT", font=("Helvetica", 14, "bold"), 
                 fg=self.color_accent, bg="#34495e").pack(pady=(30, 10))
        tk.Label(popup, text=message_resultat, font=("Helvetica", 16), 
                 fg="white", bg="#34495e", justify="center").pack(pady=20)

        # Style commun pour les boutons de la popup
        btn_pop = {"font": ("Helvetica", 11, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        
        # Bouton Rejouer : Ferme la popup et relance le jeu
        tk.Button(popup, text="🔄 RELANCER UNE PARTIE", bg=self.color_accent, fg="white",
                  command=lambda: [popup.destroy(), self.lancer_jeu()], **btn_pop).pack(pady=5)
        
        # Bouton Menu : Ferme la popup et retourne au menu
        tk.Button(popup, text="🏠 MENU PRINCIPAL", bg="#95a5a6", fg="white",
                  command=lambda: [popup.destroy(), self.afficher_menu()], **btn_pop).pack(pady=5)
        
        # Bouton Quitter : Ferme complètement l'application
        tk.Button(popup, text="❌ QUITTER LE JEU", bg="#e74c3c", fg="white",
                  command=self.root.destroy, **btn_pop).pack(pady=5)