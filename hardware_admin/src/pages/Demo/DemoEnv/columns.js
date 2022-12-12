import { Space, Button } from 'antd';

export const columns = (sendCommand) => [
  {
    title: '设备名称',
    dataIndex: 'de_equip',
    key: 'de_equip',
    render: deEquip => deEquip[0].he_name
  },
  {
    title: '温度',
    dataIndex: 'de_temperature',
    key: 'de_temperature',
  },
  {
    title: '湿度',
    dataIndex: 'de_humidity',
    key: 'de_humidity',
  },
  {
    title: '更新时间',
    dataIndex: 'last_modify_time',
    key: 'last_modify_time',
  },
  {
    title: "操作",
    key: "action",
    render: (text, record) => (
      <Space size="middle">
        <Button size="small" type="primary" onClick={sendCommand(record)} ghost>获取环境数据</Button>
      </Space>
    ),
  },
];


