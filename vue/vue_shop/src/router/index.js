import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import UserView from '../views/UserView.vue'
import MenuView from '../views/MenuView.vue'
import AuthorityView from '@/views/AuthorityView.vue'
import GroupView from '@/views/GroupView.vue'
import AttributeView from '@/views/AttributeView.vue'
import ProductView from '@/views/ProductView.vue'
import AddProductView from '@/views/AddProductView.vue'

const routes = [

  {
    path: '/login',
    name: 'login',
    component: LoginView

  },
  {
    path: '/',
    name: 'home',
    redirect: '/welcome',    //自動跳去
    component: HomeView,

    children: [
      {
        path: '/welcome',
        name: 'welcome',
        component: WelcomeView
      },
      {
        path: '/user_list',
        name: 'user_list',
        component: UserView
      },
      {
        path: '/authority_list',
        name: 'authority_list',
        component: MenuView
      },
      {
        path: '/character_list',
        name: 'character_list',
        component: AuthorityView

      },
      {
        path:'/group_list',
        name:'group_list',
        component:GroupView

      },
      {
        path:'/attribute_list',
        name:'attribute_list',
        component:AttributeView
      },
      {
        path:'/product_list',
        name:'product_list',
        component:ProductView
      },
      {
        path:'/add_product',
        name:'add_product',
        component:AddProductView

      }
    ]  
  },

  ]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router


//做router跳轉的login_required驗證   前端
router.beforeEach((to, from, next) => {
  if (to.path == '/login') {
    next()               //next() 代表放行，允許訪問登錄頁
  }
  else {
    //獲取token值
    const token = sessionStorage.getItem('token')
    if (!token) {               //如果沒有token就返回登錄頁面
      next('/login')   //跳轉到login頁面  重定向（改道）
    }
    else {
      next()
    }
  }


})

