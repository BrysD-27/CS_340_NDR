DELIMITER //
DROP PROCEDURE  IF EXISTS sp_delete_latest_driver();
CREATE PROCEDURE sp_delete_latest_driver()
BEGIN
    DELETE FROM Drivers
    WHERE driverID = (
        SELECT MAX(driverID) FROM Drivers
    );
END //
DELIMITER ;