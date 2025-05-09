SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT=0;

DROP TABLE IF EXISTS DeliveriesSupplies;
DROP TABLE IF EXISTS Deliveries;
DROP TABLE IF EXISTS Supplies;
DROP TABLE IF EXISTS Drivers;
DROP TABLE IF EXISTS Recipients;

CREATE TABLE Supplies (
    supplyID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    supplyBrand VARCHAR(100) NOT NULL,
    supplyModel VARCHAR(100) NOT NULL,
    supplyCategory VARCHAR(100) NOT NULL,
    currentInventory INT NOT NULL DEFAULT 0,
    unitDescription TEXT
);

CREATE TABLE Drivers (
    driverID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    emergencyContactName VARCHAR(100),
    emergencyContactPhone VARCHAR(20),
    activeStatus BOOLEAN NOT NULL DEFAULT TRUE,
    driverDetails TEXT
);

CREATE TABLE Recipients (
    recipientID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    organizationName VARCHAR(100) NOT NULL,
    streetAddress VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    zip VARCHAR(255) NOT NULL,
    contactName VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    description TEXT
);

CREATE TABLE Deliveries (
    deliveryID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    recipientID INT NOT NULL,
    driverID INT NOT NULL,
    campaignName VARCHAR(100),
    deliveredDateTime DATETIME,
    notes TEXT,
    FOREIGN KEY (recipientID) REFERENCES Recipients(recipientID) ON DELETE CASCADE,
    FOREIGN KEY (driverID) REFERENCES Drivers(driverID) ON DELETE CASCADE
);

CREATE TABLE DeliveriesSupplies (
    deliverySupplyID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    deliveryID INT NOT NULL,
    supplyID INT NOT NULL,
    supplyQuantity INT NOT NULL,
    FOREIGN KEY (deliveryID) REFERENCES Deliveries(deliveryID) ON DELETE CASCADE,
    FOREIGN KEY (supplyID) REFERENCES Supplies(supplyID) ON DELETE CASCADE
);

-- Sample Data: Supplies
INSERT INTO Supplies (supplyBrand, supplyModel, supplyCategory, currentInventory, unitDescription) VALUES
('3M', '8210', 'N95s', 18020, '20 per small box, 160 per cardboard case, some damage to a small number of cases otherwise good condition.'),
('3M', '8110', 'N95s', 9080, 'closest thing to a kids n95, s is for small, 20 per box, 160 per cardboard case'),
('Levoit', 'Vital 100', 'Air Purifier', 225, 'rated for 1008 sq feet, hepa, has thin carbon filter'),
('Qio Chuang', 'Emergency Mylar Thermal Space Blanker', 'Emergency Blanket', 0, NULL);

-- Sample Data: Drivers
INSERT INTO Drivers (firstName, lastName, phone, email, emergencyContactName, emergencyContactPhone, activeStatus, driverDetails) VALUES
('Ryan', 'Johnson', '821-221-4522', 'rayjohnson25@gmail.com', 'Shari', '821-422-4828', TRUE, NULL),
('Cassius', 'Andor', '123-456-789', 'formysister@gmail.com', NULL, NULL, TRUE, 'Large van, certified'),
('Mike', 'Ehrmantraut', '505-867-5309', 'mike.e@yahoo.com', 'Kaylee', '505-123-4567', TRUE, 'Defensive driving certified');

-- Sample Data: Recipients
INSERT INTO Recipients (organizationName, streetAddress, city, state, zip, contactName, email, phone, description) VALUES
('United Way PNW', '400 Union Avenue SE', 'Olympia', 'WA', '98501', 'Trish Gonzalez', 'tgonzalez@unitedwaypnw.org', '208-520-1910', 'Can distribute to Forest Aid Forever and other groups.'),
('Rogue Action Center', '555 Liberty Street', 'Eugene', 'OR', '97501', 'Diego Morales', 'd.morales@rac.org', '541-781-3311', 'Focus on wildfire recovery'),
('Forest Aid Group', '1200 Pine Lane', 'Monterey', 'CA', '93940', 'June Winters', 'june.winters@forestaid.org', '503-222-0101', 'Partner org in rural areas');

-- Sample Data: Deliveries
INSERT INTO Deliveries (recipientID, driverID, campaignName, deliveredDateTime, notes) VALUES
(1, 1, 'Seattle Earthquake June 2023', '2023-06-20 10:30:00', 'Left Supplies at Side Door.'),
(2, 2, 'Southern OR Fire Relief', '2023-08-14 13:45:00', 'Extra Purifiers requested'),
(3, 3, NULL, NULL, 'In transit'),
(1, 3, 'Northwest Heat Response', '2025-04-12 09:00:00', 'Delivered Early');

-- Sample Data: DeliveriesSupplies
INSERT INTO DeliveriesSupplies (deliveryID, supplyID, supplyQuantity) VALUES
(1, 1, 20),
(2, 3, 15),
(2, 2, 25),
(3, 1, 30),
(4, 4, 35);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
