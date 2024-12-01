import json
import mysql.connector
from datetime import datetime, timedelta
import csv
import os

# 从 config.json 文件读取数据库配置
def load_db_config():
    with open('./dataImport/config.json', 'r') as file:
        config = json.load(file)
    return config['db_config']

# 获取用户输入的日期，并转换为指定格式
def get_date_input(prompt):
    while True:
        try:
            date_input = input(prompt)
            date_obj = datetime.strptime(date_input, '%Y/%m/%d')
            return date_obj
        except ValueError:
            print("\u65e5\u671f\u683c\u5f0f\u65e0\u6548\uff0c\u8bf7\u4f7f\u7528yyyy/mm/dd\u683c\u5f0f\u91cd\u65b0\u8f93\u5165\u3002")

# 执行查询并获取结果
def fetch_data_by_date(date):
    db_config = load_db_config()
    connection = None
    
    try:
        # 连接到指定数据库（iparts）
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database='iparts',
            charset=db_config.get('charset', 'utf8mb4')
        )

        # 创建源标定的文件字典的运行
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                s.\u533a\u57df AS region,
                SUM(d.\u603b\u5355\u4ef7) AS total_price
            FROM iparts.details d
            JOIN iparts.store s ON d.\u7279\u7ea6\u5e97\u4ee3\u7801 = s.\u5e97\u4ee3\u7801
            WHERE DATE(d.\u51fa\u5e93\u65e5\u671f) = %s
            GROUP BY s.\u533a\u57df;
        """
        # 执行查询
        cursor.execute(query, (date,))

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
    filename = f"export/{start_date_str}_{end_date_str}\u6bcf\u65e5\u603b\u4ef7\u6c47\u603b.csv"
    
    # 写入 CSV 文件
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['date', 'region', 'total_price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\u7ed3\u679c\u5df2\u6210\u529f\u5bfc\u51fa\u5230 {filename}")

# 主函数
def main():
    # 提示用户输入日期
    start_date_obj = get_date_input("\u8bf7\u8f93\u5165\u51fa\u5e93\u65e5\u671f\u7684\u5f00\u59cb\u65f6\u95f4 (\u683c\u5f0f: yyyy/mm/dd): ")
    end_date_obj = get_date_input("\u8bf7\u8f93\u5165\u51fa\u5e93\u65e5\u671f\u7684\u622a\u6b62\u65f6\u95f4 (\u683c\u5f0f: yyyy/mm/dd): ")
    
    # 格式化为\u6587件名用的日期字符串
    start_date_str = start_date_obj.strftime('%Y-%m-%d')
    end_date_str = end_date_obj.strftime('%Y-%m-%d')

    # 转换日期范围
    current_date = start_date_obj
    delta = timedelta(days=1)
    all_results = []

    # 对范围内每天进行查询
    while current_date <= end_date_obj:
        date_str = current_date.strftime('%Y-%m-%d')
        daily_results = fetch_data_by_date(date_str)
        
        # 处理查询结果
        for result in daily_results:
            all_results.append({
                'date': date_str,
                'region': result['region'],
                'total_price': result['total_price']
            })

        current_date += delta

    # 导出结果到CSV
    if all_results:
        export_to_csv(all_results, start_date_str, end_date_str)
    else:
        print("\u672a\u627e\u5230\u7b26\u5408\u6761\u4ef6\u7684\u8bb0\u5f55\u3002")

# 执行主函数
if __name__ == "__main__":
    main()
