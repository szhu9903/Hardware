import service from '../utils/service'

// 用户登录
const sysLogin = async (data) => {
  return await service.post(`/v2/login/`, data);
}

// 获取用户
const getSysUser = async (param) => {
  return await service.get(`/v3/sysuser/?${param ? param : ""}&depth_col=u_role`);
}
// 添加用户
const addSysUser = async (data) => {
  return await service.post(`/v3/sysuser/`, data);
}
// 修改用户
const modifySysUser = async (param, data) => {
  return await service.put(`/v3/sysuser/${param.id}/`, data);
}
// 删除用户
const delSysUser = async (param) => {
  return await service.delete(`/v3/sysuser/${param.id}/`);
}


export default {
  sysLogin,
  getSysUser,
  addSysUser,
  modifySysUser,
  delSysUser,
}


