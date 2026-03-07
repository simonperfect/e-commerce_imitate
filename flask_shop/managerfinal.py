from IIIflask_shop import create_app,db
from flask_migrate import Migrate
from flask_cors import CORS     # pip install flask_cors==3.0.10



app = create_app('develop')   #開發模式    本來是這樣app = Flask(__name__)
CORS(app,supports_credentials=True)      #解決跨越問題   跟js交互   js在前端 terminal cd vue/vue_shop  code .  打開 

#創建同步數據對象
Migrate(app,db)


'''
set FLASK_APP=managerfinal.py
flask db migrate   
flask db upgrade 更新數據庫 


git bash:
if the data is munual do the wrong action it will affect the version of the database which the file is alembic_version in the table of database 
we want to fix it

Step 1: Clear version records
    1.1 go to the mysql 
        1.1.1 how to find the mysql in your computer?
        find /c -name "mysql.exe" 2>/dev/null    
            1.1.1.1 File Descriptors have three option 0->standoard input  1->standard output 2->standard error
            we will use 2> because there are a lot of Permission denied when we find mysql
            so when we use two we can skip all the Permission denied and return the final result without Permission denied
            after that I found my mysql in "/c/Program Files/MySQL/MySQL Server 5.7/bin/mysql.exe"
        #access to sql
            "/c/Program Files/MySQL/MySQL Server 5.7/bin/mysql.exe" -u root -p
            then input the password

mysql -u root -p -e "TRUNCATE TABLE alembic_version;" flask_shop    #which -u root is the username:root  -p is password is required -e is execute

Step 2: Set to latest state:
mysql -u root -p -e "INSERT INTO alembic_version (version_num) VALUES ('head');" flask_shop

Step 3: Create tables (if they don't exist)
python -c "from managerfinal import create_app, db; app = create_app('develop'); with app.app_context(): db.create_all()"
    -c is used to tell python the following sentence "" is code 
    with app.app_context(): db.create_all()  is to create all the table

'''

if __name__ == '__main__':
    import os
   #Get the port from the environment variable. Render will automatically set this variable. If not found, 5000 will be used as the local fallback.
    port = int(os.environ.get('PORT', 5000))
    # Start the application and listen on all network interfaces ('0.0.0.0') so that the Render's proxy can forward external requests.
    app.run(host='0.0.0.0', port=port, debug=False) # When deploying to a production environment, it is recommended to set debug to False.