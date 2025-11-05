-- No AI was used in the creation and writing of the procedures below.

DELIMITER //
-- SUPPLIES

CREATE PROCEDURE sp_get_supplies()
BEGIN
  SELECT supplyID,
         supplyBrand,
         supplyModel,
         supplyCategory,
         currentInventory,
         unitDescription
  FROM Supplies
  ORDER BY supplyID;
END //

CREATE PROCEDURE sp_get_supply_by_id(
  IN id INT
)
BEGIN
  SELECT supplyID,
         supplyBrand,
         supplyModel,
         supplyCategory,
         currentInventory,
         unitDescription
  FROM Supplies
  WHERE supplyID = id;
END //

CREATE PROCEDURE sp_add_supply(
  IN brand VARCHAR(100),
  IN model VARCHAR(100),
  IN category VARCHAR(100),
  IN inventory INT,
  IN description TEXT
)
BEGIN
  INSERT INTO Supplies (
      supplyBrand,
      supplyModel,
      supplyCategory,
      currentInventory,
      unitDescription
  )
  VALUES (
      brand,
      model,
      category,
      inventory,
      description
  );
END //

CREATE PROCEDURE sp_update_supply(
  IN id INT,
  IN brand VARCHAR(100),
  IN model VARCHAR(100),
  IN category VARCHAR(100),
  IN inventory INT,
  IN description TEXT
)
BEGIN
  UPDATE Supplies
  SET supplyBrand = brand,
      supplyModel = model,
      supplyCategory = category,
      currentInventory = inventory,
      unitDescription = description
  WHERE supplyID = id;
END //

CREATE PROCEDURE sp_delete_supply(
  IN id INT
)
BEGIN
  DELETE FROM Supplies
  WHERE supplyID = id;
END //

CREATE PROCEDURE sp_get_supply_dropdown()
BEGIN
  SELECT supplyID,
         supplyBrand,
         supplyModel
  FROM Supplies
  ORDER BY supplyID;
END //

-- DRIVERS

CREATE PROCEDURE sp_get_drivers()
BEGIN
  SELECT driverID,
         firstName,
         lastName,
         phone,
         email,
         emergencyContactName,
         emergencyContactPhone,
         activeStatus,
         driverDetails
  FROM Drivers
  ORDER BY driverID;
END //

CREATE PROCEDURE sp_get_driver_by_id(
  IN id INT
)
BEGIN
  SELECT driverID,
         firstName,
         lastName,
         phone,
         email,
         emergencyContactName,
         emergencyContactPhone,
         activeStatus,
         driverDetails
  FROM Drivers
  WHERE driverID = id;
END //

CREATE PROCEDURE sp_add_driver(
  IN firstName VARCHAR(100),
  IN lastName VARCHAR(100),
  IN phone VARCHAR(20),
  IN email VARCHAR(100),
  IN eName VARCHAR(100),
  IN ePhone VARCHAR(20),
  IN active BOOL,
  IN details TEXT
)
BEGIN
  INSERT INTO Drivers (
      firstName,
      lastName,
      phone,
      email,
      emergencyContactName,
      emergencyContactPhone,
      activeStatus,
      driverDetails
  )
  VALUES (
      firstName,
      lastName,
      phone,
      email,
      eName,
      ePhone,
      active,
      details
  );
END //

CREATE PROCEDURE sp_update_driver(
  IN id INT,
  IN firstName VARCHAR(100),
  IN lastName VARCHAR(100),
  IN phone VARCHAR(20),
  IN email VARCHAR(100),
  IN eName VARCHAR(100),
  IN ePhone VARCHAR(20),
  IN active BOOL,
  IN details TEXT
)
BEGIN
  UPDATE Drivers
  SET firstName = firstName,
      lastName = lastName,
      phone = phone,
      email = email,
      emergencyContactName = eName,
      emergencyContactPhone = ePhone,
      activeStatus = active,
      driverDetails = details
  WHERE driverID = id;
END //

CREATE PROCEDURE sp_delete_driver(
  IN id INT
)
BEGIN
  DELETE FROM Drivers
  WHERE driverID = id;
END //

CREATE PROCEDURE sp_get_active_driver_dropdown()
BEGIN
  SELECT driverID,
         firstName,
         lastName
  FROM Drivers
  WHERE activeStatus = 1
  ORDER BY driverID;
END //

-- RECIPIENTS

CREATE PROCEDURE sp_get_recipients()
BEGIN
  SELECT recipientID,
         organizationName,
         streetAddress,
         city,
         state,
         zip,
         contactName,
         email,
         phone,
         description
  FROM Recipients
  ORDER BY recipientID;
END //

CREATE PROCEDURE sp_get_recipient_by_id(
  IN id INT
)
BEGIN
  SELECT recipientID,
         organizationName,
         streetAddress,
         city,
         state,
         zip,
         contactName,
         email,
         phone,
         description
  FROM Recipients
  WHERE recipientID = id;
END //

CREATE PROCEDURE sp_add_recipient(
  IN orgName VARCHAR(255),
  IN streetAddress VARCHAR(255),
  IN city VARCHAR(100),
  IN state VARCHAR(2),
  IN zip VARCHAR(10),
  IN contact VARCHAR(100),
  IN email VARCHAR(100),
  IN phone VARCHAR(20),
  IN description TEXT
)
BEGIN
  INSERT INTO Recipients (
      organizationName,
      streetAddress,
      city,
      state,
      zip,
      contactName,
      email,
      phone,
      description
  )
  VALUES (
      orgName,
      streetAddress,
      city,
      state,
      zip,
      contact,
      email,
      phone,
      description
  );
END //

CREATE PROCEDURE sp_update_recipient(
  IN id INT,
  IN orgName VARCHAR(255),
  IN streetAddress VARCHAR(255),
  IN city VARCHAR(100),
  IN state VARCHAR(2),
  IN zip VARCHAR(10),
  IN contact VARCHAR(100),
  IN email VARCHAR(100),
  IN phone VARCHAR(20),
  IN description TEXT
)
BEGIN
  UPDATE Recipients
  SET organizationName = orgName,
      streetAddress = streetAddress,
      city = city,
      state = state,
      zip = zip,
      contactName = contact,
      email = email,
      phone = phone,
      description = description
  WHERE recipientID = id;
END //

CREATE PROCEDURE sp_delete_recipient(
  IN id INT
)
BEGIN
  DELETE FROM Recipients
  WHERE recipientID = id;
END //

CREATE PROCEDURE sp_get_recipient_dropdown()
BEGIN
  SELECT recipientID,
         organizationName
  FROM Recipients
  ORDER BY recipientID;
END //

-- DELIVERIES

CREATE PROCEDURE sp_get_deliveries()
BEGIN
  SELECT d.deliveryID,
         r.organizationName AS recipientName,
         CONCAT(dr.firstName, ' ', dr.lastName) AS driverName,
         d.campaignName,
         d.deliveredDateTime,
         d.notes
  FROM Deliveries d
  JOIN Recipients r ON d.recipientID = r.recipientID
  JOIN Drivers dr ON d.driverID = dr.driverID
  ORDER BY d.deliveryID;
END //

CREATE PROCEDURE sp_get_delivery_by_id(
  IN id INT
)
BEGIN
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
  JOIN Drivers dr ON d.driverID = dr.driverID
  WHERE d.deliveryID = id;
END //

CREATE PROCEDURE sp_add_delivery(
  IN recipientID INT,
  IN driverID INT,
  IN campaign VARCHAR(255),
  IN date_time DATETIME,
  IN notes TEXT
)
BEGIN
  INSERT INTO Deliveries (
      recipientID,
      driverID,
      campaignName,
      deliveredDateTime,
      notes
  )
  VALUES (
      recipientID,
      driverID,
      campaign,
      date_time,
      notes
  );
END //

CREATE PROCEDURE sp_update_delivery(
  IN id INT,
  IN recipientID INT,
  IN driverID INT,
  IN campaign VARCHAR(255),
  IN date_time DATETIME,
  IN notes TEXT
)
BEGIN
  UPDATE Deliveries
  SET recipientID = recipientID,
      driverID = driverID,
      campaignName = campaign,
      deliveredDateTime = date_time,
      notes = notes
  WHERE deliveryID = id;
END //

CREATE PROCEDURE sp_delete_delivery(
  IN id INT
)
BEGIN
  DELETE FROM Deliveries
  WHERE deliveryID = id;
END //

CREATE PROCEDURE sp_get_delivery_dropdown()
BEGIN
  SELECT deliveryID,
         campaignName
  FROM Deliveries
  ORDER BY deliveryID;
END //

-- DELIVERIES SUPPLIES

CREATE PROCEDURE sp_get_deliveries_supplies()
BEGIN
  SELECT ds.deliverySupplyID,
         ds.deliveryID,
         d.campaignName,
         s.supplyBrand,
         s.supplyModel,
         ds.supplyQuantity
  FROM DeliveriesSupplies ds
  JOIN Deliveries d ON ds.deliveryID = d.deliveryID
  JOIN Supplies s ON ds.supplyID = s.supplyID
  ORDER BY ds.deliverySupplyID;
END //

CREATE PROCEDURE sp_get_delivery_supply_by_id(
  IN id INT
)
BEGIN
  SELECT ds.deliverySupplyID,
         ds.deliveryID,
         ds.supplyID,
         s.supplyBrand,
         s.supplyModel,
         ds.supplyQuantity
  FROM DeliveriesSupplies ds
  JOIN Supplies s ON ds.supplyID = s.supplyID
  WHERE ds.deliverySupplyID = id;
END //

CREATE PROCEDURE sp_add_delivery_supply(
  IN deliveryID INT,
  IN supplyID INT,
  IN supplyQuantity INT
)
BEGIN
  INSERT INTO DeliveriesSupplies (
      deliveryID,
      supplyID,
      supplyQuantity
  )
  VALUES (
      deliveryID,
      supplyID,
      supplyQuantity
  );
END //

CREATE PROCEDURE sp_update_delivery_supply(
  IN id INT,
  IN deliveryID INT,
  IN supplyID INT,
  IN supplyQuantity INT
)
BEGIN
  UPDATE DeliveriesSupplies
  SET deliveryID = deliveryID,
      supplyID = supplyID,
      supplyQuantity = supplyQuantity
  WHERE deliverySupplyID = id;
END //

CREATE PROCEDURE sp_delete_delivery_supply(
  IN id INT
)
BEGIN
  DELETE FROM DeliveriesSupplies
  WHERE deliverySupplyID = id;
END //

-- Home Dashboard Counts

CREATE PROCEDURE sp_get_total_supplies()
BEGIN
  SELECT COALESCE(SUM(currentInventory), 0) AS total_supplies
  FROM Supplies;
END //

CREATE PROCEDURE sp_get_active_drivers()
BEGIN
  SELECT COUNT(*) AS active_drivers
  FROM Drivers
  WHERE activeStatus = TRUE;
END //

CREATE PROCEDURE sp_get_completed_deliveries()
BEGIN
  SELECT COUNT(*) AS completed_deliveries
  FROM Deliveries
  WHERE deliveredDateTime IS NOT NULL;
END //

DELIMITER ;
