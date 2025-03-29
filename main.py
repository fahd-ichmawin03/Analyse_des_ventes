import pandas as pd 
import matplotlib.pyplot as plt

#Liste des fichiers CSV : 
fichiers = [
    'Ventes_Janvier_2019.csv',
    'Ventes_Fevrier_2019.csv',
    'Ventes_Mars_2019.csv',
    'Ventes_Avril_2019.csv',
    'Ventes_Mai_2019.csv',
    'Ventes_Juin_2019.csv',
    'Ventes_Juillet_2019.csv',
    'Ventes_Aout_2019.csv',
    'Ventes_Septembre_2019.csv',
    'Ventes_Octobre_2019.csv',
    'Ventes_Novembre_2019.csv',
    'Ventes_Decembre_2019.csv'
]
# 1- 
# En fusionnant les fivhiers 
dataframes = [pd.read_csv(fichier) for fichier in fichiers]
ventes = pd.concat(dataframes, ignore_index=True)
ventes.to_csv('TouslesVentes.csv', index=False)
print("Les fichires sont bien rassembler")
# ---------------------------------------------------------------------------------------------------------
# 2- 
#pour supprimer les lignes dont des valeurs manquantes
ventes = ventes.dropna() 
#pour garder les lignes ou la date est bien définie
ventes["Date"] = pd.to_datetime(ventes["Date"], format='%m/%d/%y %H:%M', errors='coerce') 
# Suppression des lignes où la date n'a pas pu être convertie
ventes = ventes.dropna(subset=["Date"]) 
# ---------------------------------------------------------------------------------------------------------
# 3-
#Conversition des colonnes Quantite et Prix Unitaire en types appropriés
ventes["Quantite"] = pd.to_numeric(ventes["Quantite"], errors="coerce")
ventes["Prix Unitaire"] = pd.to_numeric(ventes["Prix Unitaire"], errors="coerce")
ventes["Chiffre d'affaires"] = ventes["Quantite"] * ventes["Prix Unitaire"]
# Extraire le mois si la colonne n'existe pas
if "Mois" not in ventes.columns:
    ventes["Mois"] = ventes["Date"].dt.month
# Calculer le chiffre d'affaires par mois
chiffre_affaires_par_mois = ventes.groupby("Mois")["Chiffre d'affaires"].sum()
# Identifier le mois avec le plus grand chiffre d'affaires
meilleur_mois = chiffre_affaires_par_mois.idxmax()
montant_max = chiffre_affaires_par_mois.max()
print(f"Le meilleur mois en chiffre d'affaires est le mois {meilleur_mois} avec {montant_max:.2f} Euro de ventes.")

#Visualisation du meilleur Moi en chiffre de ventes
plt.figure(figsize=(10, 6))
chiffre_affaires_par_mois.plot(kind='bar', color='skyblue')
plt.title("Chiffre de vente par mois")
plt.xlabel("Mois")
plt.ylabel("Chiffre de vente (€)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# ---------------------------------------------------------------------------------------------------------
# 4-
# Extraction de la ville depuis l'adresse de livraison
def extraire_ville(adresse):
    if pd.isna(adresse):
        return "Inconnue"
    parties = adresse.split(",")
    return parties[1].strip() if len(parties) > 1 else "Inconnue"
ventes["Ville"] = ventes["Adresse de livraison"].apply(extraire_ville)
# Extraction du mois depuis la date
ventes["Mois"] = pd.to_datetime(ventes["Date"], format='%d/%m/%Y').dt.month
# Calcul du chiffre d'affaires par mois et par ville
ventes_par_ville = ventes.groupby(["Mois", "Ville"])["Chiffre d'affaires"].sum().reset_index()
# Identifier la ville avec le plus de ventes chaque mois
ville_max_par_mois = ventes_par_ville.loc[ventes_par_ville.groupby("Mois")["Chiffre d'affaires"].idxmax()]
# Affichage des résultats
for index, row in ville_max_par_mois.iterrows():
    print(f"Mois {row['Mois']} : {row['Ville']} avec {row['Chiffre d\'affaires']:.2f} Euro de ventes.")
    
# Visualisation 
if "Ville" not in ventes.columns:
    ventes["Ville"] = ventes["Adresse de livraison"].apply(lambda x: x.split(",")[1].strip() if pd.notnull(x) and ',' in x else "Inconnu")
ville_ventes_mois = ventes.groupby(["Mois", "Ville"])["Chiffre d'affaires"].sum().reset_index()
ville_max_ventes = ville_ventes_mois.loc[ville_ventes_mois.groupby("Mois")["Chiffre d'affaires"].idxmax()]
plt.figure(figsize=(10, 6))
plt.bar(ville_max_par_mois["Mois"].astype(str), ville_max_par_mois["Chiffre d'affaires"], color='skyblue')
for i, row in ville_max_par_mois.iterrows():
    plt.text(row["Mois"], row["Chiffre d'affaires"], row["Ville"], ha='center', va='bottom', fontsize=9, rotation=45)
plt.xlabel("Mois")
plt.ylabel("Chiffre d'affaires (€)")
plt.title("Ville ayant le plus de ventes chaque mois")
plt.xticks(range(1, 13))  # Mois de 1 à 12
plt.tight_layout()
plt.show()
# ---------------------------------------------------------------------------------------------------------
# 5-
# EN cherchant le produit plus vendu tous les mois confendus
prd_pls = ventes.groupby("Produit")["Quantite"].sum().idxmax()
grd_quant = ventes.groupby("Produit")["Quantite"].sum().max()
print(f"Le produit le plus vendu est '{prd_pls}'avec une quantite de '{grd_quant}'.")

#Visualisation de la répartition des produit vendus
quant_p_prod = ventes.groupby("Produit")["Quantite"].sum()
quant_p_prod.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap="Set3")
plt.title("Graphe : Répartition des Produits Vendus", fontsize=20)
plt.ylabel("")  # Supprimer l'étiquette par défaut de l'axe Y
plt.tight_layout()
plt.show()
# ---------------------------------------------------------------------------------------------------------
# 6-
# Répartition des ventes par jour de la semaine (comprendrons les jours les plus performants).
# Extraction du jour de la semaine (0 = Lundi, 1 = Mardi, ..., 6 = Dimanche)
ventes["Jour Semaine"] = ventes["Date"].dt.dayofweek
# Calcul du chiffre d'affaires par jour de la semaine
chiffre_affaires_par_jour = ventes.groupby("Jour Semaine")["Chiffre d'affaires"].sum()
# Mappage des numéros de jours de la semaine à leur nom
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
chiffre_affaires_par_jour.index = [jours_semaine[j] for j in chiffre_affaires_par_jour.index]
# Affichage du jour le plus performant
jour_max = chiffre_affaires_par_jour.idxmax()
montant_max = chiffre_affaires_par_jour.max()
print(f"Le jour le plus performant en chiffre d'affaires est : {jour_max} avec {montant_max:.2f} Euro de ventes.")

# Diagramme circulaire de la répartition des ventes par jour de la semaine
plt.figure(figsize=(8, 8))
chiffre_affaires_par_jour.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap="Set3")
plt.title("Répartition des ventes par jour de la semaine", fontsize=15)
plt.ylabel("")  # Supprimer l'étiquette par défaut de l'axe Y
plt.tight_layout()
plt.show()
# ---------------------------------------------------------------------------------------------------------
# 7-
# Analyse par tranche horaire (identifions les heures de pointeQ d'achat).
# Extraire l'heure de la journée de la colonne "Date"
ventes["Heure"] = ventes["Date"].dt.hour
# Calculer le Chiffre d'affaires
ventes["Chiffre d'affaires"] = ventes["Quantite"] * ventes["Prix Unitaire"]
# Calcul du chiffre d'affaires par heure
ventes_par_heure = ventes.groupby("Heure")["Chiffre d'affaires"].sum()
# Identifier l'heure avec le chiffre d'affaires maximal
heure_max = ventes_par_heure.idxmax()
montant_max = ventes_par_heure.max()
print(f"L'heure de pointe d'achat est {int(heure_max)}:00 avec {montant_max:.2f} Euro de ventes.")

# Visualisation du chiffre d'affaires par heure avec un graphique en courbe
plt.figure(figsize=(10, 6))
plt.plot(ventes_par_heure.index, ventes_par_heure.values, marker='o', color='teal', linestyle='-', linewidth=2, markersize=8)
plt.title("Répartition des ventes par heure de la journée", fontsize=15)
plt.xlabel("Heure de la journée")
plt.ylabel("Chiffre d'affaires (€)")
# Formater l'axe des x (heures) pour afficher sous le format "HH:00"
plt.xticks(ticks=ventes_par_heure.index, labels=[f"{int(i)}:00" for i in ventes_par_heure.index])
plt.grid(True)
plt.tight_layout()
plt.show()


