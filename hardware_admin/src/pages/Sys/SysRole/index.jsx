import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Select, Input, Button, message } from 'antd';
import action from '../../../redux/actions'
import { roleColumns } from './columns';
import { sysPageSize } from '../../../utils/config';
import OperateRole from './OperateRole';
import api from '../../../api';
import './index.css'


export default function SysRole() {

  const dispatch = useDispatch();
  const { sysRole, sysRoleTotalSize } = useSelector((state) => state.sys);

  useEffect(() => {
    dispatch(action.sys.getSysMenu());
    dispatch(action.sys.getSysPurview());
    let getRoleParam = `pagination=1,${sysPageSize}`;
    dispatch(action.sys.getSysRole(getRoleParam));
  }, [])

  // 标题搜索 
  const searchRoleName = (value) => {
    let getRoleParam = `fuzzyfilter=sr_name=${value}&pagination=1,${sysPageSize}`;
    dispatch(action.sys.getSysRole(getRoleParam));
  }

  // 创建角色
  const createRole = () => {
    dispatch(action.sys.updateData({isOperateSysRole: true, sysRoleDetail:{}}));
  }

  // 修改用户
  const updateRole = (record) => () => {
    dispatch(action.sys.updateData({isOperateSysRole: true, sysRoleDetail: record}));
  }

  // 删除用户
  const deleteRole = (record) => async () => {
    console.log('删除用户', record);
    let response = await api.sys.delSysRole({id: record.id});
    if (response.data.status === 200) {
      message.success("删除成功！")
      let pageIndex = Math.ceil((sysRoleTotalSize-1)/sysPageSize);
      let getRoleParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.sys.getSysRole(getRoleParam));
    }

  }

  // 分页
  const onChangPage = (pagination) => {
    let getRoleParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.sys.getSysRole(getRoleParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize:sysPageSize,
    total: sysRoleTotalSize,
  }

  return (
    <div>
      <OperateRole />
      <div className='blog-search'>
        <Input.Search placeholder="标题搜索" onSearch={searchRoleName} style={{ width: 230 }} enterButton allowClear />
        <Button className='create-btn' type="primary" onClick={createRole} >创建新角色</Button>
      </div>
      <div className='blog-tab'>
        <Table 
          size="middle" 
          columns={roleColumns(updateRole, deleteRole)} 
          dataSource={sysRole} 
          rowKey={role => role.id} 
          onChange={onChangPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
