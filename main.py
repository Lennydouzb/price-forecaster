import pandas as pd


data = pd.read_csv("2025.csv", sep="|", decimal = ",", low_memory = False)
data_gir = data[data["Code departement"].astype(str) == "33"].copy()
data_gir = data_gir[data_gir["Type local"].isin(["Appartement", "Maison"])]
data_gir = data_gir.dropna(subset=["Valeur fonciere", "Surface reelle bati", "Surface terrain"])
col = ["Valeur fonciere", "Code postal", "Commune", "Type local", "Surface reelle bati", "Nombre pieces principales", "Surface terrain"]

dataset = data_gir[col]
print (len(dataset))
print (dataset.head())