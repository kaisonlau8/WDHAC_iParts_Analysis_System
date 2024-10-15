# 该文件用于在导入数据前的最终检查，将test表复制为最终使用的details表，并执行旧数据备份，以便于数据回滚。
import pymysql
from datetime import datetime
import re

# 数据库连接信息
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "mysecretpw",
    "database": "iparts"
}

# 创建数据库连接
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

try:
    # 检查是否存在 details 表
    cursor.execute("SHOW TABLES LIKE 'details'")
    result = cursor.fetchone()
    
    if result:
        # 查找并删除旧的 details_[date] 表
        cursor.execute("SHOW TABLES LIKE 'details_%'")
        backup_tables = cursor.fetchall()
        
        if backup_tables:
            # 按照时间从最近到最早排序
            backup_tables_sorted = sorted(backup_tables, key=lambda x: x[0], reverse=True)
            latest_backup = backup_tables_sorted[0][0]
            
            # 仅删除符合格式 'details_YYYY_MM_DD_HH_MM_SS' 的表
            if re.match(r'^details_\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}$', latest_backup):
                cursor.execute(f"DROP TABLE {latest_backup}")
                print(f"已删除旧的备份表: {latest_backup}")
        
        # 备份现有 details 表
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        backup_table_name = f"details_{timestamp}"
        cursor.execute(f"RENAME TABLE details TO {backup_table_name}")
        print(f"已将原有的 details 表重命名为 {backup_table_name}")
    
    # 复制 test 表并重命名为 details
    cursor.execute("CREATE TABLE details LIKE test")
    cursor.execute("INSERT INTO details SELECT * FROM test")
    connection.commit()
    print("表 test 已成功复制为 details")

except pymysql.MySQLError as e:
    print(f"操作失败：{e}")
    connection.rollback()

finally:
    # 关闭数据库连接
    cursor.close()
    connection.close()