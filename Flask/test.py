import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="toto",
    password="toto",
    database="cavevin"
)

# Données à insérer
data = "cave_test8"
nombre_etageres = 6
current_user_id = 2

try:
    cur = conn.cursor(dictionary=True)

    # Exécution de la requête d'insertion
    cur.execute("INSERT INTO Cave (nom, nombreEtagere, utilisateur_id) VALUES (%s, %s, %s)",
                (data, nombre_etageres, current_user_id))

    # Validation des modifications
    conn.commit()
    print(f"Cave '{data}' créée avec succès pour l'utilisateur {current_user_id}.")

    # Vérification de l'insertion avec un SELECT
    cur.execute("SELECT * FROM Cave WHERE nom = %s AND utilisateur_id = %s", (data, current_user_id))
    inserted_cave = cur.fetchone()

    if inserted_cave:
        print(f"Cave trouvée : {inserted_cave}")
    else:
        print("Erreur : la cave n'a pas été trouvée après l'insertion.")

except mysql.connector.Error as err:
    print(f"Erreur : {err}")

finally:
    cur.close()
    conn.close()
