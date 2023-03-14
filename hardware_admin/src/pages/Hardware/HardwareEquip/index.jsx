import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Select, Input, Button, message } from 'antd';
import action from '../../../redux/actions'
import { columns } from './columns';
import { sysPageSize } from '../../../utils/config';
import OperateEquip from './OperateEquip';
import AssignEquip from './AssignEquip';
import api from '../../../api';
import './index.css'


export default function HardwareEquip() {

  const dispatch = useDispatch();
  const { hardwareEquip, hardwareEquipTotalSize } = useSelector((state) => state.hardware);

  useEffect(() => {
    dispatch(action.hardware.getHardwareType());
    let getListParam = `pagination=1,${sysPageSize}`;
    dispatch(action.hardware.getHardwareEquip(getListParam));
  }, [])

  // 标题搜索
  const searchHardwareEquip = (value) => {
    let getListParam = `fuzzyfilter=he_name=${value}&pagination=1,${sysPageSize}`;
    dispatch(action.hardware.getHardwareEquip(getListParam));
  }

  // 创建设备
  const createHardwareEquip = () => {
    dispatch(action.hardware.updateData({isOperateHardwareEquip: true, hardwareEquipDetail:{}}));
  }

  // 修改设备
  const updateHaredwareEquip = (record) => () => {
    dispatch(action.hardware.updateData({isOperateHardwareEquip: true, hardwareEquipDetail: record}));
  }

  // 分配设备
  const assignHaredwareEquip = (record) => () => {
    dispatch(action.hardware.updateData({isAssignHardwareEquip: true, hardwareEquipDetail: record}));
    let getAssignParam = `filter=he_starttype=UNASSIGNED,he_effect=1,he_type=${record.he_type[0].id}`;
    dispatch(action.hardware.getAssignHardwareEquip(getAssignParam));
  }

  // 删除设备
  const deleteHardwareEquip = (record) => async () => {
    let response = await api.hardware.delHardwareEquip({id: record.id});
    if (response.data.status === 200) {
      message.success("删除成功！")
      let pageIndex = Math.ceil((hardwareEquipTotalSize-1)/sysPageSize);
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.hardware.getHardwareEquip(getListParam));
    }

  }

  // 分页
  const onChangPage = (pagination) => {
    let getListParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.hardware.getHardwareEquip(getListParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize:sysPageSize,
    total: hardwareEquipTotalSize,
  }

  return (
    <div>
      <OperateEquip />
      <AssignEquip />
      <div className='blog-search'>
        <Input.Search placeholder="标题搜索" onSearch={searchHardwareEquip} style={{ width: 230 }} enterButton allowClear />
        <Button className='create-btn' type="primary" onClick={createHardwareEquip} >新设备</Button>
      </div>
      <div className='blog-tab'>
        <Table 
          size="middle" 
          columns={columns(updateHaredwareEquip, deleteHardwareEquip, assignHaredwareEquip)} 
          dataSource={hardwareEquip} 
          rowKey={equip => equip.id} 
          onChange={onChangPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
