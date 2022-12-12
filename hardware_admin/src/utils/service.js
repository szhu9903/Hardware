import axios from 'axios'
import { message } from 'antd'

const service = axios.create({
  // baseURL: "http://127.0.0.1:8890/hardware/api",
  baseURL: "https://hardware.zsjblog.com/hardware/api", 
  headers: {"Content-Type": "application/json"},
  timeout: 50000,
})

/*是否有请求正在刷新token*/
window.isRefreshing = false
/*被挂起的请求数组*/
let refreshSubscribers = []


// 检查token实效性
function isTokenExpired(){
  let expiredTime = window.localStorage.getItem('token_time');
  if (!expiredTime) {
    return false;
  }
  let nowTime = new Date().getTime() /1000;
  return ((expiredTime - nowTime) < 10) ? true : false;
}

// 刷新token
function refreshToken(data) {
  const path = `/v2/update/tokens`;
  let refresh_token = window.localStorage.getItem("refresh_token");
  return service.post(path, {
      "data": {
        "refresh_token": refresh_token
      }
    })
    .then(res => res.data)
}

// 请求拦截
service.interceptors.request.use(
  (config) => {
    config.headers.Authorization = `Token ${window.localStorage.getItem('access_token')}`;
    // 登录接口和刷新token接口绕过
    if (config.url.indexOf('/update/tokens') >= 0 || config.url.indexOf('/login') >= 0) {
      return config;
    }
    if (isTokenExpired()) {
      if (!window.isRefreshing) {
        /*将刷新token的标志置为true*/
        window.isRefreshing = true;
        refreshToken().then(res => {
          const { access_token, token_time } = res.data
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('token_time', token_time);
          window.isRefreshing = false
          return access_token
        }).then((token) =>{
          refreshSubscribers.forEach(cb => cb(token))
          refreshSubscribers = [] 
        }).catch(error => {
            console.log('refresh token error: ', error)
        })
      }
      // 暂存拦截请求 
      const retry = new Promise((resolve) => {
        refreshSubscribers.push((token) => {
          config.headers.Authorization = 'Token ' + token;
          resolve(config);
        })
      })
      return retry;
    }
    return config;
  },
  (error) => {
    console.log(error);
    message.error("网站繁忙,请稍后再试!");
    return Promise.reject(error);
  }
);

// 响应拦截
service.interceptors.response.use(
  (response) => {
    const { status } = response.data;
    switch (status){
      case 401:
        window.localStorage.clear();
        message.error(response.data.message);
        window.location.href = '/login';
        break;
      case 401.1:
        window.localStorage.clear();
        message.error(response.data.message);
        window.location.href = '/login';
        break;
      case 403:
        message.error(response.data.message);
        break;
      default:
        return response;
    }
  },
  (error) => {
    console.log(error);
    message.error("网站繁忙,请稍后再试!");
    return Promise.reject(error);
  }

)

export default service;
