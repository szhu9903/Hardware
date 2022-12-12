import service from "../utils/service";


// 获取角色
const getSysRole = async (param) => {
  return await service.get(`/v3/sysrole/?${param ? param : ""}&depth_col=r_purview,r_menu`);
}
// 添加文章标签
const addSysRole = async (data) => {
  return await service.post(`/v3/sysrole/`, data);
}
// 修改文章标签
const modifySysRole = async (param, data) => {
  return await service.put(`/v3/sysrole/${param.id}/`, data);
}
// 删除文章标签
const delSysRole = async (param) => {
  return await service.delete(`/v3/sysrole/${param.id}/`);
}

// 获取路由权限项
const getSysPurview = async (param) => {
  return await service.get(`/v3/syspurview/?${param ? param : ""}`);
}

// 获取菜单权限项
const getSysMenu = async (param) => {
  return await service.get(`/v3/sysmenu/?${param ? param : ""}`);
}

// 获取用户菜单
const getMenu = async () => {
  return await service.get(`/v2/usermenu/`);
}

// 上传图片
const uploadImg = async (params) => {
  let config = {
    headers: {"Content-Type": "multipart/form-data"}
  }
  let response = await service.post('/v2/upload/img/', params, config);
  console.log(response.data);
  return response.data.data.link_url;
}

export default {
  getSysRole,
  addSysRole,
  modifySysRole,
  delSysRole,

  getSysPurview,
  getSysMenu,

  getMenu,
  uploadImg,
};
