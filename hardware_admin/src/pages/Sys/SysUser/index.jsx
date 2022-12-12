import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Table, Select, Input, Button, message } from 'antd';
import action from '../../../redux/actions'
import { userColumns } from './columns';
import { sysPageSize } from '../../../utils/config';
import OperateUser from './OperateUser';
import api from '../../../api';
import './index.css'


export default function SysUser() {

  const dispatch = useDispatch();
  const { sysUserList, sysUserTotalSize } = useSelector((state) => state.user);

  useEffect(() => {
    dispatch(action.sys.getSysRole());
    let getUserParam = `pagination=1,${sysPageSize}`;
    dispatch(action.user.getSysUser(getUserParam));
  }, [])

  // 标题搜索 bu_username
  const searchUserName = (value) => {
    let getUserParam = `fuzzyfilter=su_username=${value}&pagination=1,${sysPageSize}`;
    dispatch(action.user.getSysUser(getUserParam));
  }

  // 创建用户
  const createUser = () => {
    dispatch(action.user.updateData({isOperateUser: true, sysUserDetail:{}}));
  }

  // 修改用户
  const updateUser = (record) => () => {
    dispatch(action.user.updateData({isOperateUser: true, sysUserDetail: record}));
  }

  // 删除用户
  const deleteUser = (record) => async () => {
    console.log('删除用户', record);
    let response = await api.user.delSysUser({id: record.id});
    if (response.data.status === 200) {
      message.success("删除成功！")
      let pageIndex = Math.ceil((sysUserTotalSize-1)/sysPageSize);
      let getUserParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.user.getSysUser(getUserParam));
    }

  }

  // 分页
  const onChangUserPage = (pagination) => {
    let getUserParam = `pagination=${pagination.current},${sysPageSize}`;
    dispatch(action.user.getSysUser(getUserParam));
  }

  // tab 分页参数
  const tabPagination = {
    pageSize:sysPageSize,
    total: sysUserTotalSize,
  }

  return (
    <div>
      <OperateUser />
      <div className='blog-search'>
        <Input.Search placeholder="标题搜索" onSearch={searchUserName} style={{ width: 230 }} enterButton allowClear />
        <Button className='create-btn' type="primary" onClick={createUser} >创建新用户</Button>
      </div>
      <div className='blog-tab'>
        <Table 
          size="middle"
          columns={userColumns(updateUser, deleteUser)} 
          dataSource={sysUserList} 
          rowKey={user => user.id} 
          onChange={onChangUserPage}
          pagination={tabPagination}
        />
      </div>
    </div>
  )
}
