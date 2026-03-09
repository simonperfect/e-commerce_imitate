/* 與後端鏈接1
1 存放所有API接口地址   */

const base = {
        baseURL: process.env.NODE_ENV === 'development' 
        ? 'http://localhost:5000'                    // 本地開發
        : 'https://e-commerce-imitate.onrender.com',      // 線上部署
    login:'/user/login/',                    //login address
    get_menu:'/menu/menus/?type_=tree',                     //get the menu
    get_menu_list:'/menu/menus/',
    get_user_list: '/user/register/',          //get the user list
    get_user_by_id:'/user/user/',
    edit_user:'/user/user/',     //edit the individual data
    delete_user:'/user/user/',
    reset_user_password:'/user/reset_pwd/',    //reset 
    get_roles:'/roles/',     //role list、
    del_role_menu:'/role/',     //delete role menu
    set_menu:'/role/',      //reset the menu  used for assign authority in AuthorityView
    get_category:'/categorys/',   
    add_category:'/categorys/',
    get_attr_by_category:'/attributes/',   //get attribute by category id 
    add_attribute:'/attributes/',
    update_attr_value:'/attribute/', 
    get_product_list:'/products/',
    delete_product:'/product/',


    
}

export default base