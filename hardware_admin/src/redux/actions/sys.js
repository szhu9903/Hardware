import api from "../../api";
import { GET_SYS_ROLE, GET_SYS_PURVIEW, GET_SYS_MENU, GET_MENU, UPDATE_DATA } from "../constants";

// 获取系统角色
const getSysRole = (param) => {
  return async (dispatch) => {
    const response = await api.sys.getSysRole(param);
    dispatch({
      type: GET_SYS_ROLE,
      data: response.data,
    })
  }
}

// 获取权限项
const getSysPurview = (param) => {
  return async (dispatch) => {
    const response = await api.sys.getSysPurview(param);
    dispatch({
      type: GET_SYS_PURVIEW,
      data: response.data,
    })
  }
}

// 获取系统菜单项
const getSysMenu = (param) => {
  return async (dispatch) => {
    const response = await api.sys.getSysMenu(param);
    dispatch({
      type: GET_SYS_MENU,
      data: response.data,
    })
  }
}

// 获取菜单列表
const getMenu = () => {
  return async (dispatch) => {
    const response = await api.sys.getMenu();
    dispatch({
      type: GET_MENU,
      data: response.data,
    })
  }
}

// 通用更新
const updateData = (data) => ({type: UPDATE_DATA, data})

export default {
  getSysRole,
  getSysPurview,
  getSysMenu,
  getMenu,
  updateData,
}

