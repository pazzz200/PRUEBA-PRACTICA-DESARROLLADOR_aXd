CREATE DATABASE hotel_reservas;

USE hotel_reservas;

CREATE TABLE hoteles (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
ciudad VARCHAR(50) NOT NULL
);

CREATE TABLE habitaciones (
id INT AUTO_INCREMENT PRIMARY KEY,
hotel_id INT NOT NULL,
tipo VARCHAR(20) NOT NULL,
capacidad INT NOT NULL,
cantidad INT NOT NULL,
FOREIGN KEY (hotel_id) REFERENCES hoteles(id)
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    habitacion_id INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    cantidad_habitaciones INT NOT NULL DEFAULT 1,
    estado VARCHAR(20) DEFAULT 'confirmada',
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

CREATE TABLE tarifas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    habitacion_id INT,
    temporada VARCHAR(20),
    precio DECIMAL(10,2)
);

INSERT INTO hoteles (nombre, ciudad)
VALUES
('Hotel Costeño', 'Barranquilla'),
('Hotel del Valle', 'Cali'),
('Hotel Vista al mar', 'Cartagena'),
('Hotel Capital', 'Bogotá');

INSERT INTO habitaciones
(hotel_id, tipo, capacidad, cantidad)
VALUES
(1, 'estandar', 4, 30),
(1, 'premium', 4, 3),
(2, 'premium', 6, 20),
(2, 'vip', 6, 2),
(3, 'estandar', 8, 10),
(3, 'premium', 8, 1),
(4, 'estandar', 6, 20),
(4, 'premium', 6, 20),
(4, 'vip', 6, 2);

INSERT INTO tarifas (id, habitacion_id, temporada, precio) VALUES
(1, 1, 'baja', 150000.00),
(2, 1, 'alta', 220000.00),
(3, 2, 'baja', 250000.00),
(4, 2, 'alta', 350000.00),
(5, 3, 'baja', 250000.00),
(6, 3, 'alta', 350000.00),
(7, 4, 'baja', 400000.00),
(8, 4, 'alta', 550000.00),
(9, 5, 'baja', 150000.00),
(10, 5, 'alta', 220000.00),
(11, 6, 'baja', 250000.00),
(12, 6, 'alta', 350000.00),
(13, 7, 'baja', 150000.00),
(14, 7, 'alta', 220000.00),
(15, 8, 'baja', 250000.00),
(16, 8, 'alta', 350000.00),
(17, 9, 'baja', 400000.00),
(18, 9, 'alta', 550000.00);
