import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Select, Input, Button, message } from 'antd';
import action from '../../../redux/actions'
import { columns } from './columns';
import { sysPageSize } from '../../../utils/config';
import OperateLed from './OperateLed';
import api from '../../../api';
import './index.css'


export default function DemoLed() {

  const dispatch = useDispatch();
  const { demoLed, demoLedTotalSize } = useSelector((state) => state.demo);

  useEffect(() => {
    let getListParam = `pagination=1,${sysPageSize}`;
    dispatch(action.demo.getDemoLed(getListParam));
  }, [])

  // 修改文章
  const updateDemoLed = (record) => () => {
    dispatch(action.demo.updateData({isOperateDemoLed: true, demoLedDetail: record}));
  }

  // 分页
  const onChangPage = (pagination) => {
    let getListParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.demo.getDemoLed(getListParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize:sysPageSize,
    total: demoLedTotalSize,
  }

  return (
    <div>
      <OperateLed />
      <div className='blog-tab'>
        <Table 
          size="middle" 
          columns={columns(updateDemoLed)} 
          dataSource={demoLed} 
          rowKey={led => led.id} 
          onChange={onChangPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
