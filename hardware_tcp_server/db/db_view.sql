CREATE OR REPLACE VIEW Hardware_Equip_V AS
SELECT
   a.*,
   b.ht_name
FROM Hardware_Equip a
LEFT JOIN Hardware_Type b ON (a.he_type = b.id)

