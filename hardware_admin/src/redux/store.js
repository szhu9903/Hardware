import { applyMiddleware, createStore } from 'redux'
// 异步处理action
import thunk from 'redux-thunk'
// 导入reducers 处理数据
import reducers from './reducers'

export default createStore(reducers, applyMiddleware(thunk))
