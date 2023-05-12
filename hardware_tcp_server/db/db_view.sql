CREATE OR REPLACE VIEW Hardware_Equip_V AS
SELECT
   a.*,
   b.ht_name
FROM Hardware_Equip a
LEFT JOIN Hardware_Type b ON (a.he_type = b.id)

CREATE OR REPLACE VIEW Hardware_Equip_Full103 AS
SELECT
    a.*,
    b.ht_name,
    c.fe_humidity,c.fe_temperature,
    d.id AS relay_id,d.fr_controlmode,d.fr_switch
FROM Hardware_Equip a
LEFT JOIN Hardware_Type b ON (a.he_type = b.id)
LEFT JOIN Full103_Env c ON (a.id = c.fe_equipid)
left join Full103_Relay d ON (a.id = d.fr_equipid)
where a.he_effect=1 and a.he_type=2
