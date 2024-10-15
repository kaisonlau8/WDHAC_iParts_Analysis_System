# 该文件用于将 CSV 文件中的数据导入到 MySQL 数据库中，导出的结果是一个新的数据库 'iparts' 和一个新的表 'test'
import pandas as pd
import pymysql
import numpy as np
import json
import time

config_file_path = 'config.json'

try:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
        db_config = config['db_config']
        csv_file_path = config['csv_file_path']
except FileNotFoundError:
    print(f"配置文件 '{config_file_path}' 未找到。")
    exit(1)
except json.JSONDecodeError:
    print(f"配置文件 '{config_file_path}' 格式错误。")
    exit(1)

try:
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES LIKE 'iparts'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("CREATE DATABASE iparts CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
            print("数据库 'iparts' 创建成功")
        else:
            print("数据库 'iparts' 已存在")
finally:
    connection.close()

db_config['database'] = 'iparts'
start_time = time.time()

try:
    connection = pymysql.connect(**db_config)
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-16', delimiter='\t')
        df = df.replace({np.nan: None})

        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS test (
                发货仓库 VARCHAR(255),
                零部件号 VARCHAR(255),
                一级分类 VARCHAR(255),
                二级分类 VARCHAR(255),
                三级分类 VARCHAR(255),
                四级分类 VARCHAR(255),
                销售地区 VARCHAR(255),
                中文名 VARCHAR(255),
                英文名 VARCHAR(255),
                出库数量 INT,
                总成本 DECIMAL(10, 2),
                货运单号 VARCHAR(255),
                特约店代码 VARCHAR(255),
                销售订单号 VARCHAR(255),
                出库日期 DATETIME,
                总单价 DECIMAL(10, 2),
                2_4_pp VARCHAR(255),
                订单类型 VARCHAR(255),
                行号 INT,
                VIN VARCHAR(255),
                特约店到货时间 DATETIME,
                特约店签收时间 DATETIME,
                特约店签收数量 INT,
                签收方式 VARCHAR(255)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
            """)

            data = df.values.tolist()
            sql = """
            INSERT INTO test (发货仓库, 零部件号, 一级分类, 二级分类, 三级分类, 四级分类, 销售地区,
            中文名, 英文名, 出库数量, 总成本, 货运单号, 特约店代码, 销售订单号, 出库日期, 总单价, 2_4_pp,
            订单类型, 行号, VIN, 特约店到货时间, 特约店签收时间, 特约店签收数量, 签收方式)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, data)
            connection.commit()

            print(f"成功插入了 {cursor.rowcount} 条数据。")
    except FileNotFoundError:
        print(f"CSV 文件 '{csv_file_path}' 未找到。")
    except pd.errors.ParserError:
        print(f"CSV 文件 '{csv_file_path}' 解析错误。")
finally:
    connection.close()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"程序运行用时：{elapsed_time:.2f} 秒")