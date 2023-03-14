-- 增加新设备时默认增加一个待分配的设备
DROP TRIGGER IF EXISTS Hardware_Type_TAI;
DELIMITER ||
CREATE TRIGGER Hardware_Type_TAI AFTER INSERT
ON Hardware_Type FOR EACH ROW
BEGIN
    INSERT INTO Hardware_Equip(he_type, he_name, he_num,he_starttype, he_effect)
    VALUES(NEW.id, '待分配', NEW.ht_code_down, 'START', 0);
END
||
DELIMITER;

-- 修改设备时更新待分配设备
DROP TRIGGER IF EXISTS Hardware_Type_TAU;
DELIMITER ||
CREATE TRIGGER Hardware_Type_TAU AFTER UPDATE
ON Hardware_Type FOR EACH ROW
BEGIN
    IF NEW.ht_code_down <> OLD.ht_code_down THEN  /* 司机二次确认取确认时间 */
        UPDATE Hardware_Equip SET he_num=NEW.ht_code_down,he_starttype='START',he_effect=0
        WHERE he_num=OLD.ht_code_down;
    END IF;
END
||
DELIMITER;

-- 创建正常使用设备自动创建设备相关模块管理表
DROP TRIGGER IF EXISTS Hardware_Equip_TAI;
DELIMITER ||
CREATE TRIGGER Hardware_Equip_TAI AFTER INSERT
ON Hardware_Equip FOR EACH ROW
BEGIN
    -- DEMO设备
    IF (NEW.he_type=1 AND NEW.he_effect=1) THEN
        INSERT INTO Demo_Led(dl_equipid, dl_equipcode) VALUES(NEW.id, NEW.he_num);
    END IF;

    -- PCB全功能设备
    IF (NEW.he_type=2 AND NEW.he_effect=1) THEN
        INSERT INTO Full103_Relay(fr_equipid, fr_equipcode) VALUES (NEW.id, NEW.he_num);
    END IF;
END
||
DELIMITER;

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

