CREATE DATABASE cavevin;

USE cavevin;

CREATE TABLE Utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    pseudo VARCHAR(255) UNIQUE,
    motDePasse VARCHAR(255)
);

CREATE TABLE Cave (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    nombreEtagere INT,
    utilisateur_id INT,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
);

CREATE TABLE Etagere (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numeroEtagere INT,
    nombreEmplacementsDisponibles INT,
    nombreBouteilles INT,
    cave_id INT,
    FOREIGN KEY (cave_id) REFERENCES Cave(id)
);

CREATE TABLE Bouteille (
    id INT AUTO_INCREMENT PRIMARY KEY,
    domaineViticole VARCHAR(255),
    nom VARCHAR(255),
    type VARCHAR(50),
    annee INT,
    region VARCHAR(255),
    commentaires TEXT,
    notePersonnelle FLOAT,
    noteMoyenneCommunautaire FLOAT,
    photoEtiquette VARCHAR(255),
    prix FLOAT,
    etagere_id INT,
    FOREIGN KEY (etagere_id) REFERENCES Etagere(id)
);

CREATE TABLE Commentaire (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bouteille_id INT,
    pseudo VARCHAR(255),
    contenu TEXT,
    FOREIGN KEY (bouteille_id) REFERENCES Bouteille(id)
);

ALTER TABLE Commentaire ADD note INT CHECK (note >= 1 AND note <= 5);