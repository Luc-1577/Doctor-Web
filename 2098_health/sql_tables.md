CREATE DATABASE IF NOT EXISTS database_name;

USE database_name;

CREATE TABLE IF NOT EXISTS doctors(
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    picture LONGBLOB,
    department TEXT,
    username VARCHAR(256) UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS pacients(
    pacient_id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    email TEXT,
    telephone TEXT,
    message TEXT
);

CREATE TABLE IF NOT EXISTS appointments(
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    pacient_id INT,
    doctor_id INT,
    FOREIGN KEY (pacient_id) REFERENCES pacients(pacient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    department TEXT,
    date_ TEXT
); 