from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from models import *
from forms import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MYSQL_USER'] = 'toto'
app.config['MYSQL_PASSWORD'] = 'toto'
app.config['MYSQL_DB'] = 'cavevin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        pseudo = login_form.pseudo.data
        mot_de_passe = login_form.mot_de_passe.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Utilisateur WHERE pseudo = %s", (pseudo,))
        user = cur.fetchone()
        cur.close()

        print(f"User found: {user}")  # Ajoutez cette ligne pour déboguer

        if user:
            print(f"Mot de passe stocké : {user['motDePasse']}")  # Ajoutez cette ligne pour vérifier le mot de passe
            print(f"Mot de passe entré : {mot_de_passe}")  # Ajoutez cette ligne pour vérifier le mot de passe entré

            if user['motDePasse'] == mot_de_passe:
                session['user_id'] = user['id']
                session['pseudo'] = user['pseudo']
                flash(f'Bienvenue {user["pseudo"]} !', 'success')
                return redirect(url_for('lister_caves'))
            else:
                flash('Mot de passe incorrect', 'danger')
        else:
            flash('Pseudo non trouvé', 'danger')

    return render_template('index.html', login_form=login_form)


@app.route('/creer_cave', methods=['GET', 'POST'])
def creer_cave():
    cave_form = AddCaveForm()
    if cave_form.validate_on_submit():
        utilisateur_id = session.get('user_id')  # Récupérer l'ID de l'utilisateur connecté
        if utilisateur_id:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Cave (nom, nombreEtagere, utilisateur_id) VALUES (%s, %s, %s)",
                        (cave_form.nom.data, 0, utilisateur_id))
            mysql.connection.commit()
            cur.close()
            flash('Cave créée avec succès !', 'success')
        return redirect(url_for('lister_caves'))
    return render_template('creer_cave.html', cave_form=cave_form)

@app.route('/creer_etagere', methods=['GET', 'POST'])
def creer_etagere():
    etagere_form = AddEtagereForm()
    if etagere_form.validate_on_submit():
        cave_id = 1  # Remplacer par l'ID de la cave sélectionnée
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Etagere (numeroEtagere, cave_id) VALUES (%s, %s)",
                    (etagere_form.numero_etagere.data, cave_id))
        mysql.connection.commit()
        cur.close()
        flash('Étagère créée avec succès !', 'success')
        return redirect(url_for('lister_etageres'))
    return render_template('creer_etagere.html', etagere_form=etagere_form)

@app.route('/ajouter_bouteille', methods=['GET', 'POST'])
def ajouter_bouteille():
    bouteille_form = AddBouteilleForm()
    if bouteille_form.validate_on_submit():
        bouteille = Bouteille(bouteille_form.domaineViticole.data, bouteille_form.nom.data,
                              bouteille_form.type.data, bouteille_form.annee.data,
                              bouteille_form.region.data, bouteille_form.prix.data)
        etagere_id = 1  # ID d'étagère temporaire
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Bouteille (domaineViticole, nom, type, annee, region, prix, etagere_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (bouteille.domaine_viticole, bouteille.nom, bouteille.type_vin, bouteille.annee, bouteille.region, bouteille.prix, etagere_id))
        mysql.connection.commit()
        cur.close()
        flash('Bouteille ajoutée avec succès !', 'success')
        return redirect(url_for('lister_bouteilles'))
    return render_template('ajouter_bouteille.html', bouteille_form=bouteille_form)

@app.route('/lister_caves')
def lister_caves():
    utilisateur_id = session.get('user_id')
    if utilisateur_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Cave WHERE utilisateur_id = %s", [utilisateur_id])
        caves = cur.fetchall()
        cur.close()
        return render_template('lister_caves.html', caves=caves)
    else:
        flash('Vous devez être connecté pour voir vos caves', 'danger')
        return redirect(url_for('index'))

@app.route('/lister_etageres')
def lister_etageres():
    utilisateur_id = session.get('user_id')
    if utilisateur_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT E.* FROM Etagere E JOIN Cave C ON E.cave_id = C.id WHERE C.utilisateur_id = %s", [utilisateur_id])
        etageres = cur.fetchall()
        cur.close()
        return render_template('lister_etageres.html', etageres=etageres)
    else:
        flash('Vous devez être connecté pour voir vos étagères', 'danger')
        return redirect(url_for('index'))

@app.route('/lister_bouteilles')
def lister_bouteilles():
    utilisateur_id = session.get('user_id')
    if utilisateur_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT B.* FROM Bouteille B JOIN Etagere E ON B.etagere_id = E.id JOIN Cave C ON E.cave_id = C.id WHERE C.utilisateur_id = %s", [utilisateur_id])
        bouteilles = cur.fetchall()
        cur.close()
        return render_template('lister_bouteilles.html', bouteilles=bouteilles)
    else:
        flash('Vous devez être connecté pour voir vos bouteilles', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        pseudo = register_form.pseudo.data
        mot_de_passe = register_form.mot_de_passe.data
        nom = register_form.nom.data
        prenom = register_form.prenom.data

        cur = mysql.connection.cursor()
        # Vérifier si le pseudo existe déjà
        cur.execute("SELECT * FROM Utilisateur WHERE pseudo = %s", [pseudo])
        user = cur.fetchone()

        if user:
            flash('Ce pseudo est déjà pris, veuillez en choisir un autre.', 'danger')
        else:
            # Créer l'utilisateur
            cur.execute("INSERT INTO Utilisateur (nom, prenom, pseudo, motDePasse) VALUES (%s, %s, %s, %s)",
                        (nom, prenom, pseudo, mot_de_passe))
            mysql.connection.commit()
            cur.close()

            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('index'))

    return render_template('register.html', register_form=register_form)


if __name__ == '__main__':
    app.run(debug=True)