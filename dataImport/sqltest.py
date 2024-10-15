# 该文件用于测试数据库连接是否正常
import mysql.connector
import json
from mysql.connector import Error

# 读取 config.json 文件
config_file_path = 'config.json'

try:
    # 加载数据库连接信息
    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)
        db_config = config_data['db_config']
    
    # 尝试连接到数据库
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("成功连接到数据库！")
        
        # 获取数据库版本信息
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        print("数据库版本:", version[0])

except FileNotFoundError:
    print("配置文件未找到，请检查路径是否正确。")
except json.JSONDecodeError:
    print("配置文件格式不正确，请检查文件内容。")
except Error as e:
    print("数据库连接失败:", e)
finally:
    # 关闭数据库连接
    if 'connection' in locals() and connection.is_connected():
        connection.close()