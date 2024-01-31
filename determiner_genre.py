import csv
import os

print("Ce script permet, à partir d'un fichier CSV issu de Ligeo Gestion avec la configuration <unitid> / <unittitle>, "
      "de déterminer si une liste de personne est de genre féminin ou masculin.")

# Ouvrir les fichiers CSV d'entrée et de sortie avec un séparateur point-virgule et en UTF-8

def find_name(name, reference_list):
    """Prend chaque prénom individuellement sans prendre en compte le nom de famille"""
    # Convertir le nom en minuscules
    name_lower = name.lower()

    # Diviser le nom en parties en utilisant l'espace comme séparateur
    name_parts = name.split()

    # Parcourir chaque prénom de la liste de référence
    for reference_name in reference_list:
        # Vérifier si le prénom de la liste de référence est un mot entier dans le nom complet, à partir du deuxième mot
        if reference_name.lower() in [part.lower() for part in name_parts[1:]]:
            return True

    return False


# Obtenir le chemin absolu du répertoire du script
script_dir = os.path.dirname(__file__)

# Sélectionner le fichier CSV (input)
source = input("Entrer le nom du fichier CSV à traiter, avec son extension. Ce fichier doit se trouver dans le même répertoire que le script : ")
source = os.path.join(script_dir, source)
result = input("Comment souhaitez-vous nommer le fichier de résultat ?\n")
print("merci de patienter")

with open(source, 'r', encoding='utf-8', newline='') as source_file, open('prenoms_feminins.csv', 'r', encoding='utf-8', newline='') as female_file, open('prenoms_masculins.csv', 'r', encoding='utf-8', newline='') as male_file, open(f'{result}.csv', 'w', newline='', encoding='utf-8') as output_file:
    source_reader = csv.reader(source_file, delimiter=';')
    female_reader = csv.reader(female_file, delimiter=';')
    male_reader = csv.reader(male_file, delimiter=';')
    output_writer = csv.writer(output_file, delimiter=';')

    # Convertir le fichier de référence en une liste de chaînes en minuscules avec la fonction lower() appliquée à row[0] (la première colonne)
    female_list = [row[0].lower() for row in female_reader]
    male_list = [row[0].lower() for row in male_reader]

    # Parcourir chaque ligne de source_file, cellule de la colonne row[4]
    for source_row in source_reader:
        # La chaîne de caractères à examiner est dans la colonne row[4]
        source_string = source_row[4]

        # En-têtes
        if source_string == "intitule":
            output_writer.writerow([source_row[0],source_row[1],source_row[2],source_row[3],source_string, 'genre'])
        # Vérifier si le prénom est masculin
        elif find_name(source_string, male_list):
            output_writer.writerow([source_row[0],source_row[1],source_row[2],source_row[3],source_string, 'masculin'])
        # Vérifier si le prénom est féminin
        elif find_name(source_string, female_list):
            output_writer.writerow([source_row[0],source_row[1],source_row[2],source_row[3],source_string, 'féminin'])
        # Sinon, indiquer "à contrôler"
        else:
            output_writer.writerow([source_row[0],source_row[1],source_row[2],source_row[3],source_string, 'à contrôler'])

input("Programme terminé. Pressez Entrée.")
