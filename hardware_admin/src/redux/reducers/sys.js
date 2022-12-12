import { GET_SYS_ROLE, GET_SYS_PURVIEW, GET_SYS_MENU, GET_MENU, UPDATE_DATA } from "../constants";

const initState = {
  sysRole: [],
  sysRoleDetail: {},
  sysRoleTotalSize: null,
  isOperateSysRole: false,

  sysPurviewList: [],
  sysMenuList: [],
  sysMenu: [],
}

export default function sys(preState=initState, action) {
  const { type, data } = action;

  switch (type) {
    case GET_SYS_ROLE:
      return {...preState, sysRole: data.data, sysRoleTotalSize: data.total_count};

    case GET_SYS_PURVIEW:
      return {...preState, sysPurviewList: data.data};

    case GET_SYS_MENU:
      return {...preState, sysMenuList: data.data};
    
    case GET_MENU:
      return {...preState, sysMenu: data.data};
    
    case UPDATE_DATA:
      return {...preState, ...data}

    default:
      return preState;
      
  }

}


