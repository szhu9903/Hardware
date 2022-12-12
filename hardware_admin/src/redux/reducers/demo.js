import { UPDATE_DATA, GET_DEMO_LED, GET_DEMO_ENV} from '../constants'

const initState = {
  // LED
  demoLed: [],
  demoLedDetail: {},
  demoLedTotalSize: null,
  isOperateDemoLed: false,
  //ENV
  demoEnv: [],
  demoEnvTotalSize: null,
}

export default function blog(preState=initState, action) {
  const { type, data } = action;
  switch (type) {

    case GET_DEMO_LED:
      return {...preState, demoLed: data.data, demoLedTotalSize: data.total_count};
    
    case GET_DEMO_ENV:
      return {...preState, demoEnv: data.data, demoEnvTotalSize: data.total_count};
    
    case UPDATE_DATA:
      return {...preState, ...data}

    default:
      return preState;
  }
}

