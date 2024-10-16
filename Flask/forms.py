from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class AddCaveForm(FlaskForm):
    nom = StringField('Nom de la cave', validators=[DataRequired()])
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
    numero_etagere = IntegerField('Numéro d\'étagère', validators=[DataRequired()])
    submit = SubmitField('Créer Étagère')

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
