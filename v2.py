import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tkinter as tk
from tkinter import filedialog, messagebox
import csv

class AnalyseurSEO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Analyseur SEO")

        self.label_url = tk.Label(self.root, text="URL de la première page:")
        self.entry_url = tk.Entry(self.root, width=50)
        self.label_mots_cles = tk.Label(self.root, text="Mots-clés (séparés par des virgules):")
        self.entry_mots_cles = tk.Entry(self.root, width=50)
        self.bouton_analyser = tk.Button(self.root, text="Lancer l'analyse", command=self.lancer_analyse)

        self.label_url.pack(pady=5)
        self.entry_url.pack(pady=5)
        self.label_mots_cles.pack(pady=5)
        self.entry_mots_cles.pack(pady=5)
        self.bouton_analyser.pack(pady=10)

        self.fenetre_resultats = None

    def lancer_analyse(self):
        url = self.entry_url.get()
        mots_cles = [mot.strip() for mot in self.entry_mots_cles.get().split()]

        # Appel à la méthode d'audit SEO
        resultats = self.audit_seo(url, mots_cles)

        # Fermer la première fenêtre
        self.root.destroy()

        # Affichage des résultats dans une nouvelle fenetre
        self.afficher_resultats(url, resultats)

    def audit_seo(self, url, mots_cles):
        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur", f"Impossible d'obtenir le contenu de l'URL : {e}")
            return

        soup = BeautifulSoup(reponse.content, 'html.parser')

        # Recupération des liens sortants
        liens_sortants = [lien['href'] for lien in soup.find_all('a', href=True) if urlparse(lien['href']).netloc != urlparse(url).netloc]

        # Recupération des liens internes
        liens_internes = [lien['href'] for lien in soup.find_all('a', href=True) if urlparse(lien['href']).netloc == urlparse(url).netloc]

        # Recupération du pourcentage de balises alt sur les images
        balises_img = soup.find_all('img')
        total_balises_img = len(balises_img)
        balises_alt = [img.get('alt', '') for img in balises_img if img.get('alt', '')]
        pourcentage_balises_alt = (len(balises_alt) / total_balises_img) * 100 if total_balises_img > 0 else 0

        # Recupération des occurrences des mots-clés
        occurrences_mots_cles = {}
        for mot in soup.get_text().split():
            mot = mot.lower()
            if mot.isalpha() and len(mot) > 2:
                if mot in occurrences_mots_cles:
                    occurrences_mots_cles[mot] += 1
                else:
                    occurrences_mots_cles[mot] = 1

        mots_cles_tries = sorted(occurrences_mots_cles.items(), key=lambda x: x[1], reverse=True)
        top_mots_cles = [mot[0] for mot in mots_cles_tries[:3]]

        # Vérification si les mots clés de l'utilisateur sont parmi les 3 premiers
        classement_mots_cles_utilisateur = any(mot.lower() in [kw.lower() for kw in mots_cles] for mot in top_mots_cles)

        return {
            "urls": [url],
            "liens_sortants": [len(liens_sortants)],
            "liens_internes": [len(liens_internes)],
            "pourcentage_balises_alt": pourcentage_balises_alt,
            "top_mots_cles": top_mots_cles,
            "classement_mots_cles_utilisateur": classement_mots_cles_utilisateur
        }

    def afficher_resultats(self, url, resultats):
        self.fenetre_resultats = tk.Tk()
        self.fenetre_resultats.title("Résultats d'analyse")

        # Menu
        barre_menu = tk.Menu(self.fenetre_resultats)
        self.fenetre_resultats.config(menu=barre_menu)

        menu_fichier = tk.Menu(barre_menu, tearoff=0)
        barre_menu.add_cascade(label="Fichier", menu=menu_fichier)
        menu_fichier.add_command(label="Sauvegarder le rapport", command=lambda: self.sauvegarder_rapport(url, resultats))
        menu_fichier.add_command(label="Mettre à jour les mots clés parasites", command=self.mise_a_jour_mots_cles_parasites)

        for i, url in enumerate(resultats["urls"]):
            label_url = tk.Label(self.fenetre_resultats, text=f"URL: {url}")
            label_url.pack(pady=5)

            label_liens_sortants = tk.Label(self.fenetre_resultats, text=f"Nombre de liens sortants: {resultats['liens_sortants'][i]}")
            label_liens_sortants.pack(pady=5)

            label_liens_internes = tk.Label(self.fenetre_resultats, text=f"Nombre de liens internes: {resultats['liens_internes'][i]}")
            label_liens_internes.pack(pady=5)

            label_pourcentage_balises_alt = tk.Label(self.fenetre_resultats, text=f"% de balises alt: {resultats['pourcentage_balises_alt']:.2f}%")
            label_pourcentage_balises_alt.pack(pady=5)

            label_top_mots_cles = tk.Label(self.fenetre_resultats, text=f"Top 3 mots-clés: {', '.join(resultats['top_mots_cles'])}")
            label_top_mots_cles.pack(pady=5)

            classement_mots_cles_utilisateur = "Oui" if resultats['classement_mots_cles_utilisateur'] else "Non"
            label_classement_mots_cles_utilisateur = tk.Label(self.fenetre_resultats, text=f"Mots-clés de l'utilisateur parmi les 3 premiers: {classement_mots_cles_utilisateur}")
            label_classement_mots_cles_utilisateur.pack(pady=10)

    def sauvegarder_rapport(self, url, resultats):
        # Obtenez le nom de domaine de l'URL pour inclure dans le nom du fichier
        nom_domaine = urlparse(url).netloc.replace(".", "_")

        chemin_fichier = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt")],
            initialfile=f"Rapport d'analyse_{nom_domaine}"
        )

        if chemin_fichier:
            with open(chemin_fichier, 'w') as fichier:
                fichier.write("Rapport de référencement\n\n")

                for i, url in enumerate(resultats["urls"]):
                    fichier.write(f"URL: {url}\n")
                    fichier.write(f"Nombre de liens sortants: {resultats['liens_sortants'][i]}\n")
                    fichier.write(f"Nombre de liens internes: {resultats['liens_internes'][i]}\n")
                    fichier.write(f"% de balises alt: {resultats['pourcentage_balises_alt']:.2f}%\n")
                    fichier.write(f"Top 3 mots-clés: {', '.join(resultats['top_mots_cles'])}\n")
                    fichier.write(f"Mots-clés de l'utilisateur parmi les 3 premiers: {'Oui' if resultats['classement_mots_cles_utilisateur'] else 'Non'}\n\n")

            messagebox.showinfo("Sauvegarde réussie", "Le rapport a été sauvegardé avec succès.")

    def mise_a_jour_mots_cles_parasites(self):
        chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if chemin_fichier:
            try:
                with open(chemin_fichier, newline='') as fichier_csv:
                    lecteur_csv = csv.reader(fichier_csv)
                    mots_cles_parasites = [mot.lower() for ligne in lecteur_csv for mot in ligne if mot]
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier CSV : {e}")
                return

            messagebox.showinfo("Mise à jour réussie", "La liste des mots clés parasites a été mise à jour avec succès.")

if __name__ == "__main__":
    analyseur_seo = AnalyseurSEO()
    analyseur_seo.root.mainloop()
