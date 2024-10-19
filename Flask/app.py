from flask import Flask, render_template, request, redirect, url_for, flash, sessions
from flask_mysqldb import MySQL
from models import *
from forms import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_clé'
app.config['MYSQL_USER'] = 'toto'
app.config['MYSQL_PASSWORD'] = 'toto'
app.config['MYSQL_DB'] = 'cavevin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Variable globale pour stocker l'ID utilisateur
current_user_id = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_user  # Indique que l'on veut modifier la variable globale

    if request.method == 'POST':
        pseudo = request.form['pseudo']  # Récupérer le pseudo depuis le formulaire
        mot_de_passe = request.form['mot_de_passe']  # Récupérer le mot de passe depuis le formulaire

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Utilisateur WHERE pseudo = %s", (pseudo,))
        user = cur.fetchone()
        cur.close()

        if user:
            if user['motDePasse'] == mot_de_passe:
                current_user = user  # On sauvegarde l'utilisateur dans la variable globale
                flash(f'Bienvenue {user["pseudo"]} !', 'success')
                return redirect(url_for('lister_caves'))
            else:
                flash('Mot de passe incorrect', 'danger')
        else:
            flash('Pseudo non trouvé', 'danger')

    return render_template('index.html')


@app.route('/creer_cave', methods=['GET', 'POST'])
def creer_cave():
    global current_user  # Utiliser la variable globale

    cave_form = AddCaveForm()

    if cave_form.validate_on_submit():
        print("Le formulaire est bien validé")

        if current_user:  # Vérifie que l'utilisateur est bien connecté
            print(f"ID utilisateur : {current_user['id']}")  # Debug: Vérifie l'ID utilisateur
            print(f"Nom de la cave : {cave_form.nom.data}, Nombre d'étagères : {cave_form.nombre_etageres.data}")  # Debug: Vérifie les valeurs du formulaire

            try:
                # Exécution de la requête SQL
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Cave (nom, nombreEtagere, utilisateur_id) VALUES (%s, %s, %s)",
                            (cave_form.nom.data, cave_form.nombre_etageres.data, current_user['id']))
                mysql.connection.commit()
                cur.close()
                print("Insertion dans la base réussie")
                flash('Cave créée avec succès !', 'success')
            except Exception as e:
                print(f"Erreur lors de l'insertion : {e}")  # Capture l'erreur en cas d'échec
                flash(f"Erreur lors de la création de la cave : {e}", 'danger')

        return redirect(url_for('lister_caves'))
    else:
        print("Le formulaire n'a pas été validé")

        return render_template('creer_cave.html', cave_form=cave_form)

@app.route('/cave/<int:cave_id>/ajouter_etagere', methods=['GET', 'POST'])
def ajouter_etagere(cave_id):
    global current_user  # Utiliser la variable globale

    etagere_form = AddEtagereForm()

    if etagere_form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Etagere (numeroEtagere, nombreEmplacementsDisponibles, nombreBouteilles, cave_id)
            VALUES (%s, %s, %s, %s)
        """, (etagere_form.numero_etagere.data, etagere_form.nombre_emplacements.data, 0, cave_id))
        mysql.connection.commit()
        cur.close()

        flash('Étagère ajoutée avec succès !', 'success')
        return redirect(url_for('lister_etageres', cave_id=cave_id))

    # Transmettre 'cave_id' au template
    return render_template('ajouter_etagere.html', etagere_form=etagere_form, cave_id=cave_id)

@app.route('/etagere/<int:etagere_id>/supprimer', methods=['POST'])
def supprimer_etagere(etagere_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Etagere WHERE id = %s", [etagere_id])
    mysql.connection.commit()
    cur.close()

    flash('Étagère supprimée avec succès !', 'success')
    return redirect(request.referrer)

@app.route('/etagere/<int:etagere_id>/ajouter_bouteille', methods=['GET', 'POST'])
def ajouter_bouteille(etagere_id):
    bouteille_form = AddBouteilleForm()

    if bouteille_form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Bouteille (domaineViticole, nom, type, annee, region, prix, etagere_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (bouteille_form.domaineViticole.data, bouteille_form.nom.data, bouteille_form.type.data, bouteille_form.annee.data,
              bouteille_form.region.data, bouteille_form.prix.data, etagere_id))
        mysql.connection.commit()
        cur.close()

        flash('Bouteille ajoutée avec succès !', 'success')
        return redirect(url_for('lister_bouteilles', etagere_id=etagere_id))

    return render_template('ajouter_bouteille.html', bouteille_form=bouteille_form, etagere_id=etagere_id)

@app.route('/bouteille/<int:bouteille_id>/supprimer', methods=['POST'])
def supprimer_bouteille(bouteille_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Bouteille WHERE id = %s", [bouteille_id])
    mysql.connection.commit()
    cur.close()

    flash('Bouteille supprimée avec succès !', 'success')
    return redirect(request.referrer)

@app.route('/lister_caves')
def lister_caves():
    global current_user  # On utilise la variable globale current_user
    if current_user:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Cave WHERE utilisateur_id = %s", [current_user['id']])
        caves = cur.fetchall()
        cur.close()
        return render_template('lister_caves.html', caves=caves)
    else:
        flash('Vous devez être connecté pour voir vos caves', 'danger')
        return redirect(url_for('index'))


@app.route('/cave/<int:cave_id>/etageres')
def lister_etageres(cave_id):
    global current_user  # Utiliser la variable globale

    if current_user:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Etagere WHERE cave_id = %s", [cave_id])
        etageres = cur.fetchall()
        cur.close()

        # On passe la cave et les étagères à la vue
        return render_template('lister_etageres.html', etageres=etageres, cave_id=cave_id)
    else:
        flash('Vous devez être connecté pour voir les étagères', 'danger')
        return redirect(url_for('index'))

@app.route('/etagere/<int:etagere_id>/bouteilles')
def lister_bouteilles(etagere_id):
    global current_user  # Utiliser la variable globale

    if current_user:
        cur = mysql.connection.cursor()
        # Récupérer l'ID de la cave via l'étagère
        cur.execute("SELECT cave_id FROM Etagere WHERE id = %s", [etagere_id])
        cave = cur.fetchone()

        cur.execute("SELECT * FROM Bouteille WHERE etagere_id = %s", [etagere_id])
        bouteilles = cur.fetchall()
        cur.close()

        if cave:
            cave_id = cave['cave_id']  # Extraire l'ID de la cave
            return render_template('lister_bouteilles.html', bouteilles=bouteilles, etagere_id=etagere_id, cave_id=cave_id)
        else:
            flash("Étagère non trouvée", 'danger')
            return redirect(url_for('lister_caves'))
    else:
        flash('Vous devez être connecté pour voir les bouteilles', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    global current_user_id  # Utiliser la variable globale

    current_user_id = None  # Déconnexion
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

@app.route('/test_session')
def test_session():
    global current_user  # On accède à la variable globale
    if current_user:
        return f"ID utilisateur : {current_user['id']}, Pseudo : {current_user['pseudo']}"
    else:
        return "Aucun utilisateur connecté"

if __name__ == '__main__':
    app.run(debug=True)
