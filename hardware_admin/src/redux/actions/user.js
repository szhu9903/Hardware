import api from "../../api";
import { GET_SYS_USER, UPDATE_DATA } from "../constants";


// 获取网站用户
const getSysUser = (param) => {
  return async (dispatch) => {
    const response = await api.user.getSysUser(param);
    dispatch({
      type: GET_SYS_USER,
      data: response.data,
    })
  }
}

// 通用更新
const updateData = (data) => ({type: UPDATE_DATA, data})

export default {
  getSysUser,
  updateData,
}

