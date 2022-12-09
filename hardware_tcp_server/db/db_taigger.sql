
-- 补全Demo_Env关联设备ID
DROP TRIGGER IF EXISTS Demo_Env_TBI;
DELIMITER ||
CREATE TRIGGER Demo_Env_TBI BEFORE INSERT
ON Demo_Env FOR EACH ROW
BEGIN
  SET NEW.de_equipid=(SELECT id FROM Hardware_Equip WHERE he_num=NEW.de_equipcode);
END
||
DELIMITER;

-- 补全Demo_Led关联设备ID
DROP TRIGGER IF EXISTS Demo_Led_TBI;
DELIMITER ||
CREATE TRIGGER Demo_Led_TBI BEFORE INSERT
ON Demo_Led FOR EACH ROW
BEGIN
  SET NEW.dl_equipid=(SELECT id FROM Hardware_Equip WHERE he_num=NEW.dl_equipcode);
END
||
DELIMITER;

-- 创建新设备 配置外设
DROP TRIGGER IF EXISTS Hardware_Equip_TAI;
DELIMITER ||
CREATE TRIGGER Hardware_Equip_TAI AFTER INSERT
ON Hardware_Equip FOR EACH ROW
BEGIN
  INSERT INTO Demo_Led(dl_equipid, dl_equipcode)
  VALUES(NEW.id, NEW.he_num);
END
||
DELIMITER;
