/* 與後端鏈接2
2所有發送請求的這個方法   	前後端溝通的管道
*/

import axios from "../utils/request.js";           //引入封裝好的axios 
import base from "./base.js"                        //引入接口域名列表




const api ={
    //登錄功能
    login(params){            //用 Axios 發送一個 POST 請求到後端 API   post(url, data)    base.baseURL + base.login： "http://localhost:3000/api" + "/auth/login" = "http://localhost:3000/api/auth/login"
        return axios.post(base.baseURL+base.login,params)
    },

    get_menu(params){
        return axios.get(base.baseURL+base.get_menu, params )
    },
    get_user_list(params){
        return axios.get(base.baseURL+base.get_user_list,params)
    },    
    add_user(params){
        return axios.post(base.baseURL+base.get_user_list,params) 
    },
    get_user_by_id(id){
        return axios.get(base.baseURL+base.get_user_by_id+id+'/')
    },
    edit_user(id,params){   //id 是需要被修改的數據  params是需要改成是什麽數據
        return axios.put(base.baseURL+base.edit_user+id+'/',params)
    },
    delete_user(id){
        return axios.delete(base.baseURL+base.delete_user+id+'/')
    },   
    reset_user_password(id){
        return axios.get(base.baseURL+base.reset_user_password+id+'/')
    },
    get_menu_list(params){
        return axios.get(base.baseURL+base.get_menu_list,params)
    },
    get_roles(params){
        return axios.get(base.baseURL+base.get_roles,params) 
    },
    del_role_menu(rid,mid){
        return axios.get(base.baseURL+base.del_role_menu+rid+'/'+mid+'/')
    },
    set_menu(rid,params){
        return axios.post(base.baseURL+base.set_menu+rid+'/',params)
    },
    get_category(level){
        return axios.get(base.baseURL+base.get_category+'?level='+level)
    },
    add_category(params){
        return axios.post(base.baseURL+base.add_category,params)
    },
    get_attr_by_category(cid,_type){
        return axios.get(base.baseURL+base.get_attr_by_category+'?cid='+cid+'&_type='+_type)
    },
    add_attribute(params){  
        return axios.post(base.baseURL+base.add_attribute,params)
    },
    update_attr_value(id,params){
        return axios.put(base.baseURL+base.update_attr_value+id+'/',params)
    },
    get_product_list(name){
    if(name){
        return axios.get(base.baseURL+base.get_product_list+'?name='+name)
    }else{
        return axios.get(base.baseURL+base.get_product_list)
    }
    },
    delete_product(id){
        return axios.delete(base.baseURL+base.delete_product+id+'/')
    }

    // logout(params){ 
    //     return axios.get(base.baseURL+base.logout)
    // }
}


export default api



