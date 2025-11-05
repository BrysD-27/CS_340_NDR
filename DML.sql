-- Supplies Table Queries

-- Insert a new supply
INSERT INTO Supplies (supplyBrand, supplyModel, supplyCategory, currentInventory, unitDescription)
VALUES (@supplyBrandInput, @supplyModelInput, @supplyCategoryInput, @currentInventoryInput, @unitDescriptionInput);

-- Select all supplies
SELECT supplyID,
       supplyBrand,
       supplyModel, 
       supplyCategory, 
       currentInventory, 
       unitDescription
FROM Supplies;

-- Update a supply record
UPDATE Supplies
SET supplyBrand = @supplyBrandInput,
    supplyModel = @supplyModelInput,
    supplyCategory = @supplyCategoryInput,
    currentInventory = @currentInventoryInput,
    unitDescription = @unitDescriptionInput
WHERE supplyID = @supplyIDInput;

-- Delete a supply
DELETE FROM Supplies
WHERE supplyID = @supplyIDInput;


-- Drivers Table Queries

-- Insert a new driver
INSERT INTO Drivers (firstName, lastName, phone, email, emergencyContactName, emergencyContactPhone, activeStatus, driverDetails)
VALUES (@firstNameInput, @lastNameInput, @phoneInput, @emailInput, @emergencyContactNameInput, @emergencyContactPhoneInput, @activeStatusInput, @driverDetailsInput);

-- Select all drivers
SELECT driverID, 
       firstName, 
       lastName, 
       phone, 
       email, 
       emergencyContactName, 
       emergencyContactPhone, 
       activeStatus, 
       driverDetails
FROM Drivers;

-- Update a driver record
UPDATE Drivers
SET firstName = @firstNameInput,
    lastName = @lastNameInput,
    phone = @phoneInput,
    email = @emailInput,
    emergencyContactName = @emergencyContactNameInput,
    emergencyContactPhone = @emergencyContactPhoneInput,
    activeStatus = @activeStatusInput,
    driverDetails = @driverDetailsInput
WHERE driverID = @driverIDInput;

-- Delete a driver
DELETE FROM Drivers
WHERE driverID = @driverIDInput;


-- Recipients Table Queries

-- Insert a new recipient
INSERT INTO Recipients (organizationName, streetAddress, city, [state], zip, contactName, email, phone, [description])
VALUES (@organizationNameInput, @streetAddressInput, @cityInput, @stateInput, @zipInput, @contactNameInput, @emailInput, @phoneInput, @descriptionInput);

-- Select all recipients
SELECT recipientID, 
       organizationName, 
       streetAddress, 
       city, 
       [state], 
       zip, 
       contactName, 
       email, 
       phone, 
       [description]
FROM Recipients;

-- Update a recipient record
UPDATE Recipients
SET organizationName = @organizationNameInput,
    streetAddress = @streetAddressInput,
    city = @cityInput,
    [state] = @stateInput,
    zip = @zipInput,
    contactName = @contactNameInput,
    email = @emailInput,
    phone = @phoneInput,
    [description] = @descriptionInput
WHERE recipientID = @recipientIDInput;

-- Delete a recipient
DELETE FROM Recipients
WHERE recipientID = @recipientIDInput;


-- Deliveries Table Queries

-- Insert a new delivery
INSERT INTO Deliveries (recipientID, driverID, campaignName, deliveredDateTime, notes)
VALUES (@recipientIDInput, @driverIDInput, @campaignNameInput, @deliveredDateTimeInput, @notesInput);

-- Select all deliveries with recipient and driver names
SELECT d.deliveryID,
       d.recipientID,
       r.organizationName AS recipientName,
       d.driverID,
       CONCAT(dr.firstName, ' ', dr.lastName) AS driverName,
       d.campaignName,
       d.deliveredDateTime,
       d.notes
FROM Deliveries d
JOIN Recipients r ON d.recipientID = r.recipientID
JOIN Drivers dr ON d.driverID = dr.driverID;

-- Update a delivery record
UPDATE Deliveries
SET recipientID = @recipientIDInput,
    driverID = @driverIDInput,
    campaignName = @campaignNameInput,
    deliveredDateTime = @deliveredDateTimeInput,
    notes = @notesInput
WHERE deliveryID = @deliveryIDInput;

-- Delete a delivery
DELETE FROM Deliveries
WHERE deliveryID = @deliveryIDInput;


-- DeliveriesSupplies Table Queries

-- Insert a new delivery-supply record
INSERT INTO DeliveriesSupplies (deliveryID, supplyID, supplyQuantity)
VALUES (@deliveryIDInput, @supplyIDInput, @supplyQuantityInput);

-- Select all delivery-supplies with supply brand and model
SELECT ds.deliverySupplyID,
       ds.deliveryID,
       ds.supplyID,
       s.supplyBrand,
       s.supplyModel,
       ds.supplyQuantity
FROM DeliveriesSupplies ds
JOIN Supplies s ON ds.supplyID = s.supplyID;

-- Update a delivery-supply record
UPDATE DeliveriesSupplies
SET deliveryID = @deliveryIDInput,
    supplyID = @supplyIDInput,
    supplyQuantity = @supplyQuantityInput
WHERE deliverySupplyID = @deliverySupplyIDInput;

-- Delete a delivery-supply record
DELETE FROM DeliveriesSupplies
WHERE deliverySupplyID = @deliverySupplyIDInput;

-- Dropdown for Deliveries to Recipients
SELECT recipientID, organizationName
FROM Recipients;

-- Dropdown for Deliveries to Drivers
SELECT driverID, firstName, lastName
FROM Drivers;

-- Dropdown for DeliveriesSupplies to Supplies
SELECT supplyID, supplyBrand, supplyModel
FROM Supplies;

-- Dropdown for DeliveriesSupplies to Deliveries
SELECT deliveryID
FROM Deliveries;
