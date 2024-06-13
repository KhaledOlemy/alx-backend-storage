-- valid email trigger
DROP TRIGGER IF EXISTS validChecker;
DELIMITER $$
CREATE TRIGGER validChecker
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email
    THEN
        SET NEW.valid_email = 0;
    END IF;
END;
