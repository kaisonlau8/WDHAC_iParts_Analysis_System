# WDHAC iParts数据分析系统
## 1 系统详情
本系统作用是分析iParts系统导出的相关数据，共有以下组件：
1. iParts数据导入组件 —— dataImport (开发进度60%)
2. 数据库管理组件 —— phpMyAdmin (已导入)
3. 数据分析组件 —— dataAnalysis (待开发)

## 2 项目开发进度
|日期|所属组件|子项目|状态|备注|
|----|----|----|----|----|
|2024-10-15|dataImport|导入脚本|新增iparts CSV文件导入功能|开发完成|
|2024-10-15|dataImport|导入脚本|新增dataImport一键导入脚本|开发完成|
|2024-10-15|dataImport|导入脚本|在README.md文件中加入main.py程序的执行框图|待更新|

## 3 环境依赖
使用前，请确保安装有以下依赖：
```
- docker
- docker-compose
- python v3.13.0
```

## 4 安装指南
```
git clone https://github.com/kaisonlau8/WDHAC_iParts_Analysis_System.git
```
```
docker create network my_network
```
```
docker-compose up -d
```

## 5 使用指南
### 5.1 dataImport组件
1. 使用以下命令安装依赖：
`pip install pandas pymysql numpy`
2. 在iParts系统中导出相关数据，将导出的csv文件放入`details_export_csv`文件夹中，命名为`test.csv`
3. 终端进入dataImport文件夹，执行以下命令将test.csv中的数据注入到数据库中（本仓库已经在`details_export_csv`文件夹提供了测试数据）：
`python main.py`
注意：在导入数据时，系统不会校验数据的重复性，因此，请务必确保导入的数据是系统中不存在的。（iParts中的每一条数据不设有唯一的ID，因此本系统无法实现鉴定数据重复功能）
4. 导入数据时，执行`main.py`主文件会生成提示步骤，请按照提示步骤操作即
5.  步骤1提示数据库连接状态，若连接失败，请检查数据库连接信息是否正确，数据库配置信息储存在`./dataimport/config.json`文件中
6.  步骤2执行完毕后，请使用数据库管理软件查看导入数据的状态及所导入的数据是否正确，若导入的数据错误，请在终端输入`n`，以退出导入程序，数据会自动回滚，回滚后刷新数据库即可，请勿进入步骤3，步骤2会将导入的数据写入`test`数据表中。
7. 进入步骤3后，程序导入完成，若需要回滚本数据，请登入数据库管理软件，删除`test`数据表，复制系统最后一次备份的`details[date]`数据表2份，其中1份将重命名为`test`数据表，另一份重命名为`details`数据表，然后刷新数据库即可。

## 6 数据库信息

### 6.1 SQL Info
```
Host: my_mariadb / 127.0.0.1
Port: 3306
Database: iparts (执行main.py脚本时，若无此数据库，会自动创建)
Username: root
Password: mysecretpw
table: details (真实数据表，该数据库仅可通过数据库管理工具回滚1次) & test (暂存数据表，支持导入主程序回滚)
[数据表回滚步骤见5.1]
```
### 6.2 数据库管理地址 -- phpMyAdmin
1. 数据库管理由docker-compose启动，可通过以下地址访问：
`http://localhost:8080`
2. 本系统在开发时，开发者使用的是TablePlus软件，也可以使用该软件进行数据库管理

**注意：** phpMyAdmin在开发者测试环境 `MacOS 15.0.1的docker环境下` 使用时，会出现数据表数据行数显示不准确的情况，TablePlus则无此情况

当使用本地phpmyadmin登录时，需要使用以下登录信息：
````
本地mariadb服务器：my_mariadb
用户名：root
密码：mysecretpw
````