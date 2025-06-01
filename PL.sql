-- DeliveriesSupplies CUD Procedures

DELIMITER $$

-- CREATE procedure
CREATE PROCEDURE sp_add_delivery_supply(
    IN p_deliveryID INT,
    IN p_supplyID INT,
    IN p_supplyQuantity INT
)
BEGIN
    INSERT INTO DeliveriesSupplies (deliveryID, supplyID, supplyQuantity)
    VALUES (p_deliveryID, p_supplyID, p_supplyQuantity);
END$$

-- UPDATE procedure
CREATE PROCEDURE sp_update_delivery_supply(
    IN p_deliverySupplyID INT,
    IN p_deliveryID INT,
    IN p_supplyID INT,
    IN p_supplyQuantity INT
)
BEGIN
    UPDATE DeliveriesSupplies
    SET deliveryID = p_deliveryID,
        supplyID = p_supplyID,
        supplyQuantity = p_supplyQuantity
    WHERE deliverySupplyID = p_deliverySupplyID;
END$$

-- DELETE procedure
CREATE PROCEDURE sp_delete_delivery_supply(
    IN p_deliverySupplyID INT
)
BEGIN
    DELETE FROM DeliveriesSupplies
    WHERE deliverySupplyID = p_deliverySupplyID;
END$$

DELIMITER ;