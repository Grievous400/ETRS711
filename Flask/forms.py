from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import *

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
    nom = StringField('Nom', validators=[DataRequired()])
    type = StringField('Type de vin', validators=[DataRequired()])
    annee = IntegerField('Année', validators=[DataRequired()])
    region = StringField('Région', validators=[DataRequired()])
    prix = FloatField('Prix', validators=[DataRequired()])
    submit = SubmitField('Ajouter Bouteille')

class AddEtagereForm(FlaskForm):
    numero_etagere = IntegerField('Numéro de l\'étagère', validators=[DataRequired(), NumberRange(min=1, message="Le numéro de l'étagère doit être au moins 1")])
    nombre_emplacements = IntegerField('Nombre d\'emplacements disponibles', validators=[DataRequired(), NumberRange(min=1, message="Doit être supérieur à 0")])
    submit = SubmitField('Ajouter')

class AddCommentaireForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    contenu = TextAreaField('Commentaire', validators=[DataRequired()])
    bouteille_id = HiddenField('Bouteille ID', validators=[DataRequired()])
    submit = SubmitField('Ajouter Commentaire')

class RegisterForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Créer un compte')
