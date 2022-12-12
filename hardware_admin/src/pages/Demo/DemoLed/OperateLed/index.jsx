import React, { useEffect, useState } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function OperateLed(props) {

  const [ledForm] = Form.useForm();

  const dispatch = useDispatch();
  const { isOperateDemoLed, demoLedTotalSize, demoLedDetail } = useSelector((state) => state.demo);

  useEffect(() => {
    // 渲染数据到表单
    if (Object.keys(demoLedDetail).length !== 0){
      let formValue = {
        ...demoLedDetail,
        dl_switch: demoLedDetail.dl_switch + "",
      }
      ledForm.setFieldsValue(formValue);
    }
  }, [demoLedDetail])

  // 关闭对话框
  const closeOperate = () => {
    ledForm.resetFields();
    dispatch(action.demo.updateData({isOperateDemoLed: false, demoLedDetail: {}}));
  }

  // 提交文章
  const submitLed = async (values) => {
    let ledData = {
      data:{
        ...values,
      }
    }
    let response = {};
    response = await api.demo.modifyDemoLed({id: values.id}, ledData);
    if (response.data.status === 200) {
      message.success("提交成功！")
      closeOperate();
      let pageIndex = Math.ceil(demoLedTotalSize/sysPageSize)
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.demo.getDemoLed(getListParam));
    }
    
  }

  return (
    <>
      <Modal 
        title="修改LED"
        centered
        visible={isOperateDemoLed}
        onCancel={closeOperate}
        footer={null}
        width={900}
      >
        {/* <div style={{ height: '60vh', overflowY: 'auto' }}>
        </div> */}
        <Form
          form={ledForm}
          name="basic"
          onFinish={submitLed}
          autoComplete="off"
        >
          <Form.Item name="id" hidden={true}><Input /></Form.Item>
          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="开/关"
                name="dl_switch"
                rules={[{ required: true, message: '请选择开/关!' }]}
              >
                <Select placeholder="开/关" >
                  <Select.Option key={0}>开</Select.Option>
                  <Select.Option key={1}>关</Select.Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="红"
                name="dl_r"
                rules={[{ required: true, message: '请填写0～255!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="绿"
                name="dl_g"
                rules={[{ required: true, message: '请填写0～255!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="蓝"
                name="dl_b"
                rules={[{ required: true, message: '请填写0～255!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item wrapperCol={{ offset: 21, span: 3 }}>
            <Button type="primary" htmlType="submit">修改LED</Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
