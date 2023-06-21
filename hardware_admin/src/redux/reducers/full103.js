import { UPDATE_DATA, GET_FULL103_DATA} from '../constants'

const initState = {
  full103Data: [],
  full103TotalSize: null,
}

export default function full103(preState=initState, action) {
  const { type, data } = action;
  switch (type) {

    case GET_FULL103_DATA:
      return {...preState, full103Data: data.data, full103TotalSize: data.total_count};
    
    case UPDATE_DATA:
      return {...preState, ...data}

    default:
      return preState;
  }
}

