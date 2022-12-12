
import { Tag, Space, Button } from 'antd';

export const roleColumns = (updateRole, deleteRole) => [
  {
    title: '角色名称',
    dataIndex: 'sr_name',
    key: 'sr_name',
  },
  {
    title: '权限项',
    key: 'r_purview',
    dataIndex: 'r_purview',
    render: tags => (
      <>
      {tags && tags.map((tag) => (
      <Tag color='blue' key={tag.id}>{tag.sp_name}</Tag>
      ))}
      </>
    )
  },
  {
    title: '菜单项',
    key: 'r_menu',
    dataIndex: 'r_menu',
    render: tags => (
      <>
      {tags && tags.map((tag) => (
      <Tag color='blue' key={tag.id}>{tag.sm_name}</Tag>
      ))}
      </>
    )
  },
  {
    title: "操作",
    key: "action",
    render: (text, record) => (
      <Space size="middle">
        <Button size="small" type="primary" onClick={updateRole(record)} ghost>修改</Button>
        <Button size="small" type="primary" onClick={deleteRole(record)} danger ghost>删除</Button>
      </Space>
    ),
  },
];
