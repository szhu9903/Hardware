import { GET_SYS_USER, UPDATE_DATA } from "../constants";

const initState = {
  sysUserList: [],
  sysUserDetail:{},
  sysUserTotalSize: null,
  isOperateUser: false,     // 添加修改用户页面标志
}

export default function user(preState=initState, action) {
  const { type, data } = action;

  switch (type) {
    case GET_SYS_USER:
      return {...preState, sysUserList: data.data, sysUserDetail: data.total_count};
    
    case UPDATE_DATA:
      return {...preState, ...data}

    default:
      return preState;
      
  }

}


