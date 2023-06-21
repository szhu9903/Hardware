import { UPDATE_DATA, GET_HARDWARE_EQUIP, GET_HARDWARE_TYPE, GET_HARDWARE_CONFIG_VAR, GET_ASSIGN_HARDWARE_EQUIP} from '../constants'

const initState = {
  // 设备
  hardwareEquip: [],
  hardwareEquipDetail: {},
  hardwareEquipTotalSize: null,
  isOperateHardwareEquip: false,
  assignHardwareEquip: [],
  isAssignHardwareEquip: false,
  //设备分类
  hardwareType: [],
  hardwareTypeDetail: {},
  hardwareTypeTotalSize: null,
  isOperateHardwareType: false,
  //设备配置项
  hardwareConfigVar: [],
  hardwareConfigVarDetail: {},
  hardwareConfigVarTotalSize: null,
  isOperateHardwareConfigVar: false,
}

export default function blog(preState=initState, action) {
  const { type, data } = action;
  switch (type) {

    case GET_HARDWARE_EQUIP:
      return {...preState, hardwareEquip: data.data, hardwareEquipTotalSize: data.total_count};
    
    case GET_ASSIGN_HARDWARE_EQUIP:
      return {...preState, assignHardwareEquip: data.data};
      
    case GET_HARDWARE_TYPE:
      return {...preState, hardwareType: data.data, hardwareTypeTotalSize: data.total_count};
    
    case GET_HARDWARE_CONFIG_VAR:
      return {...preState, hardwareConfigVar: data.data, hardwareConfigVarTotalSize: data.total_count};
    
    case UPDATE_DATA:
      return {...preState, ...data}

    default:
      return preState;
  }
}

