import React, { useEffect, useState } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function OperateRole(props) {

  const [roleForm] = Form.useForm();

  const dispatch = useDispatch();
  const { isOperateSysRole, sysRoleTotalSize, sysRoleDetail, sysPurviewList, sysMenuList  } = useSelector((state) => state.sys)

  useEffect(() => {
    // 修改文章，渲染文章数据到表单
    if (Object.keys(sysRoleDetail).length !== 0){
      let formValue = {
        ...sysRoleDetail,
        r_purview: sysRoleDetail.r_purview ? sysRoleDetail.r_purview.map((purview) => purview.id + ""):[],
        r_menu: sysRoleDetail.r_menu ? sysRoleDetail.r_menu.map((menu) => menu.id + ""):[],
      }
      roleForm.setFieldsValue(formValue);
    }
  }, [sysRoleDetail])

  // 关闭对话框
  const closeOperateRole = () => {
    roleForm.resetFields();
    dispatch(action.sys.updateData({isOperateSysRole: false, sysRoleDetail: {}}));
  }

  // 提交
  const submitRole = async (values) => {
    console.log("all",values);
    let roleData = {
      data:{
        ...values,
        r_purview: values.r_purview.map((purview) => ({rp_purviewid: purview})),
        r_menu: values.r_menu.map((menu) => ({rm_menuid: menu}))
      }
    }
    let response = {};
    if (values.id === undefined){
      response = await api.sys.addSysRole(roleData);
    }else{
      response = await api.sys.modifySysRole({id: values.id}, roleData);
    }
    if (response.data.code === 6) {
      message.success("提交成功！")
      closeOperateRole();
      let pageIndex = Math.ceil(sysRoleTotalSize/sysPageSize)
      let getRoleParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.sys.getSysRole(getRoleParam));
    }else {
      message.error(response.data.message);
    }
    
  }

  return (
    <>
      <Modal 
        title={sysRoleDetail.id?"修改角色":"创建角色"}
        centered
        visible={isOperateSysRole}
        onCancel={closeOperateRole}
        footer={null}
        width={900}
      >
        {/* <div style={{ height: '60vh', overflowY: 'auto' }}>
        </div> */}
        <Form
          form={roleForm}
          name="basic"
          onFinish={submitRole}
          autoComplete="off"
        >
          <Form.Item name="id" hidden={true}><Input /></Form.Item>

          <Form.Item
            label="角色名称"
            name="sr_name"
            rules={[{ required: true, message: 'Please input your blog title!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="权限项"
            name="r_purview"
            rules={[{ required: true, message: 'Please input your blog type!' }]}
          >
            <Select mode="multiple" placeholder="选择权限项">
              {sysPurviewList && 
                sysPurviewList.map(purview => <Select.Option key={purview.id}>{purview.sp_name}</Select.Option>)
              }
            </Select>
          </Form.Item>

          <Form.Item
            label="菜单项"
            name="r_menu"
            rules={[{ required: true, message: 'Please input your blog type!' }]}
          >
            <Select mode="multiple" placeholder="选择菜单项">
              {sysMenuList && 
                sysMenuList.map(menu => <Select.Option key={menu.id}>{menu.sm_name}</Select.Option>)
              }
            </Select>
          </Form.Item>
          
          <Form.Item wrapperCol={{ offset: 21, span: 3 }}>
            <Button type="primary" htmlType="submit">
              {sysRoleDetail.id?"修改角色":"创建角色"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
