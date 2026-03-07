/* 前端_构建请求工具与结构  
你的代碼
    ↓
請求攔截器 ← 添加 token、loading、修改請求
    ↓
發送到伺服器
    ↓
伺服器處理
    ↓
響應攔截器 ← 統一錯誤處理、數據格式化
    ↓
你的 .then() 或 .catch()

*/

import axios from "axios"
import router from '@/router/index.js'       //vue 外部的引用方法


const errorHandle = (status,info) =>{    //處理錯誤
  switch(status){
    case 400:
      console.log("语义错误");
      break;
    case 401:
      console.log("服务器认证失败");
      break;
    case 403:
      console.log("服务器请求拒绝执行");
      break;
    case 404:
      console.log("请检查网路请求地址");
      break;
    case 500:
      console.log("服务器发生意外");
      break;
    case 502:
      console.log("服务器无响应");
      break;
    default:
      console.log(info);
      break;
   }
}
/**
 * 创建Axios对象
 */
const instance = axios.create({
  timeout:5000,
})



 
instance.interceptors.request.use(     //處理請求   安檢人員  檢查你帶的東西是否合規
  config =>{
    //獲取token       後端
    let token = sessionStorage.getItem('token')
    //獲取到的token放到請求頭裏面
    /*
    原本請求頭是這樣的：   請求的時候複雜每次都要説出所有參數  例如名字 密碼重新登陸  return axios({method: 'GET',url: `/api/user/${userId}/orders`, headers: { 'Content-Type': 'application/json',
    {
        GET /api/user/1001/orders HTTP/1.1
        Host: api.supermarket.com
        Accept: application/json
        Content-Type: application/json
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
        Accept-Language: zh-TW
        Connection: keep-alive
        }

      加入token后變成這樣：    請求的時候簡單  只需要token在就行了   const getOrders = () =>  return request.get('/api/orders')  
      {
        GET /api/orders HTTP/1.1
        Host: api.supermarket.com
        Accept: application/json
        Content-Type: application/json
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEwMDEsIm5hbWUiOiJcdTU3MmNcdTRlMDkiLCJwaG9uZSI6IjA5MTIzNDU2NzgiLCJpYXQiOjE3MDQxMjM0NTYsImV4cCI6MTcwNDEyNzA1Nn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
        Accept-Language: zh-TW
        Connection: keep-alive
        X-Client-Version: 2.1.0
      }
    
    */
    if(token){ 
        config.headers.token = token   //   網絡裏的headers就是信封表面的信息   後端
    }

    return config
   },
  error => Promise.reject(error)      
)



 
instance.interceptors.response.use(     //處理響應  響應攔截器：在收到伺服器響應之後，傳遞給調用者之前執行
  response=>{
    if(response.status == 200){           //檢查 HTTP 狀態碼是否為 200
      if(response.data.status == 401){     //後端的token文件的 login_required  unvalidate token就會返回401的狀態   檢查響應數據中的業務狀態碼是否為 401
        //delete unvalidate token
        sessionStorage.removeItem("token")
        //token失效
        router.push('/login');
        return Promise.reject(response);
      }
      else if (response.data.status === 200){
        return Promise.resolve(response);
      }
      else {
      // 其他業務錯誤 (500, 404, 403, 400 等)     可以省略 因爲我們沒有設置這些狀態
      return Promise.reject(response);
      }
    }
    else{
      return Promise.reject(response);
    }
  },
  error =>{
    const { response } = error;
    if(response){
      errorHandle(response.status,response.info)
     }else{ 
      console.log("网络请求被中断了");
     }
   }
)
export default instance


