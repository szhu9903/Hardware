import React, { useEffect, useState, useRef } from 'react'
import { Modal, Form, Input, Select, Button, Row, Col, message } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { sysPageSize } from '../../../../utils/config';
import { initWebsocket } from '../../../../utils/socket';
import action from '../../../../redux/actions';
import api from '../../../../api';

export default function AssignEquip(props) {

  const [assignForm] = Form.useForm();

  const dispatch = useDispatch();
  const { isAssignHardwareEquip, hardwareEquipTotalSize, hardwareEquipDetail, hardwareType, assignHardwareEquip } = useSelector((state) => state.hardware);
  const ws = useRef(null);


  // 创建websocket
  useEffect(() => {
    ws.current = initWebsocket('asyncfunc');
    // 接收到websocket消息
    ws.current.onmessage = (event) => {
      let message_data = JSON.parse(event.data);
      console.log('Received message:', message_data);
      if(message_data && message_data.code === 0x06){
        message.success(message_data.message);
      }else {
        message.error(message_data.message);
      }
    };
    return () => {
      ws.current?.close();
    };
  }, [ws])

  // 关闭对话框
  const closeOperate = () => {
    assignForm.resetFields();
    dispatch(action.hardware.updateData({isAssignHardwareEquip: false, assignHardwareEquip: []}));
  }


  // 发送指令
  const sendCommand = (values) => {
    console.log('发送指令', values, hardwareEquipDetail);

    let msgData = {
      event: 'sys_set_he_num_cmd',
      equip_code: hardwareEquipDetail.he_num,
      message_data: {he_num: values.assign_equip}
    }
    console.log(msgData);
    ws.current?.send(JSON.stringify(msgData));
    dispatch(action.hardware.updateData({isAssignHardwareEquip: false, assignHardwareEquip: []}));
  }

  return (
    <>
      <Modal 
        title="分配设备"
        centered
        forceRender
        visible={isAssignHardwareEquip}
        onCancel={closeOperate}
        footer={null}
        width={600}
      >
        {/* <div style={{ height: '60vh', overflowY: 'auto' }}>
        </div> */}
        <Form
          name="basic"
          form={assignForm}
          // initialValues={hardwareEquipDetail}
          onFinish={sendCommand}
          autoComplete="off"
        >
          <Form.Item
            label="可分配设备"
            name="assign_equip"
            rules={[{ required: true, message: '请选择设备!' }]}
          >
            <Select placeholder="选择设备" >
              {assignHardwareEquip && 
                assignHardwareEquip.map(item => <Select.Option key={item.he_num}>{item.he_num}({item.he_name})</Select.Option>)
              }
            </Select>
          </Form.Item>

          <Form.Item wrapperCol={{ offset: 20, span: 3 }}>
            <Button type="primary" htmlType="submit">分配设备</Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
