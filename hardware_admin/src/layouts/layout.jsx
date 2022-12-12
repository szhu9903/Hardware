import React, { useState, useEffect } from 'react'
import { Layout, Menu, Dropdown, Avatar } from 'antd';
import { Link, Outlet, matchRoutes, useLocation, useNavigate } from 'react-router-dom';
import { getUserInfo } from '../utils/user';
import router from '../router';
import logo from '../assets/images/logo.png'
import './layout.css'
import { useDispatch, useSelector } from 'react-redux';
import actions from '../redux/actions';

const { Header, Content, Footer, Sider } = Layout;
// min-height: calc(100vh - 152px);

export default function LayoutAdmin() {

  const [selectedKeys, setSelectedKeys] = useState([]);
  //数据
  const { sysMenu } = useSelector((state) => state.sys)
  const dispatch = useDispatch();
  // 路由
  const location = useLocation();
  const navigate = useNavigate();
  // 用户
  const userInfo = getUserInfo();

  // 加载菜单数据
  useEffect(() => {
    dispatch(actions.sys.getMenu());
  }, [])

  // 渲染菜单选中项
  useEffect(() => {
    if (userInfo.id === null || userInfo.su_isadmin !== 1){
      navigate('/login');
    }
    const routes = matchRoutes(router, location.pathname)
    if (routes !== null){
      for (let route of routes){
        let path = route.route.path;
        if (path){
          setSelectedKeys([path]);
        }
      }
    }
  }, [location.pathname])

  // 退出登录处理函数
  const clearLocalUser = () => () =>{
    localStorage.clear();
    navigate(0);
  }

  //退出登录
  const downMenu = (
    <Menu>
      <Menu.Item key="0">
        <a onClick={clearLocalUser()}>
          退出登录
        </a>
      </Menu.Item>
    </Menu>
  );

  // 渲染菜单
  const createMenu = (sysMenu) => {
    return sysMenu.map(menu => {
      if (menu.sub && menu.sub.length > 0){
        return <Menu.SubMenu key={menu.id} title={menu.sm_name}>{ createMenu(menu.sub) }</Menu.SubMenu>
      }else {
        return <Menu.Item key={menu.sm_menupath}> <Link to={menu.sm_menupath}>{menu.sm_name}</Link> </Menu.Item>
      }
    })
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider>
        <div className="logo">
          <img src={logo} alt="logo"/>
        </div>
        <Menu theme="dark" selectedKeys={selectedKeys} mode="inline">
          { createMenu(sysMenu) }
        </Menu>
      </Sider>
      <Layout className="site-layout">
        <Header className="site-layout-background">
          <Dropdown overlay={downMenu}  trigger={['click']} placement="bottom"  arrow={{ pointAtCenter: true }} >
            <a>
              <Avatar src={userInfo.su_userphoto} /> {userInfo.su_username}
            </a>
          </Dropdown>
        </Header>
        <Content className="layout-content">
          <Outlet />
        </Content>
        <Footer className='footer' style={{ textAlign: 'center' }}>
          <p>
            © 2019-2022 <a href="">Zsj Blog</a> 版权所有 ICP证： <a href="https://beian.miit.gov.cn" target="_blank">豫ICP备19013573号-1</a>
          </p>
        </Footer>
      </Layout>
    </Layout>
  )
}
