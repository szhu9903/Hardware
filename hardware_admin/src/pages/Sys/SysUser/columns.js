
import { Tag, Space, Button } from 'antd';

export const userColumns = (updateUser, deleteUser) => [
  {
    title: '账号',
    dataIndex: 'su_account',
    key: 'su_account',
  },
  {
    title: '性别',
    dataIndex: 'su_sex',
    key: 'su_sex',
  },
  {
    title: '用户名',
    dataIndex: 'su_username',
    key: 'su_username',
  },
  {
    title: '头像地址',
    dataIndex: 'su_userphoto',
    key: 'su_userphoto',
  },
  {
    title: '电话',
    dataIndex: 'su_phone',
    key: 'su_phone',
  },
  {
    title: '邮箱',
    dataIndex: 'su_email',
    key: 'su_email',
  },
  {
    title: '允许后台',
    dataIndex: 'su_isadmin',
    key: 'su_isadmin',
    render: buisadmin => (
      <Tag color={buisadmin ? 'green' : 'red'}>
        {buisadmin ? '允许' : '禁止'}
      </Tag>
    )
  },
  {
    title: '注册时间',
    dataIndex: 'su_createdate',
    key: 'su_createdate',
  },
  {
    title: '有效状态',
    key: 'su_delflag',
    dataIndex: 'su_delflag',
    render: bDelflag => (
      <Tag color={bDelflag ? 'geekblue' : 'green'}>
        {bDelflag ? '无效' : '有效'}
      </Tag>
    )
  },
  {
    title: "操作",
    key: "action",
    render: (text, record) => (
      <Space size="middle">
        <Button size="small" type="primary" onClick={updateUser(record)} ghost>修改</Button>
        <Button size="small" type="primary" onClick={deleteUser(record)} danger ghost>删除</Button>
      </Space>
    ),
  },
];
