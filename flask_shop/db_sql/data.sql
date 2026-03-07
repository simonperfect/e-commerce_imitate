insert into t_menus(id,name,level,path) values(-1,'All',0,NUll);

#一級層
insert into t_menus(id,name,level,pid) values(1,'Guests management',1,-1);
insert into t_menus(id,name,level,pid) values(2,'Autority',1,-1);
insert into t_menus(id,name,level,pid) values(3,'Merchandise management',1,-1);
insert into t_menus(id,name,level,pid) values(4,'Order management',1,-1);
insert into t_menus(id,name,level,pid) values(5,'Statistic',1,-1);
;




#二級層
insert into t_menus(id,name,level,path,pid) values(11,'Guests list',2,'/user_list',1);
insert into t_menus(id,name,level,path,pid) values(21,'Character list',2,'/character_list',2);
insert into t_menus(id,name,level,path,pid) values(22,'Authority list',2,'/authority_list',2);
insert into t_menus(id,name,level,path,pid) values(31,'Merchandise list',2,'/productr_list',3);
insert into t_menus(id,name,level,path,pid) values(32,'catagory list',2,'/group_list',3);