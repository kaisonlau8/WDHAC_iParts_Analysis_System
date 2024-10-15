# 该文件是导入iParts系统数据的主程序，负责调用其他脚本并控制整个流程。
import subprocess
import sys

def execute_step(script, prompt_message=""):
    # 执行脚本
    process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # 输出脚本运行结果
    print(stdout.decode())
    if stderr:
        print(stderr.decode())

    # 如果有提示消息，要求用户输入
    if prompt_message:
        user_input = input(prompt_message)
        return user_input.lower() == "y"
    
    # 默认返回 True，以便在没有用户输入时继续执行
    return True

# 步骤一：执行 sqltest.py
if not execute_step("sqltest.py", "是否继续执行步骤二？ (y/n): "):
    print("程序已结束。")
    sys.exit()

# 步骤二：执行 csv2sql.py
if execute_step("csv2sql.py", "请登入数据库，确认导入数据无误后按y键确认，若csv文件上传有误，请输入n以回滚先前的数据。 (y/n): "):
    # 步骤三：执行 finalcheck.py
    execute_step("finalcheck.py")
    print("数据导入成功")
else:
    # 执行 testimportfail.py
    execute_step("testimportfail.py")
    print("程序已结束。")
    sys.exit()

# 明确在完成所有步骤后退出
print("流程全部完成，程序已结束。")
sys.exit()