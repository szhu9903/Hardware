import service from '../utils/service'

// 获取full103数据
const getFull103Data = async (param) => {
  return await service.get(`/v3/hardwareequip/?${param ? param : ""}&view=Hardware_Equip_Full103`);
}
// 修改full103
const modifyFull103Data = async (param, data) => {
  return await service.put(`/v3/full103relay/${param.id}/`, data)
}



export default {
  getFull103Data,
  modifyFull103Data,

  // getDemoEnv,
}
