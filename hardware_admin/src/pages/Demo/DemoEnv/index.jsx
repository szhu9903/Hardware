import React, { useEffect, useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, message } from 'antd';
import action from '../../../redux/actions'
import { columns } from './columns';
import { sysPageSize } from '../../../utils/config';
import { initWebsocket } from '../../../utils/socket';
import './index.css'


export default function DemoEnv() {

  const dispatch = useDispatch();
  const { demoEnv, demoEnvTotalSize } = useSelector((state) => state.demo);
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
        let getListParam = `pagination=1,${sysPageSize}`;
        dispatch(action.demo.getDemoEnv(getListParam));
      }else {
        message.error(message_data.message);
      }
    };
    return () => {
      ws.current?.close();
    };
  }, [ws])

  // 加载页面数据
  useEffect(() => {
    let getListParam = `pagination=1,${sysPageSize}`;
    dispatch(action.demo.getDemoEnv(getListParam));
  }, [])

  // 发送指令
  const sendCommand = (record) => () => {
    let msgData = {
      event: 'demo_query_env_cmd',
      equip_code: record.de_equipcode,
      message_data: {}
    }
    ws.current?.send(JSON.stringify(msgData));
  }

  // 分页
  const onChangPage = (pagination) => {
    let getListParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.demo.getDemoEnv(getListParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize: sysPageSize,
    total: demoEnvTotalSize,
  }

  return (
    <div>
      <div className='blog-tab'>
        <Table 
          size="middle" 
          columns={columns(sendCommand)} 
          dataSource={demoEnv} 
          rowKey={env => env.id} 
          onChange={onChangPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
