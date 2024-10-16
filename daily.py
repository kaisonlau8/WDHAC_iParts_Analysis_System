import json
import mysql.connector
from datetime import datetime
import csv
import os

# 从 config.json 文件读取数据库配置
def load_db_config():
    with open('./dataImport/config.json', 'r') as file:
        config = json.load(file)
    return config['db_config']  # 获取嵌套的 db_config 部分

# 获取用户输入的日期，并转换为指定格式
def get_date_input(prompt):
    while True:
        try:
            date_input = input(prompt)
            date_obj = datetime.strptime(date_input, '%Y/%m/%d')
            return date_obj
        except ValueError:
            print("日期格式无效，请使用yyyy/mm/dd格式重新输入。")

# 执行查询并获取结果
def fetch_data(start_date, end_date):
    db_config = load_db_config()
    connection = None
    
    try:
        # 连接到指定数据库（iparts）
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database='iparts',  # 直接指定数据库名称
            charset=db_config.get('charset', 'utf8mb4')
        )

        # 创建游标并执行查询
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                d.特约店代码 AS store_code,
                SUM(d.总单价) AS total_price,
                s.店名 AS store_name,
                s.督导 AS supervisor,
                s.区域 AS region
            FROM iparts.details d
            JOIN iparts.store s ON d.特约店代码 = s.店代码
            WHERE d.出库日期 BETWEEN %s AND %s
            GROUP BY d.特约店代码, s.店名, s.督导, s.区域;
        """
        # 执行查询，使用用户输入的日期
        cursor.execute(query, (start_date, end_date))

        # 获取查询结果
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection:
            connection.close()

# 导出结果到CSV文件
def export_to_csv(data, start_date_str, end_date_str):
    # 确保 export 文件夹存在
    os.makedirs("export", exist_ok=True)
    
    # 定义 CSV 文件路径和名称
    filename = f"export/{start_date_str}_{end_date_str}产值汇总.csv"
    
    # 写入 CSV 文件
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['store_code', 'total_price', 'store_name', 'supervisor', 'region'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"结果已成功导出到 {filename}")

# 主函数
def main():
    # 提示用户输入日期并转换为字符串
    start_date_obj = get_date_input("请输入出库日期的开始时间 (格式: yyyy/mm/dd): ")
    end_date_obj = get_date_input("请输入出库日期的截止时间 (格式: yyyy/mm/dd): ")
    
    # 格式化为完整的时间字符串
    start_date = start_date_obj.strftime('%Y/%m/%d 00:00:00')
    end_date = end_date_obj.strftime('%Y/%m/%d 23:59:59')
    
    # 格式化为文件名使用的日期字符串
    start_date_str = start_date_obj.strftime('%Y-%m-%d')
    end_date_str = end_date_obj.strftime('%Y-%m-%d')

    # 执行查询并获取结果
    results = fetch_data(start_date, end_date)
    
    # 导出结果到CSV文件
    if results:
        export_to_csv(results, start_date_str, end_date_str)
    else:
        print("未找到符合条件的记录。")

# 执行主函数
if __name__ == "__main__":
    main()