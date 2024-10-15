# 该文件用于删除错误导入的test表，以回滚错误的操作
import json
import mysql.connector
from mysql.connector import Error

# 读取配置文件
def load_config():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            return config["db_config"]
    except FileNotFoundError:
        print("配置文件config.json未找到")
        return None
    except json.JSONDecodeError:
        print("配置文件格式错误")
        return None

# 删除并复制表的函数
def manage_table(config):
    try:
        # 连接数据库
        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database="iparts",
            charset=config.get("charset", "utf8mb4")
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # 删除test表
            cursor.execute("DROP TABLE IF EXISTS test")
            print("已删除 test 表")
            
            # 复制details表为test表
            cursor.execute("CREATE TABLE test LIKE details")
            cursor.execute("INSERT INTO test SELECT * FROM details")
            print("已复制 details 表为 test 表")
            
            # 提交更改
            connection.commit()
    
    except Error as e:
        print(f"数据库操作错误: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")

# 主程序
if __name__ == "__main__":
    config = load_config()
    if config:
        manage_table(config)