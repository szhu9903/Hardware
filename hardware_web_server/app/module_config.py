
from app.comm.TableModule import TableModule

table_module_map = {
    'sysuser': TableModule('sys_user'),
    'sysrole': TableModule('sys_role'),
    'syspurview': TableModule('sys_purview'),
    'sysmenu': TableModule('sys_menu'),
    'urrelation': TableModule('ur_relation'),
    'rprelation': TableModule('rp_relation'),
    'rmrelation': TableModule('rm_relation'),
    'hardwaretype': TableModule('Hardware_Type'),
    'hardwareequip': TableModule('Hardware_Equip', ['Hardware_Equip_Full103']),
    'hardwareconfigvar': TableModule('Hardware_ConfigVar'),

    'demoenv': TableModule('Demo_Env'),
    'demoled': TableModule('Demo_Led'),

    'full103env': TableModule('Full103_Env'),
    'full103relay': TableModule('Full103_Relay'),
}
