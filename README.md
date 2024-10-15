## 环境依赖
- docker
- docker-compose
- python v3.13.0

## 安装指南
1. `docker create network my_network`
2. `docker-compose up -d`

## 使用指南
1. 使用以下命令安装`csv2sql`依赖：
`pip install pandas pymysql numpy`
2. 在iParts系统中导出相关数据，将导出的csv文件放入`details_export_csv`文件夹中，命名为`test.csv`
3. 执行以下命令将test.csv中的数据注入到数据库中：
`python csv2sql.py`
注意：在导入数据时，系统不会校验数据的重复性，因此，请务必确保导入的数据是系统中不存在的。（iParts中的每一条数据不设有唯一的ID，因此本系统无法实现鉴定数据重复功能）

## 数据库管理地址
`http://localhost:8080`

当使用本地phpmyadmin登录时，需要使用以下登录信息：
````
本地mariadb服务器：my_mariadb
用户名：root
密码：mysecretpw
````
## 仓库结构
````
.
├── .DS_Store
├── .gitignore
├── csv2sql.py
├── details_export_csv/
│   └── .DS_Store
├── docker-compose.yml
└── README.md
````