import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

data = pd.read_csv("2025.csv", sep="|", decimal = ",", low_memory = False)
data["annee"] = 2025
data2= pd.read_csv("2024.csv", sep="|", decimal = ",", low_memory = False)
data2["annee"] = 2024
data = pd.concat([data, data2], ignore_index=True)
data2= pd.read_csv("2023.csv", sep="|", decimal = ",", low_memory = False)
data2["annee"] = 2023
data = pd.concat([data, data2], ignore_index=True)
data_gir = data[data["Code departement"].astype(str) == "33"].copy()
data_gir = data_gir[data_gir["Type local"].isin(["Appartement", "Maison"])]
data_gir = data_gir.dropna(subset=["Valeur fonciere", "Surface reelle bati", "Surface terrain"])
data_gir["Code postal"] = data_gir["Code postal"].astype(str)
col = ["annee", "Valeur fonciere", "Code postal", "Commune", "Type local", "Surface reelle bati", "Nombre pieces principales", "Surface terrain"]


dataset = data_gir[col]

if dataset["Valeur fonciere"].dtype == "object":
    dataset["Valeur fonciere"] = dataset["Valeur fonciere"].str.replace(',','.').astype(float)
dataset = dataset[(dataset["Valeur fonciere"] > 50000) & (dataset["Valeur fonciere"] < 1500000)]
dataset = dataset[(dataset["Surface reelle bati"] > 15) & (dataset["Surface reelle bati"] < 300)]
dataset = dataset[(dataset["Surface terrain"] <= 5000)]
col_stats = ["annee", 'Surface reelle bati', 'Surface terrain', 'Nombre pieces principales', "Commune", "Type local", "Code postal"]
X = dataset[col_stats]
X = pd.get_dummies(X, columns=['Commune', 'Type local', "Code postal"], drop_first=True)
y = dataset["Valeur fonciere"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


modele = LinearRegression()
modele.fit(X_train, y_train)
predictions = modele.predict(X_test)
erreur_moyenne = mean_absolute_error(y_test, predictions)
score_r2 = r2_score(y_test, predictions)
print(f"\n--- RÉSULTATS DE LA RÉGRESSION LINÉAIRE ---")
print(f"Erreur moyenne : {erreur_moyenne:,.2f} €")
print(f"Score de précision(R2): {score_r2:.2f} (Max = 1.0)")



modele_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modele_rf.fit(X_train, y_train)
predictions = modele_rf.predict(X_test)
erreur_moyenne = mean_absolute_error(y_test, predictions)
score_r2 = r2_score(y_test, predictions)
print(f"\n--- RÉSULTATS DU RANDOM FOREST ---")
print(f"Erreur moyenne : {erreur_moyenne:,.2f} €")
print(f"Score de précision(R2): {score_r2:.2f} (Max = 1.0)")

modele_xgb = XGBRegressor(
        n_estimators=200,
        learning_rate=0.3,
        subsample=0.8,
        n_jobs=-1,
        reg_alpha=10,
        reg_lambda=1,
        max_depth=7
        )
modele_xgb.fit(X_train, y_train)

predictions = modele_xgb.predict(X_test)
erreur_moyenne = mean_absolute_error(y_test, predictions)
print(f"\n--- RÉSULTATS DU xgboost ---")
print(f"Erreur moyenne : {erreur_moyenne:,.2f} €")
print(f"XGBoost R2 : {r2_score(y_test, predictions):.2f}")
