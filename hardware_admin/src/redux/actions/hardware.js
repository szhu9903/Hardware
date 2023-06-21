import api from '../../api'
import { 
  UPDATE_DATA, 
  GET_HARDWARE_EQUIP, 
  GET_ASSIGN_HARDWARE_EQUIP,
  GET_HARDWARE_TYPE, 
  GET_HARDWARE_CONFIG_VAR,
} from '../constants'

// 获取设备列表
const getHardwareEquip = (param) => {
  return async (dispatch) => {
    const response = await api.hardware.getHardwareEquip(param);
    dispatch({
      type: GET_HARDWARE_EQUIP,
      data: response.data,
    })
  }
}

// 获取可分配设备列表
const getAssignHardwareEquip = (param) => {
  return async (dispatch) => {
    const response = await api.hardware.getHardwareEquip(param);
    dispatch({
      type: GET_ASSIGN_HARDWARE_EQUIP,
      data: response.data,
    })
  }
}

// 获取设备分类
const getHardwareType = (param) => {
  return async (dispatch) => {
    const response = await api.hardware.getHardwareType(param);
    dispatch({
      type: GET_HARDWARE_TYPE,
      data: response.data,
    })
  }
}

// 获取设备配置项
const getHardwareConfigVar = (param) => {
  return async (dispatch) => {
    const response = await api.hardware.getHardwareConfigVar(param);
    dispatch({
      type: GET_HARDWARE_CONFIG_VAR,
      data: response.data,
    })
  }
}
// 通用更新
const updateData = (data) => ({type: UPDATE_DATA, data})

export default {
  getHardwareEquip,
  getAssignHardwareEquip,
  getHardwareType,
  getHardwareConfigVar,
  updateData,
}

