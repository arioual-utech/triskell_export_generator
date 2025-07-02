#!/usr/bin/env python3
"""
Script de démarrage pour l'interface web Triskell
"""

import os
import sys
import subprocess

def check_dependencies():
    """Vérifie si les dépendances sont installées"""
    try:
        import flask
        import pandas
        import openpyxl
        import fpdf
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        return False

def install_dependencies():
    """Installe les dépendances manquantes"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation des dépendances")
        return False

def main():
    print("🚀 Démarrage de l'interface web Triskell")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("\n📦 Installation automatique des dépendances...")
        if not install_dependencies():
            print("❌ Impossible d'installer les dépendances. Veuillez les installer manuellement:")
            print("   pip install -r requirements.txt")
            return
    
    # Démarrer l'interface web
    print("\n🌐 Démarrage du serveur web...")
    print("📱 Interface disponible sur: http://localhost:5000")
    print("🛑 Pour arrêter: Ctrl+C")
    print("=" * 50)
    
    try:
        from web_interface import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main() 