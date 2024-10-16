from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from models import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MYSQL_USER'] = 'toto'
app.config['MYSQL_PASSWORD'] = 'toto'
app.config['MYSQL_DB'] = 'cavevin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creer_cave', methods=['GET', 'POST'])
def creer_cave():
    if request.method == 'POST':
        nom_cave = request.form['nom']
        # On suppose que l'utilisateur est connecté et qu'on a son ID
        utilisateur = Utilisateur("Dupont", "Jean", "jdupont", "password")
        utilisateur.creer_cave(nom_cave, mysql)
        return redirect(url_for('index'))
    return render_template('creer_cave.html')

@app.route('/ajouter_bouteille', methods=['GET', 'POST'])
def ajouter_bouteille():
    if request.method == 'POST':
        domaine_viticole = request.form['domaineViticole']
        nom = request.form['nom']
        type_vin = request.form['type']
        annee = request.form['annee']
        region = request.form['region']
        prix = request.form['prix']

        bouteille = Bouteille(domaine_viticole, nom, type_vin, annee, region, prix)
        # Exemple avec une étagère ID = 1 temporairement
        etagere = Etagere(1, 1)
        etagere.ajouter_bouteille(bouteille, mysql)
        return redirect(url_for('index'))
    return render_template('ajouter_bouteille.html')

if __name__ == '__main__':
    app.run(debug=True)
