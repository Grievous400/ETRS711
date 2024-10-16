class Utilisateur:
    def __init__(self, nom, prenom, pseudo, mot_de_passe):
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo
        self.mot_de_passe = mot_de_passe

    def creer_cave(self, nom_cave, mysql):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Cave (nom, nombreEtagere, utilisateur_id) VALUES (%s, %s, %s)",
                    (nom_cave, 0, self.id))
        mysql.connection.commit()
        cur.close()

    def supprimer_cave(self, cave_id, mysql):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Cave WHERE id = %s", (cave_id,))
        mysql.connection.commit()
        cur.close()

class Cave:
    def __init__(self, nom, nombre_etagere, utilisateur_id):
        self.nom = nom
        self.nombre_etagere = nombre_etagere
        self.utilisateur_id = utilisateur_id

    def ajouter_etagere(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Etagere (numeroEtagere, nombreEmplacementsDisponibles, nombreBouteilles, cave_id) VALUES (%s, %s, %s, %s)",
                    (self.nombre_etagere + 1, 10, 0, self.id))
        mysql.connection.commit()
        cur.close()

class Etagere:
    def __init__(self, numero_etagere, cave_id):
        self.numero_etagere = numero_etagere
        self.cave_id = cave_id

    def ajouter_bouteille(self, bouteille, mysql):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Bouteille (domaineViticole, nom, type, annee, region, prix, etagere_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (bouteille.domaine_viticole, bouteille.nom, bouteille.type_vin, bouteille.annee, bouteille.region, bouteille.prix, self.id))
        mysql.connection.commit()
        cur.close()

class Bouteille:
    def __init__(self, domaine_viticole, nom, type_vin, annee, region, prix):
        self.domaine_viticole = domaine_viticole
        self.nom = nom
        self.type_vin = type_vin
        self.annee = annee
        self.region = region
        self.prix = prix

    def ajouter_commentaire(self, commentaire, mysql):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Commentaire (bouteille_id, pseudo, contenu) VALUES (%s, %s, %s)",
                    (self.id, commentaire.pseudo, commentaire.contenu))
        mysql.connection.commit()
        cur.close()

class Commentaire:
    def __init__(self, bouteille, pseudo, contenu):
        self.bouteille = bouteille
        self.pseudo = pseudo
        self.contenu = contenu
