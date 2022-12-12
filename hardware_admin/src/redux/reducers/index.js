
import { combineReducers } from 'redux'
import login from './login'
import user from './user'
import sys from './sys'
import hardware from './hardware'
import demo from './demo'

export default combineReducers({
  login,
  user,
  sys,
  hardware,
  demo,
})
