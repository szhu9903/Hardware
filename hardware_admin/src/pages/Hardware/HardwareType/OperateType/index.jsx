import React, { useEffect, useState } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function OperateType(props) {

  const [typeForm] = Form.useForm();

  const dispatch = useDispatch();
  const { isOperateHardwareType, hardwareTypeTotalSize, hardwareTypeDetail } = useSelector((state) => state.hardware);

  useEffect(() => {
    // 修改分类，渲染文章数据到表单
    if (Object.keys(hardwareTypeDetail).length !== 0){
      let formValue = {
        ...hardwareTypeDetail,
      }
      typeForm.setFieldsValue(formValue);
    }
  }, [hardwareTypeDetail])

  // 关闭对话框
  const closeOperate = () => {
    typeForm.resetFields();
    dispatch(action.hardware.updateData({isOperateHardwareType: false, hardwareTypeDetail: {}}));
  }

  // 提交分类
  const submitType = async (values) => {
    let typeData = {
      data:{
        ...values,
      }
    }
    let response = {};
    if (values.id === undefined){
      response = await api.hardware.addHardwareType(typeData);
    }else{
      response = await api.hardware.modifyHardwareType({id: values.id}, typeData);
    }
    if (response.data.status === 200) {
      message.success("提交成功！")
      closeOperate();
      let pageIndex = Math.ceil(hardwareTypeTotalSize/sysPageSize)
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.hardware.getHardwareType(getListParam));
    }
    
  }

  return (
    <>
      <Modal 
        title={hardwareTypeDetail.id?"修改分类":"创建分类"}
        centered
        visible={isOperateHardwareType}
        onCancel={closeOperate}
        footer={null}
        width={900}
      >
        {/* <div style={{ height: '60vh', overflowY: 'auto' }}>
        </div> */}
        <Form
          form={typeForm}
          name="basic"
          // initialValues={hardwareTypeDetail}
          onFinish={submitType}
          autoComplete="off"
        >
          <Form.Item name="id" hidden={true}><Input /></Form.Item>
          <Form.Item
            label="分类名称"
            name="ht_name"
            rules={[{ required: true, message: '请填写分类名称!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item wrapperCol={{ offset: 21, span: 3 }}>
            <Button type="primary" htmlType="submit">
              {hardwareTypeDetail.id?"修改分类":"创建分类"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
