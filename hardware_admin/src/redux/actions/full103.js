import api from '../../api'
import {UPDATE_DATA, GET_FULL103_DATA} from '../constants'

// 获取设备列表
const getFull103Data = (param) => {
  return async (dispatch) => {
    const response = await api.full103.getFull103Data(param);
    dispatch({
      type: GET_FULL103_DATA,
      data: response.data,
    })
  }
}

// 通用更新
const updateData = (data) => ({type: UPDATE_DATA, data})

export default {
  getFull103Data,
  updateData,
}

