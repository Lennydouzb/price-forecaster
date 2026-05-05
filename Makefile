# --- Variables ---
PYTHON = python3
PIP = pip
TARGET = main.py

# Liste des fichiers CSV attendus
DATA_FILES = 2025.csv 2024.csv 2023.csv

# URLs (Remplace les liens ici)
URL_2025 = "https://www.data.gouv.fr/api/1/datasets/r/902db087-b0eb-4cbb-a968-0b499bde5bc4"
URL_2024 = "https://www.data.gouv.fr/api/1/datasets/r/99a26050-b94f-4ffc-9eb0-73ed28a895d1"
URL_2023 = "https://www.data.gouv.fr/api/1/datasets/r/025b9d29-8efb-40bb-8ce6-5bddf97a4e51"

# --- Règles ---

# Règle par défaut : installe les dépendances, télécharge les données et lance le script
all: install download run

# Installation des bibliothèques nécessaires
install:
	$(PIP) install pandas Scikit-learn xgboost

# Téléchargement des fichiers (seulement s'ils n'existent pas)
download: $(DATA_FILES)

2025.csv:
	@echo "Téléchargement des données 2025..."
	curl -L $(URL_2025) -o 2025.zip
	unzip -p 2025.zip > 2025.csv
	rm 2025.zip

2024.csv:
	@echo "Téléchargement des données 2024..."
	curl -L $(URL_2024) -o 2024.zip
	unzip -p 2024.zip > 2024.csv
	rm 2024.zip

2023.csv:
	@echo "Téléchargement des données 2023..."
	curl -L $(URL_2023) -o 2023.zip
	unzip -p 2023.zip > 2023.csv
	rm 2023.zip

# Exécution du script Python
run:
	$(PYTHON) $(TARGET)

# Nettoyage des fichiers téléchargés
clean:
	rm -f $(DATA_FILES)

.PHONY: all install download run clean
