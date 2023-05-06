import service from '../utils/service'

// 获取full103数据
const getFull103Data = async (param) => {
  return await service.get(`/v3/hardwareequip/?${param ? param : ""}&view=Hardware_Equip_Full103`);
}
// // 修改LED
// const modifyDemoLed = async (param, data) => {
//   return await service.put(`/v3/demoled/${param.id}/`, data)
// }



export default {
  getFull103Data,
  // modifyDemoLed,

  // getDemoEnv,
}
