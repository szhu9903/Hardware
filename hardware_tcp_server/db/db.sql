
/* 系统用户 */
CREATE TABLE IF NOT EXISTS `sys_user`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    /* 账号 */
    `su_account` VARCHAR(30)  NOT NULL,
    /* 密码 */
    `su_pwd` VARCHAR(100)  NOT NULL DEFAULT '',
    /* 性别*/
    `su_sex` VARCHAR(10)  NOT NULL  DEFAULT '',
    /* 用户名 */
    `su_username` VARCHAR(50)  NOT NULL DEFAULT '',
    /* 头像地址 */
    `su_userphoto` VARCHAR(100)  NOT NULL DEFAULT '' ,
    /* 电话 */
    `su_phone` VARCHAR(50)  NOT NULL DEFAULT '',
    /* 邮箱 */
    `su_email` VARCHAR(50)  NOT NULL DEFAULT '',
    /* 是否可进入后台 */
    `su_isadmin` INT UNSIGNED NOT NULL DEFAULT 0,
    /* 注册时间 */
    `su_createdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    /* 有效状态 0：有效;1：无效 */
    `su_delflag` INT UNSIGNED NOT NULL DEFAULT 0,
    UNIQUE KEY `uk_sys_user_su_account` (`su_account`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 系统角色 */
CREATE TABLE IF NOT EXISTS `sys_role`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    /* 角色名称 */
    `sr_name` VARCHAR(30) NOT NULL ,
    UNIQUE KEY `uk_sys_role_sr_name` (`sr_name`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 系统api权限 */
CREATE TABLE IF NOT EXISTS `sys_purview`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    /* 权限名称 */
    `sp_name` VARCHAR(30) NOT NULL ,
    /* api_path */
    `sp_apipath` VARCHAR(30) NOT NULL ,
    /* 权限类型(1:查看2:操作) */
    `sp_type` TINYINT UNSIGNED NOT NULL ,
    UNIQUE KEY `uk_sys_role_sr_name` (`sp_name`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 系统后台管理菜单 */
CREATE TABLE IF NOT EXISTS `sys_menu`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    /* 菜单名称 */
    `sm_name` VARCHAR(30) NOT NULL ,
    /* 菜单 path */
    `sm_menupath` VARCHAR(30) NULL ,
    /* 所属关联父级菜单(sys_menu) */
    `sm_menuupid` INT UNSIGNED NULL ,
    /* 菜单顺序 */
    `sm_sort` INT UNSIGNED NOT NULL ,
    UNIQUE KEY `uk_sys_menu_sm_name` (`sm_name`),
    CONSTRAINT `fk_sys_menu_sm_menuupid` FOREIGN KEY (`sm_menuupid`) REFERENCES sys_menu(`id`) ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 系统 用户-角色关联表 */
CREATE TABLE IF NOT EXISTS `ur_relation`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    /* 用户ID(blog_user) */
    `ur_userid` INT UNSIGNED NOT NULL ,
    /* 角色ID(sys_role) */
    `ur_roleid` INT UNSIGNED NOT NULL ,
    UNIQUE KEY `uk_ur_relation_ur_userid_ur_roleid` (`ur_userid`, `ur_roleid`),
    CONSTRAINT `fk_ur_relation_ur_userid` FOREIGN KEY (`ur_userid`) REFERENCES sys_user(`id`) ON DELETE CASCADE ,
    CONSTRAINT `fk_ur_relation_ur_roleid` FOREIGN KEY (`ur_roleid`) REFERENCES sys_role(`id`) ON DELETE  CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 系统 角色-权限关联表 */
CREATE TABLE IF NOT EXISTS `rp_relation`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    /* 角色ID(sys_role) */
    `rp_roleid` INT UNSIGNED NOT NULL ,
    /* 权限ID(syspurview) */
    `rp_purviewid` INT UNSIGNED NOT NULL ,
    UNIQUE KEY `uk_rp_relation_rp_roleid_rp_purviewid` (`rp_roleid`, `rp_purviewid`),
    CONSTRAINT `fk_rp_relation_rp_roleid` FOREIGN KEY (`rp_roleid`) REFERENCES sys_role(`id`) ON DELETE  CASCADE ,
    CONSTRAINT `fk_rp_relation_rp_purviewid` FOREIGN KEY (`rp_purviewid`) REFERENCES sys_purview(`id`) ON DELETE  CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 系统 角色-菜单关联表 */
CREATE TABLE IF NOT EXISTS `rm_relation`(
    /* ID */
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    /* 角色ID(sys_role) */
    `rm_roleid` INT UNSIGNED NOT NULL ,
    /* 权限ID(sys_menu) */
    `rm_menuid` INT UNSIGNED NOT NULL ,
    UNIQUE KEY `uk_rm_relation_rm_roleid_rm_menuid` (`rm_roleid`, `rm_menuid`),
    CONSTRAINT `fk_rm_relation_rm_roleid` FOREIGN KEY (`rm_roleid`) REFERENCES sys_role(`id`) ON DELETE CASCADE ,
    CONSTRAINT `fk_rm_relation_rm_menuid` FOREIGN KEY (`rm_menuid`) REFERENCES sys_menu(`id`) ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 硬件设备表  */
CREATE TABLE IF NOT EXISTS `Hardware_Type`(
    /* id */
    `id` INT UNSIGNED AUTO_INCREMENT,
    /* 分类名称 */
    `ht_name` VARCHAR(50) NOT NULL,
    /* 分类设备编码范围下边界 */
    `ht_code_down` INT UNSIGNED NOT NULL,
    /* 分类设备编码范围上边界 */
    `ht_code_up` INT UNSIGNED NOT NULL,
    UNIQUE KEY `uk_hardware_type_ht_name` (`ht_name`),
    PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 硬件设备表  */
CREATE TABLE IF NOT EXISTS `Hardware_Equip`(
    /* id */
    `id` INT UNSIGNED AUTO_INCREMENT,
    /* 设备类型(Hardware_Type) */
    `he_type` INT UNSIGNED NOT NULL,
    /* 设备名称 */
    `he_name` VARCHAR(50) NOT NULL,
    /* 设备编号 */
    `he_num` VARCHAR(50) NOT NULL,
    /* 设备登录状态 LINKED BROKEN */
    `he_equipstatus` VARCHAR(50)  NOT NULL DEFAULT 'BROKEN',
    /* 设备可用状态 start: 启用 stop：停用  unassigned: 待分配  */
    `he_starttype` VARCHAR(50) NOT NULL DEFAULT 'UNASSIGNED',
    /* 设备作用 0：临时设备（用于分配编号的设备） 1：正常设备 */
    `he_effect` TINYINT UNSIGNED NOT NULL DEFAULT 1,
    UNIQUE KEY `uk_hardware_equip_he_num` (`he_num`),
    CONSTRAINT `fk_hardware_equip_he_type` FOREIGN KEY(`he_type`) REFERENCES `Hardware_Type`(`id`),
    PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 设备配置项 */
CREATE TABLE IF NOT EXISTS `Hardware_ConfigVar`(
    /* id */
    `id` INT UNSIGNED AUTO_INCREMENT,
    /* 设备类型(Hardware_Type) */
    `hcv_type` INT UNSIGNED,
    /* 参数项名称 */
    `hcv_variablekey`  VARCHAR(50) NOT NULL,
    /* 参数项取值 */
    `hcv_variablevalue` INT NOT NULL,
    /* 描述 */
    `hcv_describe` VARCHAR(300),
    UNIQUE KEY `uk_sys_configvar_hcv_type_scv_variablekey` (`hcv_type`,`hcv_variablekey`),
    CONSTRAINT `fk_hardware_configvar_he_type` FOREIGN KEY(`hcv_type`) REFERENCES `Hardware_Type`(`id`),
    PRIMARY KEY ( `id` )
)ENGINE=INNODB DEFAULT CHARSET=utf8mb4;


-- DEMO
/* 测试板设备环境数据 */
CREATE TABLE IF NOT EXISTS `Demo_Env`(
  `id` INT UNSIGNED AUTO_INCREMENT,
  /* 关联设备(Hardware_Equip) */
  `de_equipid` INT UNSIGNED NOT NULL,
  /* 关联设备编码 */
  `de_equipcode` INT UNSIGNED NOT NULL,
  /* 温度 */
  `de_temperature` FLOAT(5,1) NOT NULL DEFAULT 0,
  /* 湿度 */
  `de_humidity` FLOAT(5,1) NOT NULL DEFAULT 0,
  /* 时间戳，自动更新 */
  `last_modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_demo_env_de_equipid` (de_equipid),
  CONSTRAINT `fk_demo_env_de_equipid` FOREIGN KEY(`de_equipid`) REFERENCES `Hardware_Equip`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 测试板设备LED控制 */
CREATE TABLE IF NOT EXISTS `Demo_Led`(
  `id` INT UNSIGNED AUTO_INCREMENT,
  /* 关联设备(Hardware_Equip) */
  `dl_equipid` INT UNSIGNED NOT NULL,
  /* 关联设备编码 */
  `dl_equipcode` INT UNSIGNED NOT NULL,
  /* LED 开关 0开 1关 */
  `dl_switch` INT UNSIGNED NOT NULL DEFAULT 1,
  /* LED R */
  `dl_r` INT UNSIGNED NOT NULL DEFAULT 0,
  /* LED G */
  `dl_g` INT UNSIGNED NOT NULL DEFAULT 0,
  /* LED B */
  `dl_b` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_demo_led_dl_equipid` (dl_equipid),
  CONSTRAINT `fk_demo_led_dl_equipid` FOREIGN KEY(`dl_equipid`) REFERENCES `Hardware_Equip`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- f103全功能
/* 设备环境数据 */
CREATE TABLE IF NOT EXISTS `Full103_Env`(
  `id` INT UNSIGNED AUTO_INCREMENT,
  /* 关联设备(Hardware_Equip) */
  `fe_equipid` INT UNSIGNED NOT NULL,
  /* 关联设备编码 */
  `fe_equipcode` INT UNSIGNED NOT NULL,
  /* 温度 */
  `fe_temperature` FLOAT(5,1) NOT NULL DEFAULT 0,
  /* 湿度 */
  `fe_humidity` FLOAT(5,1) NOT NULL DEFAULT 0,
  /* 时间戳，自动更新 */
  `last_modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_full103_env_fe_equipid` (fe_equipid),
  CONSTRAINT `fk_full103_env_fe_equipid` FOREIGN KEY(`fe_equipid`) REFERENCES `Hardware_Equip`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* 设备继电器控制 */
CREATE TABLE IF NOT EXISTS `Full103_Relay`(
  `id` INT UNSIGNED AUTO_INCREMENT,
  /* 关联设备(Hardware_Equip) */
  `fr_equipid` INT UNSIGNED NOT NULL,
  /* 关联设备编码 */
  `fr_equipcode` INT UNSIGNED NOT NULL,
  /* Relay 开关 0:开 1:关 */
  `fr_switch` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  /* 控制方式 0:自动 1:手动 */
  `fr_controlmode` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_full103_relay_fr_equipid` (fr_equipid),
  CONSTRAINT `fk_full103_relay_fr_equipid` FOREIGN KEY(`fr_equipid`) REFERENCES `Hardware_Equip`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
