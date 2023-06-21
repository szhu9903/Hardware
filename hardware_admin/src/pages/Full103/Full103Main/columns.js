
import { Tag, Space, Button } from 'antd';

export const columns = (updateFunc) => [
  {
    title: '设备名称',
    dataIndex: 'dl_equip',
    key: 'dl_equip',
    render: dlEquip => dlEquip[0].he_name
  },
  {
    title: '开关',
    dataIndex: 'dl_switch',
    key: 'dl_switch',
    render: dlSwitch => (
      <Tag color={dlSwitch ? 'red' : 'green'}>
        {dlSwitch ? '关' : '开'}
      </Tag>
    )
  },
  {
    title: '红',
    dataIndex: 'dl_r',
    key: 'dl_r',
  },
  {
    title: '绿',
    dataIndex: 'dl_g',
    key: 'dl_g',
  },
  {
    title: '蓝',
    dataIndex: 'dl_b',
    key: 'dl_b',
  },
  {
    title: "操作",
    key: "action",
    render: (text, record) => (
      <Space size="middle">
        <Button size="small" type="primary" onClick={updateFunc(record)} ghost>修改</Button>
      </Space>
    ),
  },
];
