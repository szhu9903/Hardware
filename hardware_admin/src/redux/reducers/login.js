import { UPDATE_IS_SHOW_LOGIN } from "../constants";


const initState = {
  isShowLogin: false,
}

export default function login(preState=initState, action) {
  const { type, data } = action;
  switch (type) {

    case UPDATE_IS_SHOW_LOGIN:
      return {...preState, isShowLogin: data.isShowLogin};
    
    default:
      return preState;
  }
}

