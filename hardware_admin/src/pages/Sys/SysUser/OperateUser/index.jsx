import React, { useEffect, useState } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function OperateUser(props) {

  const [userForm] = Form.useForm();

  const dispatch = useDispatch();
  const { sysRole } = useSelector((state) => state.sys)
  const { isOperateUser, sysUserTotalSize, sysUserDetail } = useSelector((state) => state.user)

  useEffect(() => {
    // 修改文章，渲染文章数据到表单
    if (Object.keys(sysUserDetail).length !== 0){
      let formValue = {
        ...sysUserDetail,
        su_isadmin: sysUserDetail.su_isadmin + "",
        u_role: sysUserDetail.u_role ? sysUserDetail.u_role.map((role) => role.id + ""):[],
      }
      userForm.setFieldsValue(formValue);
    }
  }, [sysUserDetail])

  // 关闭对话框
  const closeOperateUser = () => {
    userForm.resetFields();
    dispatch(action.user.updateData({isOperateUser: false, sysUserDetail: {}}));
  }

  // 提交
  const submitUser = async (values) => {
    console.log("all",values);
    let userData = {
      data:{
        ...values,
        u_role: values.u_role.map((role) => ({ur_roleid: role}))
      }
    }
    let response = {};
    if (values.id === undefined){
      response = await api.user.addSysUser(userData);
    }else{
      response = await api.user.modifySysUser({id: values.id}, userData);
    }
    if (response.data.code === 6) {
      message.success("提交成功！")
      closeOperateUser();
      let pageIndex = Math.ceil(sysUserTotalSize/sysPageSize)
      let getUserParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.user.getSysUser(getUserParam));
    }else {
      console.log(response.data);
      message.error(response.data.message);
    }
    
  }

  return (
    <>
      <Modal 
        title={sysUserDetail.id?"修改用户":"创建用户"}
        centered
        visible={isOperateUser}
        onCancel={closeOperateUser}
        footer={null}
        width={900}
      >
        {/* <div style={{ height: '60vh', overflowY: 'auto' }}>
        </div> */}
        <Form
          form={userForm}
          name="basic"
          onFinish={submitUser}
          autoComplete="off"
        >
          <Form.Item name="id" hidden={true}><Input /></Form.Item>

              <Form.Item
                label="账号"
                name="su_account"
                rules={[{ required: true, message: '请输入账号!' }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="密码"
                name="su_pwd"
                hidden={sysUserDetail.id ? true : false}
                rules={[{ required: true, message: '请输入密码!' }]}
              >
                <Input.Password />
              </Form.Item>


          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="用户名"
                name="su_username"
                rules={[{ required: true, message: '请输入用户名!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="性别"
                name="su_sex"
                rules={[{ required: true, message: '请选择性别!' }]}
              >
                <Select placeholder="选择性别" >
                  <Select.Option key="男">男</Select.Option>
                  <Select.Option key="女">女</Select.Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="电话号"
                name="su_phone"
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="邮箱"
                name="su_email"
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="头像地址"
                name="su_userphoto"
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="后台"
                name="su_isadmin"
                rules={[{ required: true, message: '请选择是否可登入后台!' }]}
              >
                <Select placeholder="是否允许后台" >
                  <Select.Option key={0}>禁止</Select.Option>
                  <Select.Option key={1}>允许</Select.Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            label="角色"
            name="u_role"
            rules={[{ required: true, message: '请选择角色!' }]}
          >
            <Select mode="multiple" placeholder="选择角色">
              {sysRole && 
                sysRole.map(role => <Select.Option key={role.id}>{role.sr_name}</Select.Option>)
              }
            </Select>
          </Form.Item>
          
          <Form.Item wrapperCol={{ offset: 21, span: 3 }}>
            <Button type="primary" htmlType="submit">
              {sysUserDetail.id?"修改用户":"创建用户"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
