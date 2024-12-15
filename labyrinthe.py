from pyamaze import maze, agent, COLOR
import tkinter as tk
from tkinter import messagebox

class File:
    def __init__(self):
        self.f = []
        
    def file_vide(self):
        return len(self.f) == 0
    
    def emfiler(self, x):
        self.f.append(x)
        
    def defiler(self):
        if not self.file_vide():
            return self.f.pop(0)

class Graphe:
    def __init__(self, L, C):
        self.L = L
        self.C = C
        self.graphe = {}
        
    def ajouterNoeud(self, i, j):
        self.graphe[(i, j)] = []
        
    def ajouterArc(self, i, j, voisin_i, voisin_j, porte=False):
        if 0 <= voisin_i < self.L and 0 <= voisin_j < self.C:
            self.graphe[(i, j)].append(((voisin_i, voisin_j), porte))
            self.graphe[(voisin_i, voisin_j)].append(((i, j), porte))
        
    def listerArcs(self, i, j):
        return self.graphe[(i, j)]

class SearchLabyrinthe:
    def __init__(self, graphe):
        self.explores = {}
        self.accessibles = {}
        self.order = 0
        self.graphe = graphe  

    def succeuseur(self, etat):
        r = []
        l = self.graphe.listerArcs(etat[0], etat[1])
        for e, porte in l:
            if e not in self.explores and porte:
                r.append(e)
        return r
    
    def verifEtat(self, etat):
        if etat in self.explores:
            return "explore"
        elif etat in self.accessibles:
            return "accessible"
        else:
            return "inconnu"  

    def recherche_largeur(self, entree, sol):  
        f = File()
        f.emfiler(entree)
        chemin = {entree: None} 
        while not f.file_vide():
            etat = f.defiler()
            if etat == sol:
                solution = []
                while etat:
                    solution.append(etat)
                    etat = chemin[etat]
                solution.reverse()  
                return solution
            if self.verifEtat(etat) != "explore":
                self.explores[etat] = self.order
                self.order += 1
                succ = self.succeuseur(etat)
                for successeur in succ:
                    if successeur not in chemin:  
                        f.emfiler(successeur)
                        chemin[successeur] = etat  
                        self.accessibles[successeur] = self.order
                        self.order += 1
        return []

def creer_labyrinthe():
    labyrinthe = Graphe(3, 3)
    for i in range(3):
        for j in range(3):
            labyrinthe.ajouterNoeud(i, j)
            
    labyrinthe.ajouterArc(0, 0, 1, 0, True) 
    labyrinthe.ajouterArc(0, 0, 0, 1, True)  
    labyrinthe.ajouterArc(0, 1, 1, 1, True)  
    labyrinthe.ajouterArc(0, 1, 0, 2, True)  
    labyrinthe.ajouterArc(1, 0, 2, 0, True)  
    labyrinthe.ajouterArc(1, 1, 1, 2, True)  
    labyrinthe.ajouterArc(1, 2, 2, 2, True)
    
    return labyrinthe

def trouver_solution():
    labyrinthe = creer_labyrinthe()
    search_algo = SearchLabyrinthe(labyrinthe)
    path = search_algo.recherche_largeur((0, 0), (2, 2))
    
    # Affichage de la solution sous forme de liste
    if path:
        messagebox.showinfo("Solution trouvée", f"Le chemin est : {path}")
    else:
        messagebox.showinfo("Pas de solution", "Aucun chemin trouvé")

    # Déplacement de l'agent dans le labyrinthe
    a = agent(m, footprints=True)

    # Tracer le chemin trouvé dans le labyrinthe
    m.tracePath({a: path}, delay=100)

    # Affichage du labyrinthe avec l'agent parcourant le chemin
    m.run()

# Création de l'interface graphique avec tkinter
root = tk.Tk()
root.title("Labyrinthe Solver")

# Définir la taille de la fenêtre
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

# Bouton pour trouver la solution
solve_button = tk.Button(frame, text="Trouver la solution", command=trouver_solution)
solve_button.pack(pady=20)

# Création et affichage du labyrinthe avec pyamaze
m = maze(3, 3)
m.CreateMaze(loopPercent=100)
m.run()

# Afficher la fenêtre
root.mainloop()
