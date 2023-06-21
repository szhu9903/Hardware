import React, { useEffect, useState } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function OperateEquip(props) {

  const [equipForm] = Form.useForm();

  const dispatch = useDispatch();
  const { isOperateHardwareEquip, hardwareEquipTotalSize, hardwareEquipDetail, hardwareType } = useSelector((state) => state.hardware);

  useEffect(() => {
    // 修改文章，渲染文章数据到表单
    if (Object.keys(hardwareEquipDetail).length !== 0){
      let formValue = {
        ...hardwareEquipDetail,
        he_type: hardwareEquipDetail.he_type[0].id + "",
      }
      equipForm.setFieldsValue(formValue);
    }
  }, [hardwareEquipDetail])

  // 关闭对话框
  const closeOperate = () => {
    equipForm.resetFields();
    dispatch(action.hardware.updateData({isOperateHardwareEquip: false, hardwareEquipDetail: {}}));
  }

  // 提交文章
  const submitEquip = async (values) => {
    let equipData = {
      data:{
        ...values,
      }
    }
    let response = {};
    if (values.id === undefined){
      response = await api.hardware.addHardwareEquip(equipData);
    }else{
      response = await api.hardware.modifyHardwareEquip({id: values.id}, equipData);
    }
    if (response.data.status === 200) {
      message.success("提交成功！")
      closeOperate();
      let pageIndex = Math.ceil(hardwareEquipTotalSize/sysPageSize)
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.hardware.getHardwareEquip(getListParam));
    }
    
  }

  return (
    <>
      <Modal 
        title={hardwareEquipDetail.id?"修改文章":"创建文章"}
        centered
        forceRender
        visible={isOperateHardwareEquip}
        onCancel={closeOperate}
        footer={null}
        width={900}
      >
        {/* <div style={{ height: '60vh', overflowY: 'auto' }}>
        </div> */}
        <Form
          form={equipForm}
          name="basic"
          // initialValues={hardwareEquipDetail}
          onFinish={submitEquip}
          autoComplete="off"
        >
          <Form.Item name="id" hidden={true}><Input /></Form.Item>
          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="设备名称"
                name="he_name"
                rules={[{ required: true, message: '请填写设备名称!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="设备编码"
                name="he_num"
                rules={[{ required: true, message: '请填写设备编号!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="设备分类"
                name="he_type"
                rules={[{ required: true, message: '请选择设备类型!' }]}
              >
                <Select placeholder="选择设备类型" >
                  {hardwareType && 
                    hardwareType.map(typeItem => <Select.Option key={typeItem.id}>{typeItem.ht_name}</Select.Option>)
                  }
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="设备启用状态"
                name="he_starttype"
                rules={[{ required: true, message: 'Please input your blog type!' }]}
              >
                <Select placeholder="启用状态" >
                  <Select.Option key={'START'}>启用</Select.Option>
                  <Select.Option key={'STOP'}>停用</Select.Option>
                  <Select.Option key={'UNASSIGNED'}>待分配</Select.Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item wrapperCol={{ offset: 21, span: 3 }}>
            <Button type="primary" htmlType="submit">
              {hardwareEquipDetail.id?"修改设备":"创建设备"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
