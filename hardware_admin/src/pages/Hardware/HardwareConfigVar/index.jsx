import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Select, Input, Button, message } from 'antd';
import action from '../../../redux/actions'
import { columns } from './columns';
import { sysPageSize } from '../../../utils/config';
import OperateConfigVar from './OperateConfigVar';
import api from '../../../api';
import './index.css'


export default function HardwareConfigVar() {

  const dispatch = useDispatch();
  const { hardwareConfigVar, hardwareConfigVarTotalSize } = useSelector((state) => state.hardware);

  useEffect(() => {
    dispatch(action.hardware.getHardwareType());
    let getListParam = `pagination=1,${sysPageSize}`;
    dispatch(action.hardware.getHardwareConfigVar(getListParam));
  }, [])

  // 标题搜索
  const searchHardwareConfigVar = (value) => {
    let getListParam = `fuzzyfilter=hcv_variablekey=${value}&pagination=1,${sysPageSize}`;
    dispatch(action.hardware.getHardwareConfigVar(getListParam));
  }

  // 创建设备分类
  const createHardwareConfigVar = () => {
    dispatch(action.hardware.updateData({isOperateHardwareConfigVar: true, hardwareConfigVarDetail:{}}));
  }

  // 修改设备分类
  const updateHaredwareConfigVar = (record) => () => {
    dispatch(action.hardware.updateData({isOperateHardwareConfigVar: true, hardwareConfigVarDetail: record}));
  }

  // 删除设备分类
  const deleteHardwareConfigVar = (record) => async () => {
    let response = await api.hardware.delHardwareConfigVar({id: record.id});
    if (response.data.status === 200) {
      let pageIndex = Math.ceil((hardwareConfigVarTotalSize-1)/sysPageSize);
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.hardware.getHardwareConfigVar(getListParam));
    }

  }

  // 分页
  const onChangPage = (pagination) => {
    let getListParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.hardware.getHardwareConfigVar(getListParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize:sysPageSize,
    total: hardwareConfigVarTotalSize,
  }

  return (
    <div>
      <OperateConfigVar />
      <div className='blog-search'>
        <Input.Search placeholder="配置项搜索" onSearch={searchHardwareConfigVar} style={{ width: 230 }} enterButton allowClear />
        <Button className='create-btn' type="primary" onClick={createHardwareConfigVar} >新配置项</Button>
      </div>
      <div className='blog-tab'>
        <Table 
          size="middle" 
          columns={columns(updateHaredwareConfigVar, deleteHardwareConfigVar)} 
          dataSource={hardwareConfigVar} 
          rowKey={config => config.id} 
          onChange={onChangPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
