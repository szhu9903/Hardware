import { lazy, Suspense } from 'react'
import { Navigate } from 'react-router-dom'
import LayoutAdmin from '../layouts/layout'

const Login = lazy(() => import('../pages/Login'))
const Home = lazy(() => import('../pages/Home'))

const SysUser = lazy(() => import('../pages/Sys/SysUser'))
const SysRole = lazy(() => import('../pages/Sys/SysRole'))

const HardwareEquip = lazy(() => import('../pages/Hardware/HardwareEquip'))
const HardwareType = lazy(() => import('../pages/Hardware/HardwareType'))
const HardwareConfigVar = lazy(() => import('../pages/Hardware/HardwareConfigVar'))

const DemoLed = lazy(() => import('../pages/Demo/DemoLed'))
const DemoEnv = lazy(() => import('../pages/Demo/DemoEnv'))

const Full103Main = lazy(() => import('../pages/Full103/Full103Main'))

const lazyLoad = (children) => {
  return  (<Suspense fallback={<></>}>
            {children}
          </Suspense>)
}


const router = [
  { path: "/login", element: lazyLoad(<Login />) },
  {
    path: "/",
    element: <LayoutAdmin />,
    children: [
      { index: true, element:  <Navigate to="/home" /> },
      { path: "home", element: lazyLoad(<Home />) },
      
      { path: "sysuser", element: lazyLoad(<SysUser />)},
      { path: "sysrole", element: lazyLoad(<SysRole />)},
      
      { path: "hardwareequip", element: lazyLoad(<HardwareEquip />)},
      { path: "hardwaretype", element: lazyLoad(<HardwareType />)},
      { path: "hardwareconfigvar", element: lazyLoad(<HardwareConfigVar />)},

      { path: "demoled", element: lazyLoad(<DemoLed />)},
      { path: "demoenv", element: lazyLoad(<DemoEnv />)},

      { path: "full103main", element: lazyLoad(<Full103Main />)},

      // { path: "blog/detail/:id", element: lazyLoad(<BlogDetail />) },
    ]
  },
  { path: "*", element: <Navigate to="/login" /> }
]

export default router

