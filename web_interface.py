from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from triskell_interactive import process_triskell_data

app = Flask(__name__)
app.secret_key = 'triskell_secret_key_2025'

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 