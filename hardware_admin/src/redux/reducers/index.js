
import { combineReducers } from 'redux'
import login from './login'
import user from './user'
import sys from './sys'
import hardware from './hardware'
import demo from './demo'
import full103 from './full103'

export default combineReducers({
  login,
  user,
  sys,
  hardware,
  demo,
  full103,
})
