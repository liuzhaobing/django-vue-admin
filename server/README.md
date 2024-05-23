### django后端

定位到server文件夹

安装依赖包 `pip install -r requirements.txt`

复制server文件夹下的conf_e.py为conf.py
根据需要修改里面的数据库连接及DEBUG参数

同步数据库

```shell
python manage.py makemigrations
python manage.py migrate
```

可导入初始数据

```shell
python manage.py loaddata db.json
``` 

或直接使用sqlite数据库(超管账户密码均为admin,每隔一段时间数据库会重置)

创建超级管理员

```shell
python manage.py createsuperuser
```

运行服务

```shell
python manage.py runserver 8000
``` 
