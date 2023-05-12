import React, { useEffect, useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Switch, Tooltip, Button, message, Card } from 'antd';
import { EditOutlined, RedoOutlined, SettingOutlined } from '@ant-design/icons';
import { initWebsocket } from '../../../utils/socket';
import action from '../../../redux/actions'
import { columns } from './columns';
import { sysPageSize } from '../../../utils/config';
import api from '../../../api';
import './index.css'

const { Meta } = Card;

export default function Full103Main() {

  const dispatch = useDispatch();
  const { full103Data, full103TotalSize } = useSelector((state) => state.full103);
  const ws = useRef(null);

  // 创建websocket
  useEffect(() => {
    ws.current = initWebsocket('asyncfunc');
    // 接收到websocket消息
    ws.current.onmessage = (event) => {
      let message_data = JSON.parse(event.data);
      console.log('Received message:', message_data);
      if(message_data && message_data.code === 0x06){
        message.success(message_data.message);
        dispatch(action.full103.getFull103Data(null));
      }else {
        message.error(message_data.message);
      }
    };
    return () => {
      ws.current?.close();
    };
  }, [ws])

  useEffect(() => {
    dispatch(action.full103.getFull103Data(null));
  }, [])


  // console.log('得到的', full103Data);

  const onChange = async (checked, item) => {
    console.log(`switch to ${checked}`, item);
    let ledData = {
      data:{
        fr_switch: checked ? 0 : 1,
      }
    }
    let response = {};
    response = await api.full103.modifyFull103Data({id: item.relay_id}, ledData);
    if (response.data.status === 200) {
      message.success("更新成功！");
      dispatch(action.full103.getFull103Data(null));
    }
  };

  const refresh = (record) => {
    console.log(`刷新环境数据`);
    let msgData = {
      event: 'full103_query_env_cmd',
      equip_code: record.he_num,
      message_data: {}
    }
    ws.current?.send(JSON.stringify(msgData));

  };


  return (
    <div>
      {full103Data && full103Data.map(item => {
        return <Card
          key={item.id}
          style={{
            width: 300,
          }}
          actions={[
            <Tooltip title="开关"><Switch checked={!item.fr_switch} onChange={(checked) => onChange(checked, item)} /></Tooltip>,
            <RedoOutlined key="ellipsis" onClick={() => refresh(item)} />,
          ]}
        >
          <div>
            <span className='title'>{item.he_name}</span>
            <span className='status'>{item.he_equipstatus=="LINKED" ? '在线' : '离线'}</span>
          </div>
          <p className='env'>
            <span>温度：{item.fe_temperature}</span>
            <span>湿度：{item.fe_humidity}</span>
          </p>
        </Card>
      })}
    </div>
  )
}
