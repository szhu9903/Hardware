import React, { useEffect, useState } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function OperateConfigVar(props) {

  const [configVarForm] = Form.useForm();

  const dispatch = useDispatch();
  const { isOperateHardwareConfigVar, hardwareConfigVarTotalSize, hardwareConfigVarDetail, hardwareType } = useSelector((state) => state.hardware);

  useEffect(() => {
    // 修改配置
    if (Object.keys(hardwareConfigVarDetail).length !== 0){
      console.log('hardwareConfigVarDetail', hardwareConfigVarDetail);
      let formValue = {
        ...hardwareConfigVarDetail,
        hcv_type: hardwareConfigVarDetail.hcv_type ? hardwareConfigVarDetail.hcv_type[0].id + "" : 'null',
      }
      configVarForm.setFieldsValue(formValue);
    }
  }, [hardwareConfigVarDetail])

  // 关闭对话框
  const closeOperate = () => {
    configVarForm.resetFields();
    dispatch(action.hardware.updateData({isOperateHardwareConfigVar: false, hardwareConfigVarDetail: {}}));
  }

  // 提交分类
  const submitConfigVar = async (values) => {
    if(!values.hcv_type || values.hcv_type === 'null'){
      delete values.hcv_type;
    }
    let configVarData = {
      data:{
        ...values,
      }
    }
    let response = {};
    if (values.id === undefined){
      response = await api.hardware.addHardwareConfigVar(configVarData);
    }else{
      response = await api.hardware.modifyHardwareConfigVar({id: values.id}, configVarData);
    }
    if (response.data.status === 200 && response.data.code === 6) {
      message.success("提交成功！")
      closeOperate();
      let pageIndex = Math.ceil(hardwareConfigVarTotalSize/sysPageSize)
      let getListParam = `pagination=${pageIndex},${sysPageSize}`;
      dispatch(action.hardware.getHardwareConfigVar(getListParam));
    }
    
  }

  return (
    <>
      <Modal 
        title={hardwareConfigVarDetail.id?"修改配置项":"创建配置项"}
        centered
        visible={isOperateHardwareConfigVar}
        onCancel={closeOperate}
        footer={null}
        width={900}
      >
        <Form
          form={configVarForm}
          name="basic"
          // initialValues={hardwareTypeDetail}
          onFinish={submitConfigVar}
          autoComplete="off"
        >
          <Form.Item name="id" hidden={true}><Input /></Form.Item>

          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="参数项名称"
                name="hcv_variablekey"
                rules={[{ required: true, message: '请填写参数项名称!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="参数项取值"
                name="hcv_variablevalue"
                rules={[{ required: true, message: '请填写参数项取值!' }]}
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={20}>
            <Col span={12}>
              <Form.Item
                label="设备类型"
                name="hcv_type"
                rules={[{ required: true, message: '请选择设备类型!' }]}
              >
                <Select placeholder="选择设备类型" >
                  <Select.Option key={null}>全局</Select.Option>
                  {hardwareType && 
                    hardwareType.map(typeItem => <Select.Option key={typeItem.id}>{typeItem.ht_name}</Select.Option>)
                  }
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="描述"
                name="hcv_describe"
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item wrapperCol={{ offset: 21, span: 3 }}>
            <Button type="primary" htmlType="submit">
              {hardwareConfigVarDetail.id?"修改配置项":"创建配置项"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
