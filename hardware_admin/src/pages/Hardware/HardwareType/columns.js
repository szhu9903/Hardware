
import { Tag, Space, Button } from 'antd';

export const columns = (updateFunc, deleteFunc) => [
  {
    title: '分类名称',
    dataIndex: 'ht_name',
    key: 'ht_name',
  },
  {
    title: '编号最小值',
    dataIndex: 'ht_code_down',
    key: 'ht_code_down',
  },
  {
    title: '编号最大值',
    dataIndex: 'ht_code_up',
    key: 'ht_code_up',
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
