import { baseWs } from './config';
import { message } from 'antd';

export function initWebsocket(url) {
  var ws = new WebSocket(`${baseWs}/${url}/?token=${window.localStorage.getItem('access_token')}`);
  ws.onopen = () => {
    console.log('open OK');
  };
  ws.onclose = () => {
    console.log('close OK');
  };
  ws.onerror = (error) => {
    console.log('error');
  };
  ws.onmessage = (event) => {
    let message_data = JSON.parse(event.data);
    console.log('Received message:', message_data);
    if(message_data && message_data.code !== 0x06){
      message.success(message_data.message);
    }else {
      message.error(message_data.message);
    }
  };
  return ws
}
