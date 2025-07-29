# 📊 Triskell Export Generator

## 📋 Sommaire
- [🎯 Présentation](#-présentation)
- [🌐 Utilisation Web](#-utilisation-web)
- [💻 Utilisation CLI](#-utilisation-cli)
- [📁 Structure des fichiers](#-structure-des-fichiers)

---

## 🎯 Présentation

Générateur automatique de rapports de temps Triskell au format PDF à partir d'un fichier Excel (.xlsx). L'outil gère les absences et produit une mise en page professionnelle fidèle au modèle Triskell.

**Fonctionnalités principales :**
- 📈 Lecture de fichiers Excel exportés depuis Triskell
- 🗓️ Gestion automatique des jours d'absence
- 📄 Génération PDF conforme à la charte Triskell
- 🌐 Interface web intuitive
- ⚡ Utilisation en ligne de commande

---

## 🌐 Utilisation Web

### Installation
```bash
# Cloner le projet
git clone <repository-url>
cd triskell_generator

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement
```bash
python3 start_web_interface.py
```

### Accès
Ouvrez votre navigateur sur : **http://localhost:5000**

### Utilisation
1. **Uploadez** votre fichier Excel (.xlsx) exporté de Triskell
2. **Saisissez** les jours d'absence (ex: "9,10,15" ou format JSON)
3. **Sélectionnez** le mois et l'année
4. **Générez** votre PDF en un clic !

---

## 💻 Utilisation CLI

### Commande de base
```bash
python triskell_interactive.py \
  --input-file "votre_fichier.xlsx" \
  --absence-dates "9,10,15" \
  --month 6 \
  --year 2025
```

### Options disponibles
- `--input-file` : Fichier Excel d'entrée
- `--absence-dates` : Jours d'absence (format: "9,10,15" ou JSON)
- `--month` : Mois cible (1-12)
- `--year` : Année cible

---

## 📁 Structure des fichiers

### Fichiers principaux
- **`start_web_interface.py`** 🚀 : Script de démarrage automatique avec vérification des dépendances
- **`web_interface.py`** 🌐 : Interface web Flask avec upload et génération PDF
- **`triskell_interactive.py`** ⚡ : Module principal de traitement des données et génération PDF
- **`requirements.txt`** 📦 : Dépendances Python (Flask, pandas, openpyxl, fpdf)

### Dossiers
- **`templates/`** 🎨 : Interface HTML
- **`uploads/`** 📁 : Stockage temporaire des fichiers uploadés

### Format attendu du fichier Excel
- **Ligne 1** : En-tête général
- **Ligne 2** : Date au format AAAA-MM (ex: 2025-06)
- **Ligne 3** : Colonnes des jours (ex: Lun 2, Mar 3, ...)
- **Lignes suivantes** : Données des projets

---

**🎯 Résultat :** PDF professionnel avec alternance de couleurs, totaux calculés et gestion des absences intégrée. 