import { UPDATE_IS_SHOW_LOGIN } from "../constants";

// 显示或关闭登录窗口
const updateIsShowLogin = (data) => ({type: UPDATE_IS_SHOW_LOGIN, data});

export default {
  updateIsShowLogin,
}

