import mysql.connector

# Remplacez par vos informations de connexion
conn = mysql.connector.connect(
    host="localhost",
    user="toto",
    password="toto",
    database="cavevin"
)

pseudo = 'test'
mot_de_passe = 'test'  # Mettez ici le mot de passe que vous essayez

cur = conn.cursor(dictionary=True)
cur.execute("SELECT * FROM Utilisateur WHERE pseudo = %s", (pseudo,))
user = cur.fetchone()

if user:
    if user['motDePasse'] == mot_de_passe:
        print(f"Connexion réussie pour {user['pseudo']}")
    else:
        print("Mot de passe incorrect.")
else:
    print("Utilisateur non trouvé.")

cur.close()
conn.close()
