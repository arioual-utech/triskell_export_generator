# Triskell Export Generator

Générateur de rapports de temps Triskell au format PDF, **100 % côté navigateur**, sans serveur.
Hébergé sur GitHub Pages : [https://arioual-utech.github.io/triskell_generator](https://arioual-utech.github.io/triskell_generator)

---

## Fonctionnalités

- Sélection du mois et de l'année cibles
- Calendrier interactif pour marquer les jours d'absence
- Sélecteurs rapides : tous les jours de semaine, tous les lundis/vendredis, tous les weekends
- Sélection par plage de jours
- Génération et téléchargement du PDF en un clic, directement dans le navigateur
- Aucune donnée envoyée sur un serveur — tout est local

---

## Utilisation

Ouvrir l'application dans le navigateur (GitHub Pages ou fichier local), puis :

1. Sélectionner le **mois** et l'**année**
2. Cliquer sur les jours d'absence dans le calendrier (ou utiliser les sélecteurs rapides)
3. Cliquer sur **Générer le PDF** — le fichier `Triskell_MM-YYYY.pdf` est téléchargé automatiquement

---

## Déploiement GitHub Pages

### Activation (à faire une seule fois)

1. Aller dans **Settings** du dépôt → section **Pages**
2. Choisir la source : branche `master` (ou `main`), dossier `/ (root)`
3. Sauvegarder — GitHub Pages sera disponible en quelques secondes à l'adresse :
   `https://<organisation>.github.io/<nom-du-repo>/`

### Mise à jour

Chaque push sur la branche configurée déclenche automatiquement un nouveau déploiement.

---

## Format du PDF généré

Le PDF suit le format Triskell standard :

- **Tableau récapitulatif** : totaux A1039 (jours travaillés) et EXT (jours d'absence)
- **Matrice des jours** : grille mensuelle avec une ligne par type (travail / absence)
  - Week-ends : 0 partout
  - Jours d'absence sélectionnés : A1039 = 0, EXT = 1
  - Jours travaillés : A1039 = 1, EXT = 0

---

## Structure du projet

```
index.html              Application complète (HTML + CSS + JS, sans dépendances installées)
requirements.txt        Dépendances Python (ancienne version Flask — non utilisée par GitHub Pages)
web_interface.py        Ancienne interface Flask (conservée pour référence)
triskell_interactive.py Ancienne logique Python (conservée pour référence)
start_web_interface.py  Ancien script de démarrage Flask (conservé pour référence)
templates/index.html    Ancien template Jinja2 (conservé pour référence)
```

### Dépendances embarquées (CDN, aucune installation)

| Bibliothèque | Rôle |
|---|---|
| [Font Awesome 6](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css) | Icônes |
| [jsPDF 2.5.1](https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js) | Génération PDF côté client |

---

## Ancienne version (Flask / CLI)

L'ancienne version nécessitait Python et un serveur local.

### Lancement serveur local

```bash
pip install -r requirements.txt
python3 start_web_interface.py
# → http://localhost:5000
```

### CLI

```bash
python triskell_interactive.py \
  --input-file "votre_fichier.xlsx" \
  --absence-dates "9,10,15" \
  --month 6 \
  --year 2025
```
