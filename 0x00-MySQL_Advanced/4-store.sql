-- create trigger to descrease item quantities when orders made
DROP TRIGGER IF EXISTS decrease_quantity;
DELIMITER $$
CREATE TRIGGER IF NOT EXISTS decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END $$
DELIMITER ;
