import pandas as pd
import os

# ─────────────────────────────────────────────
# 1. Chemins des fichiers
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SCORES_PATH   = os.path.join(DATA_DIR, "scores.csv")
INSCRITS_PATH = os.path.join(DATA_DIR, "fact_inscrits.xls")
OUTPUT_PATH   = os.path.join(DATA_DIR, "edu_stat_master_dataset.csv")

# ─────────────────────────────────────────────
# 2. Chargement des fichiers
# ─────────────────────────────────────────────
print("[1/5] Chargement des fichiers...")

# Lecture en UTF-8 (encodage réel du fichier scores.csv)
df_scores = pd.read_csv(SCORES_PATH, sep=";", encoding="utf-8")
df_inscrits = pd.read_excel(INSCRITS_PATH)

print(f"  scores   : {df_scores.shape[0]} lignes | colonnes : {df_scores.columns.tolist()}")
print(f"  inscrits : {df_inscrits.shape[0]} lignes | colonnes : {df_inscrits.columns.tolist()}")

# ─────────────────────────────────────────────
# 2b. Nettoyage des données
# ─────────────────────────────────────────────
print("[2/5] Nettoyage des données...")

def clean_dataframe(df, name="df"):
    original_shape = df.shape

    # Supprimer les espaces en début/fin sur les colonnes texte
    str_cols = df.select_dtypes(include="str").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # Normaliser les noms de colonnes (strip + minuscules)
    df.columns = [c.strip() for c in df.columns]

    # Supprimer les lignes entièrement vides
    df = df.dropna(how="all")

    # Supprimer les doublons complets
    before_dedup = df.shape[0]
    df = df.drop_duplicates()
    after_dedup = df.shape[0]

    print(f"  [{name}] {original_shape} -> {df.shape} | doublons supprimés : {before_dedup - after_dedup}")
    return df

df_scores  = clean_dataframe(df_scores,  "scores")
df_inscrits = clean_dataframe(df_inscrits, "inscrits")

# Convertir les colonnes numériques avec virgule décimale → point
numeric_score_cols = [c for c in df_scores.columns if "Score" in c or "score" in c]
for col in numeric_score_cols:
    if df_scores[col].dtype == object:
        df_scores[col] = df_scores[col].str.replace(",", ".").astype(float)

# ─────────────────────────────────────────────
# 3. Préparation des inscrits
#    – Total H + F par établissement et par année
# ─────────────────────────────────────────────
df_inscrits["total_inscrits"] = df_inscrits["inscrits_f"] + df_inscrits["inscrits_m"]

inscrits_summary = (
    df_inscrits
    .groupby(["code_etablissement", "annee"])["total_inscrits"]
    .sum()
    .reset_index()
)

print(f"[3/5] Resume inscrits (par etablissement & annee) : {inscrits_summary.shape[0]} lignes")

# ─────────────────────────────────────────────
# 4. Ajout de la colonne code_etablissement dans scores
#    si elle n'existe pas encore on l'extrait du
#    début du Code_Filiere (les 3 premiers chiffres)
# ─────────────────────────────────────────────
if "code_etablissement" not in df_scores.columns:
    df_scores["code_etablissement"] = (
        df_scores["Code_Filiere"]
        .astype(str)
        .str.extract(r"^(\d{3})")  # ex: "101" depuis "1016"
        [0]
        .astype("Int64")
    )
    print("  + Colonne 'code_etablissement' generee depuis 'Code_Filiere'")

# ─────────────────────────────────────────────
# 5. Fusion (LEFT JOIN : on garde tous les scores)
# ─────────────────────────────────────────────
print("[4/5] Fusion en cours...")

# On croise avec chaque année disponible dans les inscrits
annees = inscrits_summary["annee"].unique()
frames = []

for annee in sorted(annees):
    inscrits_year = inscrits_summary[inscrits_summary["annee"] == annee][
        ["code_etablissement", "total_inscrits"]
    ].rename(columns={"total_inscrits": f"inscrits_{annee}"})

    frames.append(inscrits_year)

# Merge séquentiel pour avoir une colonne par année
from functools import reduce
inscrits_pivot = reduce(
    lambda left, right: pd.merge(left, right, on="code_etablissement", how="outer"),
    frames
)

master_df = pd.merge(df_scores, inscrits_pivot, on="code_etablissement", how="left")

print(f"  Resultat : {master_df.shape[0]} lignes | {master_df.shape[1]} colonnes")
print(f"  Colonnes finales : {master_df.columns.tolist()}")

# ─────────────────────────────────────────────
# 6. Gestion des valeurs manquantes (NaN)
#    Les gouvernorats sans donnees inscrits (ex: Gafsa)
#    recoivent la moyenne de la colonne pour ne pas
#    faire planter le modele Django / l'IA.
# ─────────────────────────────────────────────
cols_inscrits = [c for c in master_df.columns if c.startswith("inscrits_")]

nan_avant = master_df[cols_inscrits].isna().sum().sum()

for col in cols_inscrits:
    moyenne = master_df[col].mean()
    master_df[col] = master_df[col].fillna(round(moyenne, 0))

nan_apres = master_df[cols_inscrits].isna().sum().sum()
print(f"[NaN] {nan_avant} valeurs manquantes remplaces par la moyenne | restant : {nan_apres}")

# Afficher les lignes qui avaient des NaN (pour verification)
if nan_avant > 0:
    print("  Colonnes concernees :")
    for col in cols_inscrits:
        print(f"    {col} -> moyenne utilisee : {master_df[col].mean():.0f}")

# ─────────────────────────────────────────────
# 7. Sauvegarde (UTF-8, séparateur virgule)
# ─────────────────────────────────────────────
master_df.to_csv(OUTPUT_PATH, index=False, sep=",", encoding="utf-8")
print(f"[5/5] Fusion + nettoyage reussis ! Fichier sauvegarde : {OUTPUT_PATH}")
print(f"  Format : CSV UTF-8, separateur ','")
print(f"  Dimensions finales : {master_df.shape[0]} lignes x {master_df.shape[1]} colonnes")
