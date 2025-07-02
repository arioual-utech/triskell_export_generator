from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime, date
import json
from triskell_interactive import process_triskell_data
from flask_cors import CORS
import calendar

app = Flask(__name__)
app.secret_key = 'triskell_secret_key_2025'
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Vérifier si un fichier a été uploadé
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Sécuriser le nom du fichier
            filename = secure_filename(file.filename)
            
            # Créer un nom unique pour éviter les conflits
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Sauvegarder le fichier
            file.save(filepath)
            
            # Récupérer les paramètres du formulaire
            absence_dates_str = request.form.get('absence_dates', '').strip()
            month = request.form.get('month', type=int)
            year = request.form.get('year', type=int)
            
            try:
                # Traiter les dates d'absence
                absence_dates = []
                if absence_dates_str:
                    if absence_dates_str.startswith('['):
                        # Format JSON
                        absence_dates = json.loads(absence_dates_str)
                    else:
                        # Format simple: "9,10,15"
                        absence_dates = [int(d.strip()) for d in absence_dates_str.split(',') if d.strip().isdigit()]
                
                # Générer le PDF
                result = process_triskell_data(
                    fichier_entree=filepath,
                    absence_dates=absence_dates,
                    mois_cible=month,
                    annee_cible=year
                )
                
                if result:
                    # Retourner le PDF généré
                    return send_file(
                        result,
                        as_attachment=True,
                        download_name=os.path.basename(result),
                        mimetype='application/pdf'
                    )
                else:
                    flash('Erreur lors de la génération du PDF', 'error')
                    
            except Exception as e:
                flash(f'Erreur: {str(e)}', 'error')
            finally:
                # Nettoyer le fichier temporaire
                try:
                    os.remove(filepath)
                except:
                    pass
        else:
            flash('Type de fichier non autorisé. Utilisez .xlsx ou .xls', 'error')
    
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Triskell Generator Web Interface'}

@app.route('/api/calendar/<int:year>/<int:month>')
def get_calendar_data(year, month):
    """API pour récupérer les données du calendrier d'un mois"""
    try:
        # Obtenir le nombre de jours dans le mois
        num_days = calendar.monthrange(year, month)[1]
        
        # Obtenir le premier jour de la semaine (0 = lundi, 6 = dimanche)
        first_day = calendar.monthrange(year, month)[0]
        
        # Le système Python utilise déjà lundi=0, dimanche=6, pas besoin de conversion
        
        # Noms des mois en français
        month_names_fr = {
            1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
        }
        
        calendar_data = {
            'year': year,
            'month': month,
            'month_name': month_names_fr[month],
            'num_days': num_days,
            'first_day': first_day,
            'days': []
        }
        
        # Générer les données pour chaque jour
        for day in range(1, num_days + 1):
            current_date = date(year, month, day)
            day_of_week = current_date.weekday()  # 0 = lundi, 6 = dimanche
            
            # Noms des jours en français
            day_names = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
            
            calendar_data['days'].append({
                'day': day,
                'day_name': day_names[day_of_week],
                'is_weekend': day_of_week >= 5,  # Samedi et dimanche
                'date': current_date.isoformat()
            })
        
        return jsonify(calendar_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/select-pattern', methods=['POST'])
def select_pattern():
    """API pour sélectionner des jours selon un pattern"""
    try:
        data = request.get_json()
        year = data.get('year')
        month = data.get('month')
        pattern = data.get('pattern')
        
        if not all([year, month, pattern]):
            return jsonify({'error': 'Paramètres manquants'}), 400
        
        num_days = calendar.monthrange(year, month)[1]
        selected_days = []
        
        if pattern == 'all_weekdays':
            # Tous les jours de semaine (lundi à vendredi)
            for day in range(1, num_days + 1):
                current_date = date(year, month, day)
                if current_date.weekday() < 5:  # 0-4 = lundi à vendredi
                    selected_days.append(day)
        
        elif pattern == 'all_weekends':
            # Tous les weekends
            for day in range(1, num_days + 1):
                current_date = date(year, month, day)
                if current_date.weekday() >= 5:  # 5-6 = samedi et dimanche
                    selected_days.append(day)
        
        elif pattern.startswith('day_'):
            # Un jour spécifique de la semaine (ex: day_0 pour lundi)
            day_of_week = int(pattern.split('_')[1])
            for day in range(1, num_days + 1):
                current_date = date(year, month, day)
                if current_date.weekday() == day_of_week:
                    selected_days.append(day)
        
        elif pattern == 'range':
            # Plage de dates
            start_day = data.get('start_day')
            end_day = data.get('end_day')
            if start_day and end_day:
                for day in range(start_day, end_day + 1):
                    if 1 <= day <= num_days:
                        selected_days.append(day)
        
        return jsonify({'selected_days': selected_days})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 