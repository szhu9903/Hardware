import service from '../utils/service'

// 获取LED
const getDemoLed = async (param) => {
  return await service.get(`/v3/demoled/?${param ? param : ""}&depth_col=dl_equip`);
}
// 修改LED
const modifyDemoLed = async (param, data) => {
  return await service.put(`/v3/demoled/${param.id}/`, data)
}

// 获取环境数据
const getDemoEnv = async (param) => {
  return await service.get(`/v3/demoenv/?${param?param:""}&depth_col=de_equip`);
}



export default {
  getDemoLed,
  modifyDemoLed,

  getDemoEnv,
}
