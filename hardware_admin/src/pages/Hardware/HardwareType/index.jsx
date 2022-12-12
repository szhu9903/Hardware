import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Select, Input, Button, message } from 'antd';
import action from '../../../redux/actions'
import { columns } from './columns';
import { sysPageSize } from '../../../utils/config';
import OperateType from './OperateType';
import api from '../../../api';
import './index.css'


export default function HardwareType() {

  const dispatch = useDispatch();
  const { hardwareType, hardwareTypeTotalSize } = useSelector((state) => state.hardware);

  useEffect(() => {
    let getListParam = `pagination=1,${sysPageSize}`;
    dispatch(action.hardware.getHardwareType(getListParam));
  }, [])

  // 标题搜索
  const searchHardwareType = (value) => {
    let getListParam = `fuzzyfilter=ht_name=${value}&pagination=1,${sysPageSize}`;
    dispatch(action.hardware.getHardwareType(getListParam));
  }

  // 创建设备分类
  const createHardwareType = () => {
    dispatch(action.hardware.updateData({isOperateHardwareType: true, hardwareTypeDetail:{}}));
  }

  // 修改设备分类
  const updateHaredwareType = (record) => () => {
    dispatch(action.hardware.updateData({isOperateHardwareType: true, hardwareTypeDetail: record}));
  }

  // 删除设备分类
  const deleteHardwareType = (record) => async () => {
    console.log('删除设备分类', record);
    let response = await api.hardware.delHardwareType({id: record.id});
    if (response.data.status === 200) {
      message.success("删除成功！")
      let pageIndex = Math.ceil((hardwareTypeTotalSize-1)/sysPageSize);
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.hardware.getHardwareType(getListParam));
    }

  }

  // 分页
  const onChangPage = (pagination) => {
    let getListParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.hardware.getHardwareType(getListParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize:sysPageSize,
    total: hardwareTypeTotalSize,
  }

  return (
    <div>
      <OperateType />
      <div className='blog-search'>
        <Input.Search placeholder="标题搜索" onSearch={searchHardwareType} style={{ width: 230 }} enterButton allowClear />
        <Button className='create-btn' type="primary" onClick={createHardwareType} >新类型</Button>
      </div>
      <div className='blog-tab'>
        <Table 
          size="middle" 
          columns={columns(updateHaredwareType, deleteHardwareType)} 
          dataSource={hardwareType} 
          rowKey={type => type.id} 
          onChange={onChangPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
