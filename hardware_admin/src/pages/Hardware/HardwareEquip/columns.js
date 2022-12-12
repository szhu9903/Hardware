
import { Tag, Space, Button } from 'antd';

export const columns = (updateFunc, deleteFunc) => [
  {
    title: '设备名称',
    dataIndex: 'he_name',
    key: 'he_name',
  },
  {
    title: '设备编号',
    dataIndex: 'he_num',
    key: 'he_num',
  },
  {
    title: '设备分类',
    dataIndex: 'he_type',
    key: 'he_type',
    render: heType => heType[0].ht_name
  },
  {
    title: '设备状态',
    dataIndex: 'he_equipstatus',
    key: 'he_equipstatus',
    render: heEquipStatus => (
      <Tag color={heEquipStatus == 'LINKED' ? 'green' : 'geekblue'}>
        {heEquipStatus == 'LINKED' ? '在线' : '离线'}
      </Tag>
    )
  },
  {
    title: '启用状态',
    dataIndex: 'he_starttype',
    key: 'he_starttype',
    render: heStartType => (
      <Tag color={heStartType == 'START' ? 'green' : 'geekblue'}>
        {heStartType == 'START' ? '启用' : '停用'}
      </Tag>
    )
  },
  {
    title: "操作",
    key: "action",
    render: (text, record) => (
      <Space size="middle">
        <Button size="small" type="primary" onClick={updateFunc(record)} ghost>修改</Button>
        <Button size="small" type="primary" onClick={deleteFunc(record)} danger ghost>删除</Button>
      </Space>
    ),
  },
];
