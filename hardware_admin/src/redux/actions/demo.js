import api from '../../api'
import {UPDATE_DATA, GET_DEMO_LED, GET_DEMO_ENV} from '../constants'

// 获取设备列表
const getDemoLed = (param) => {
  return async (dispatch) => {
    const response = await api.demo.getDemoLed(param);
    dispatch({
      type: GET_DEMO_LED,
      data: response.data,
    })
  }
}

// 获取设备分类
const getDemoEnv = (param) => {
  return async (dispatch) => {
    const response = await api.demo.getDemoEnv(param);
    dispatch({
      type: GET_DEMO_ENV,
      data: response.data,
    })
  }
}

// 通用更新
const updateData = (data) => ({type: UPDATE_DATA, data})

export default {
  getDemoLed,
  getDemoEnv,
  updateData,
}

