# triskell_export_generator

Ce projet permet de générer automatiquement des rapports de temps Triskell au format PDF à partir d'un fichier Excel (.xlsx), avec gestion des absences et une mise en page professionnelle fidèle au modèle Triskell.

## Fonctionnalités principales
- Lecture du fichiers Excel (.xlsx) exporté depuis Triskel pour la 1ère semaine du mois voulu
- Gestion des jours d'absence (saisie simple ou JSON)
- Génération d'un PDF conforme à la charte Triskell (tableaux, couleurs, alternance, totaux)
- Interface web (Flask)
- Utilisation possible en ligne de commande

## Dépendances
- pandas
- openpyxl
- fpdf

Installez-les avec :
```bash
pip install -r requirements.txt
```

## Utilisation recommandée : Interface Web

```bash
cd triskell_export_generator
python web_interface.py
```

Puis ouvrez votre navigateur sur : http://localhost:5000

## Utilisation en ligne de commande

```bash
python triskell_interactive.py \
  --input-file "votre_fichier.xlsx" \
  --absence-dates "9,10,15" \
  --month 6 \
  --year 2025
```

## Structure attendue du fichier Excel
- Ligne 1 : En-tête général
- Ligne 2 : Date au format AAAA-MM (ex : 2025-06)
- Ligne 3 : Colonnes des jours (ex : Lun 2, Mar 3, ...)
- Lignes suivantes : Données des projets

## Exemple de résultat
- Les jours travaillés sont tous marqués à 1 par défaut
- Les absences sont définies par l'utilisateur et donc non comptées

## Personnalisation graphique
- Les couleurs et l'alternance sont codées pour coller au modèle Triskell
---

Pour toute question ou suggestion, ouvrez une issue ou contactez le mainteneur. 