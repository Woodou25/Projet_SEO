import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


# # Etape 1 : Saisie du texte
# def saisie_texte_utilisateur():
#     texte_utilisateur = input("Entrer du texte : ")
#     return texte_utilisateur
#
# texte_saisi = saisie_texte_utilisateur()
#
# def occurrence_mots(texte):
#     mots = texte.split()
#     dictionnaire_occurrences = {}
#     for mot in mots:
#         mot = mot.lower()
#         if mot in dictionnaire_occurrences:
#             dictionnaire_occurrences[mot] += 1
#         else:
#             dictionnaire_occurrences[mot] = 1
#     liste_triee = sorted(dictionnaire_occurrences.items(), key=lambda x: x[1], reverse=True)
#     return liste_triee
#
# resultat_occurrence_mots = occurrence_mots(texte_saisi)
# # print(resultat_occurrence_mots)
#
#
#
# # Etape 2 : Suppression des Mots Parasites
# def supprimer_mots_parasites(occurrences, mots_parasites):
#     texte_filtre = [item for item in occurrences if item[0] not in mots_parasites]
#     return texte_filtre
#
# liste_mots_parasites = ['le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'en', 'à', 'avec', 'sur', 'sous', 'par', 'pour', 'et', 'ou', 'car', 'donc', 'mais', 'si', 'que', 'qui', 'quoi', 'où', 'comment', 'quand', 'pourquoi', 'combien', 'cela']
# resultat_filtre = supprimer_mots_parasites(resultat_occurrence_mots, liste_mots_parasites)
# # print(resultat_filtre)
#
#
#
# # Etape 3 : Récupération des mots parasites depuis un fichier CSV
# def recuperer_mots_parasites_depuis_csv(parasite):
#     mots_parasites = []
#     with open(parasite, newline='') as csvfile:
#         lecteur_csv = csv.reader(csvfile)
#         for ligne in lecteur_csv:
#             mots_parasites.extend(ligne)
#     return mots_parasites
#
# nom_fichier = 'parasite.csv'
# mots_parasites = recuperer_mots_parasites_depuis_csv(nom_fichier)
#
#
#
# # # Etape 4 : Appelez les fonctions
#
# # Etape 1
# resultat_etape1 = occurrence_mots(texte_saisi)
# print("\n-----------Etape 1:-----------")
# print(resultat_etape1)
#
# # Etape 3
# resultat_etape3 = recuperer_mots_parasites_depuis_csv(nom_fichier)
# print("\n-----------Etape 3:-----------")
# print(resultat_etape3)
#
# # Etape 2
# resultat_etape2 = supprimer_mots_parasites(resultat_etape1, resultat_etape3)
# print("\n-----------Etape 2:-----------")
# print(resultat_etape2)



# Etape 5 : Suppression des balises HTML
def supprimer_balises_html(texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    texte_sans_balises = soup.get_text()
    return texte_sans_balises

# # print("\n-----------Etape 5:-----------")
# html_texte = input("Entrer chaine HTML : ")
# texte_sans_balises = supprimer_balises_html(html_texte)
# # print(texte_sans_balises)



# Etape 6 : Récupération des valeurs des attributs
def obtenir_valeurs_attributs(contenu_html, nom_tag, nom_attribut):
    soup = BeautifulSoup(contenu_html, 'html.parser')
    valeurs_tag = []
    for tag in soup.find_all(nom_tag):
        if tag.has_attr(nom_attribut):
            valeurs_tag.append(tag[nom_attribut])
    return valeurs_tag


# Etape 8 : Extraction du nom de domaine
def extraire_domaine_de_url(url):
    url_analysé = urlparse(url)
    return url_analysé.netloc



# Etape 9 : Filtrage des URLs par domaine
def filtrer_urls_par_domaine(nom_domaine, liste_urls):
    domaine_urls = []
    autres_urls = []

    for url in liste_urls:
        if extraire_domaine_de_url(url) == nom_domaine:
            domaine_urls.append(url)
        else:
            autres_urls.append(url)

    return domaine_urls, autres_urls



# Etape 10 : Récupération du contenu HTML depuis une URL
def obtenir_contenu_html(url):
    réponse = requests.get(url)
    return réponse.text



# Etape 11 : Audit SEO
def audit_seo(url):
    # Etape 10
    contenu_html = obtenir_contenu_html(url)

    # Etape 6
    valeurs_alt = obtenir_valeurs_attributs(contenu_html, 'img', 'alt')
    valeurs_href = obtenir_valeurs_attributs(contenu_html, 'a', 'href')

    # # # Etape 7
    # print("\nValeurs Alt pour les balises img:", valeurs_alt)
    # print("Valeurs Href pour les balises a:", valeurs_href)

    # Etape 8
    domaine = extraire_domaine_de_url(url)

    # Etape 9
    domaine_urls, autres_urls = filtrer_urls_par_domaine(domaine, valeurs_href)

    # Etape 11
    print("-----------Debut de l'audit-----------")
    print("\nRésultats de l'audit SEO pour :", url)
    print("")
    print("Domaine:", domaine)
    print("")
    print("Valeurs Alt pour les balises img:", valeurs_alt)
    print("Nombre de liens entrants:", len(domaine_urls))
    print("Liens entrants:", domaine_urls)
    print("Nombre de liens sortants:", len(autres_urls))
    print("Liens sortants:", autres_urls)

    print("\nMots clé et leurs occurrences:")

    # Nombre d'occurrences de chaque mot dans le contenu HTML
    Nombre_de_mots = {}
    for mots in contenu_html.split():
        mots = mots.lower()
        if mots.isalpha() and len(mots) > 2:
            if mots in Nombre_de_mots:
                Nombre_de_mots[mots] += 1
            else:
                Nombre_de_mots[mots] = 1

    # Affichage des 3 premières valeurs d’occurrences
    Nombre_de_mots_Trié = sorted(Nombre_de_mots.items(), key=lambda x: x[1], reverse=True)
    for i in range(3):
        if i < len(Nombre_de_mots_Trié):
            print(f"{Nombre_de_mots_Trié[i][0]}: {Nombre_de_mots_Trié[i][1]} occurrences")


# Audit SEO avec une URL spécifique
url_à_auditer = input("Entrez l'URL de la page à analyser : ")
audit_seo(url_à_auditer)

print("")
print("-----------Fin de l'audit-----------")