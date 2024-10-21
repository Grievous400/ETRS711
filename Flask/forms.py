from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class AddCaveForm(FlaskForm):
    nom = StringField('Nom de la cave', validators=[DataRequired()])
    nombre_etageres = IntegerField('Nombre d\'étagères', validators=[DataRequired(), NumberRange(min=1, message="Le nombre d'étagères doit être au moins de 1")])
    submit = SubmitField('Créer')

class AddBouteilleForm(FlaskForm):
    domaineViticole = StringField('Domaine Viticole', validators=[DataRequired()])
    nom = StringField('Nom de la bouteille', validators=[DataRequired()])
    type = StringField('Type de vin')
    annee = IntegerField('Année', validators=[DataRequired()])
    region = StringField('Région')
    prix = IntegerField('Prix', validators=[DataRequired()])
    photoEtiquette = FileField('Photo de l\'étiquette', validators=[FileAllowed(['jpg', 'png'], 'Images seulement!')])
    submit = SubmitField('Ajouter la bouteille')

class AddEtagereForm(FlaskForm):
    numero_etagere = IntegerField('Numéro de l\'étagère', validators=[DataRequired(), NumberRange(min=1, message="Le numéro de l'étagère doit être au moins 1")])
    nombre_emplacements = IntegerField('Nombre d\'emplacements disponibles', validators=[DataRequired(), NumberRange(min=1, message="Doit être supérieur à 0")])
    submit = SubmitField('Ajouter')

class AddCommentaireForm(FlaskForm):
    contenu = TextAreaField('Votre commentaire', validators=[DataRequired()])
    note = IntegerField('Votre note (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5, message="La note doit être entre 1 et 5")])
    submit = SubmitField('Ajouter un commentaire')

class RegisterForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Créer un compte')
