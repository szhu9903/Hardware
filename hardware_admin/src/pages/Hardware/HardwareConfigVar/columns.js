
import { Tag, Space, Button } from 'antd';

export const columns = (updateFunc, deleteFunc) => [
  {
    title: '参数项名称',
    dataIndex: 'hcv_variablekey',
    key: 'hcv_variablekey',
  },
  {
    title: '参数项取值',
    dataIndex: 'hcv_variablevalue',
    key: 'hcv_variablevalue',
  },
  {
    title: '设备类型',
    dataIndex: 'hcv_type',
    key: 'hcv_type',
    render: hcvType => hcvType[0].ht_name
  },
  {
    title: '描述',
    dataIndex: 'hcv_describe',
    key: 'hcv_describe',
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
