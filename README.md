# Générateur de Rapports Triskell

Ce projet permet de générer automatiquement des rapports de temps Triskell au format PDF à partir d'un fichier Excel (.xlsx), avec gestion des absences et une mise en page professionnelle fidèle au modèle Triskell.

## Fonctionnalités principales
- Lecture de fichiers Excel (.xlsx)
- Gestion des jours d'absence (saisie simple ou JSON)
- Génération d'un PDF conforme à la charte Triskell (tableaux, couleurs, alternance, totaux)
- Interface web moderne (Flask)
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
cd Python
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
- Les jours travaillés sont marqués dans "A1039 Socle IAAS Cloud"
- Les absences dans "EXT - Absence U TECH"
- Les week-ends sont automatiquement gérés
- Le PDF est coloré (bleu très clair, blanc, gris clair) et centré

## Personnalisation graphique
- Les couleurs et l'alternance sont codées pour coller au modèle Triskell
- Le code est épuré, seuls les scripts nécessaires sont conservés

## Nettoyage du dépôt
- Les anciens scripts de test ou d'analyse ont été supprimés pour plus de clarté
- Seuls les fichiers utiles à la génération du PDF et à l'interface web sont conservés

---

Pour toute question ou suggestion, ouvrez une issue ou contactez le mainteneur. 