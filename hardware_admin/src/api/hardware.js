import service from '../utils/service'

// 获取设备
const getHardwareEquip = async (param) => {
  return await service.get(`/v3/hardwareequip/?${param ? param : ""}&depth_col=he_type`);
}
// 添加设备
const addHardwareEquip = async (data) => {
  return await service.post(`/v3/hardwareequip/`, data)
}
// 修改设备
const modifyHardwareEquip = async (param, data) => {
  return await service.put(`/v3/hardwareequip/${param.id}/`, data)
}
// 删除设备
const delHardwareEquip = async (param) => {
  return await service.delete(`/v3/hardwareequip/${param.id}/`)
}

// 获取设备分类
const getHardwareType = async (param) => {
  return await service.get(`/v3/hardwaretype/?${param?param:""}`);
}
// 添加设备分类
const addHardwareType = async (data) => {
  return await service.post(`/v3/hardwaretype/`, data)
}
// 修改设备分类
const modifyHardwareType = async (param, data) => {
  return await service.put(`/v3/hardwaretype/${param.id}/`, data)
}
// 删除设备分类
const delHardwareType = async (param) => {
  return await service.delete(`/v3/hardwaretype/${param.id}/`)
}

// 获取设备配置项
const getHardwareConfigVar = async (param) => {
  return await service.get(`/v3/hardwareconfigvar/?${param ? param : ""}&depth_col=hcv_type`);
}
// 添加设备配置项
const addHardwareConfigVar = async (data) => {
  return await service.post(`/v3/hardwareconfigvar/`, data)
}
// 修改设备配置项
const modifyHardwareConfigVar = async (param, data) => {
  return await service.put(`/v3/hardwareconfigvar/${param.id}/`, data)
}
// 删除设备配置项
const delHardwareConfigVar = async (param) => {
  return await service.delete(`/v3/hardwareconfigvar/${param.id}/`)
}

// 发送设备指令
// const sendCommand = async (data) => {
//   return await service.post(`/v2/hardware/operation/`, data)
// }

export default {
  getHardwareEquip,
  addHardwareEquip,
  modifyHardwareEquip,
  delHardwareEquip,

  getHardwareType,
  addHardwareType,
  modifyHardwareType,
  delHardwareType,

  getHardwareConfigVar,
  addHardwareConfigVar,
  modifyHardwareConfigVar,
  delHardwareConfigVar,

  // sendCommand,
}
