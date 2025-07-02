import pandas as pd
from datetime import datetime, timedelta
import calendar
from fpdf import FPDF
import os
import re
import argparse
import json
import sys

def parse_absence_dates(absence_dates_str):
    """Parse les dates d'absence depuis une chaîne JSON ou une liste de dates"""
    try:
        if isinstance(absence_dates_str, str):
            if absence_dates_str.startswith('['):
                # Format JSON array
                return json.loads(absence_dates_str)
            else:
                # Format simple: "9,10,15" ou "9, 10, 15"
                return [int(d.strip()) for d in absence_dates_str.split(',')]
        elif isinstance(absence_dates_str, list):
            return absence_dates_str
        else:
            return []
    except Exception as e:
        print(f"Erreur lors du parsing des dates d'absence: {e}")
        return []

def process_triskell_data(fichier_entree, absence_dates=None, mois_cible=None, annee_cible=None):
    """
    Traite les données Triskell avec les paramètres donnés
    
    Args:
        fichier_entree (str): Chemin vers le fichier Excel
        absence_dates (list): Liste des jours d'absence (ex: [9, 10, 15])
        mois_cible (int): Mois cible (1-12)
        annee_cible (int): Année cible
    """
    
    if absence_dates is None:
        absence_dates = []
    
    print(f"Traitement du fichier: {fichier_entree}")
    print(f"Jours d'absence: {absence_dates}")
    print(f"Mois/Année cible: {mois_cible}/{annee_cible}")
    
    # --- Configuration et lecture du fichier d'entrée ---
    try:
        df_raw = pd.read_excel(fichier_entree, header=None, skiprows=2)
        print(f"Fichier '{fichier_entree}' lu avec succès (en ignorant les 2 premières lignes).")
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_entree}' n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue lors de la lecture du fichier : {e}")
        return None

    # --- Extraction des informations clés du fichier Excel ---
    try:
        df_header = pd.read_excel(fichier_entree, header=None, nrows=3)
        
        # Extraction de la date si non fournie
        if mois_cible is None or annee_cible is None:
            line_with_date = str(df_header.iloc[1, 0]) if len(df_header) > 1 else ""
            match_date = re.search(r'\d{4}-\d{2}', line_with_date)
            if match_date:
                date_str = match_date.group(0)
                annee_cible = int(date_str.split('-')[0])
                mois_cible = int(date_str.split('-')[1])
                print(f"Mois et année extraits du fichier : {calendar.month_name[mois_cible]} {annee_cible}")
            else:
                print("Utilisation des valeurs par défaut: Juin 2025")
                annee_cible = 2025
                mois_cible = 6
    except Exception as e:
        print(f"Erreur lors de l'extraction de la date: {e}. Utilisation par défaut Juin 2025.")
        annee_cible = 2025
        mois_cible = 6

    # --- Extraction des colonnes de jours ---
    jours_colonnes_raw = df_header.iloc[2].astype(str).tolist() if len(df_header) > 2 else []
    jours_colonnes_dict = {}
    
    for i, col_name in enumerate(jours_colonnes_raw):
        col_name = col_name.strip()
        match = re.match(r'([A-Za-z]+)\s(\d+)', col_name)
        if match:
            jour_abbr = match.group(1)
            jour_num = int(match.group(2))
            jours_colonnes_dict[col_name] = {'index': i, 'jour_abbr': jour_abbr, 'jour_num': jour_num}

    if not jours_colonnes_dict:
        print("Aucune colonne de jour trouvée. Vérifiez la structure du fichier.")
        return None

    print(f"Colonnes de jours identifiées: {list(jours_colonnes_dict.keys())}")

    # --- Création de la structure du calendrier ---
    num_jours_mois = calendar.monthrange(annee_cible, mois_cible)[1]
    jours_calendrier = []
    jours_semaine_fr = {
        'Mon': 'Lun', 'Tue': 'Mar', 'Wed': 'Mer', 'Thu': 'Jeu',
        'Fri': 'Ven', 'Sat': 'Sam', 'Sun': 'Dim'
    }

    for jour_num in range(1, num_jours_mois + 1):
        date_courante = datetime(annee_cible, mois_cible, jour_num)
        jour_semaine_abbr_en = date_courante.strftime('%a')
        jour_semaine_fr_abbr = jours_semaine_fr[jour_semaine_abbr_en]
        
        # Déterminer si c'est un weekend (Sam ou Dim)
        is_weekend = jour_semaine_abbr_en in ['Sat', 'Sun']
        
        # Déterminer si c'est un jour d'absence
        is_absence = jour_num in absence_dates
        
        # Logique de remplissage :
        # - Weekends : toujours 0 (pas de travail)
        # - Jours d'absence : 0 dans A1039, 1 dans EXT
        # - Jours travaillés : 1 dans A1039, 0 dans EXT
        
        if is_weekend:
            # Weekends : pas de travail
            jour_data = {
                'jour_num': jour_num,
                'jour_semaine': jour_semaine_fr_abbr,
                'saisie_A1039': '0',
                'realise_A1039': '0.00',
                'saisie_EXT': '0',
                'realise_EXT': '0.00',
            }
        elif is_absence:
            # Jours d'absence
            jour_data = {
                'jour_num': jour_num,
                'jour_semaine': jour_semaine_fr_abbr,
                'saisie_A1039': '0',
                'realise_A1039': '0.00',
                'saisie_EXT': '1',
                'realise_EXT': '1.00',
            }
        else:
            # Jours travaillés normaux
            jour_data = {
                'jour_num': jour_num,
                'jour_semaine': jour_semaine_fr_abbr,
                'saisie_A1039': '1',
                'realise_A1039': '1.00',
                'saisie_EXT': '0',
                'realise_EXT': '0.00',
            }
        
        jours_calendrier.append(jour_data)

    print(f"Calendrier généré pour {calendar.month_name[mois_cible]} {annee_cible}")
    print(f"Jours d'absence configurés: {absence_dates}")

    # --- Génération du PDF ---
    nom_fichier_pdf = f'Triskell_{mois_cible:02d}-{annee_cible}.pdf'
    
    try:
        pdf = PDFMensuel(mois_cible, annee_cible, 'P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.chapter_body(jours_calendrier, {})
        pdf.output(nom_fichier_pdf)
        print(f"PDF généré avec succès: {nom_fichier_pdf}")
        return nom_fichier_pdf
    except Exception as e:
        print(f"Erreur lors de la génération du PDF: {e}")
        return None

class PDFMensuel(FPDF):
    def __init__(self, mois_cible, annee_cible, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mois_cible = mois_cible
        self.annee_cible = annee_cible
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 12, 'Temps Passés - Liste', 0, 1, 'C')
        self.ln(2)

    def footer(self):
        self.y = -15
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_body(self, jours_data, donnees_projets_globales):
        self.set_font('Arial', '', 10)

        # --- Tableau principal ---
        col_widths = [48, 38, 38, 60, 22]
        total_table_width = sum(col_widths)
        x_debut = (self.w - self.l_margin - self.r_margin - total_table_width) / 2 + self.l_margin
        headers = [
            "Pool de ressources", "Parent", "Objet", "Description", "Réalisé"
        ]
        # En-tête bleu très clair
        self.set_fill_color(233, 238, 244)
        self.set_font('Arial', 'B', 10)
        self.set_x(x_debut)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        # Ligne 1 : blanc
        self.set_font('Arial', '', 10)
        self.set_fill_color(255,255,255)
        self.set_x(x_debut)
        self.cell(col_widths[0], 8, "A1039 Socle IAAS Cloud", 1, 0, 'L', True)
        self.cell(col_widths[1], 8, "Socle IaaS 2025", 1, 0, 'L', True)
        self.cell(col_widths[2], 8, "Socle IaaS 2025", 1, 0, 'L', True)
        self.cell(col_widths[3], 8, "", 1, 0, 'L', True)
        total_realise_A1039_mois = sum(float(d['realise_A1039']) for d in jours_data)
        self.cell(col_widths[4], 8, f"{total_realise_A1039_mois:.2f}".replace('.', ','), 1, 1, 'R', True)
        # Ligne 2 : gris clair
        self.set_fill_color(240,242,245)
        self.set_x(x_debut)
        self.cell(col_widths[0], 8, "EXT - Absence U TECH", 1, 0, 'L', True)
        self.cell(col_widths[1], 8, "EXT - Absence U TECH", 1, 0, 'L', True)
        self.cell(col_widths[2], 8, "EXT - Absence U TECH", 1, 0, 'L', True)
        self.cell(col_widths[3], 8, "pour saisie des temps non travaillés pour U", 1, 0, 'L', True)
        total_realise_EXT_mois = sum(float(d['realise_EXT']) for d in jours_data)
        self.cell(col_widths[4], 8, f"{total_realise_EXT_mois:.2f}".replace('.', ','), 1, 1, 'R', True)
        self.ln(4)

        # --- Mois/année centré ---
        self.set_font('Arial', 'B', 12)
        mois_annee = f"{self.annee_cible}-{self.mois_cible:02d}"
        self.cell(0, 10, mois_annee, 0, 1, 'C')
        self.ln(2)

        # --- Matrice des jours ---
        nb_jours = len(jours_data)
        total_travail = sum(float(d['saisie_A1039']) for d in jours_data)
        total_absence = sum(float(d['saisie_EXT']) for d in jours_data)
        jours_travail = [int(d['saisie_A1039']) for d in jours_data]
        jours_absence = [int(d['saisie_EXT']) for d in jours_data]
        col_per_row_first = 5
        col_per_row_next = 6
        col_w = (self.w - self.l_margin - self.r_margin) / 6
        # Premier bloc : Total + 5 jours
        start = 0
        end = min(start + col_per_row_first, nb_jours)
        # En-tête bleu très clair
        self.set_fill_color(233, 238, 244)
        self.set_font('Arial', 'B', 10)
        self.cell(col_w, 8, "Total", 1, 0, 'C', True)
        for i in range(start, end):
            label = f"Jour {i+1}"
            self.cell(col_w, 8, label, 1, 0, 'C', True)
        self.ln()
        # Ligne 1 : blanc
        self.set_fill_color(255,255,255)
        self.set_font('Arial', '', 10)
        self.cell(col_w, 8, str(int(total_travail)), 1, 0, 'C', True)
        for i in range(start, end):
            self.cell(col_w, 8, str(jours_travail[i]), 1, 0, 'C', True)
        self.ln()
        # Ligne 2 : gris clair
        self.set_fill_color(240,242,245)
        self.cell(col_w, 8, str(int(total_absence)), 1, 0, 'C', True)
        for i in range(start, end):
            self.cell(col_w, 8, str(jours_absence[i]), 1, 0, 'C', True)
        self.ln()
        # Blocs suivants : 6 jours par ligne
        for start in range(end, nb_jours, col_per_row_next):
            end2 = min(start + col_per_row_next, nb_jours)
            # En-tête bleu très clair
            self.set_fill_color(233, 238, 244)
            self.set_font('Arial', 'B', 10)
            for i in range(start, end2):
                label = f"Jour {i+1}"
                self.cell(col_w, 8, label, 1, 0, 'C', True)
            self.ln()
            # Ligne 1 : blanc
            self.set_fill_color(255,255,255)
            self.set_font('Arial', '', 10)
            for i in range(start, end2):
                self.cell(col_w, 8, str(jours_travail[i]), 1, 0, 'C', True)
            self.ln()
            # Ligne 2 : gris clair
            self.set_fill_color(240,242,245)
            for i in range(start, end2):
                self.cell(col_w, 8, str(jours_absence[i]), 1, 0, 'C', True)
            self.ln()

def main():
    parser = argparse.ArgumentParser(description='Générateur de rapport Triskell interactif')
    parser.add_argument('--input-file', required=True, help='Fichier Excel d\'entrée')
    parser.add_argument('--absence-dates', help='Jours d\'absence (format: "9,10,15" ou JSON array)')
    parser.add_argument('--month', type=int, help='Mois cible (1-12)')
    parser.add_argument('--year', type=int, help='Année cible')
    
    args = parser.parse_args()
    
    absence_dates = parse_absence_dates(args.absence_dates) if args.absence_dates else []
    
    result = process_triskell_data(
        fichier_entree=args.input_file,
        absence_dates=absence_dates,
        mois_cible=args.month,
        annee_cible=args.year
    )
    
    if result:
        print(f"✅ Succès! PDF généré: {result}")
        sys.exit(0)
    else:
        print("❌ Échec de la génération du PDF")
        sys.exit(1)

if __name__ == "__main__":
    main() 