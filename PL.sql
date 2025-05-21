DELIMITER //
CREATE PROCEDURE sp_delete_demo_driver()
BEGIN
    DELETE FROM Drivers WHERE firstName = 'Ryan' AND lastName = 'Johnson';
END //
DELIMITER ;
