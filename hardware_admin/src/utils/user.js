
export function getUserInfo() {
  let userInfo = {
    id: null,
  };
  if (window.localStorage.getItem('user_info')) {
    userInfo = JSON.parse(window.localStorage.getItem('user_info'));
  }
  return userInfo;
}
