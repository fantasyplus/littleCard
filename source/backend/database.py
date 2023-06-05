import mysql.connector
from mysql.connector.cursor import MySQLCursor
import openpyxl
import sys
import os
from os import path
d = path.dirname(__file__)  # 获取当前路径
parent_path = os.path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级

from backend.readSell import readExcel

def insertContentTable(cursor:MySQLCursor,main_id,key_name,value):
    try:
        # 获取当前最大的ID
        cursor.execute("SELECT MAX(id) FROM content_table")
        result = cursor.fetchone()
        id = result[0] if result[0] is not None else 0
        id+=1

        # 插入子表数据
        insert_content_table_sql = "INSERT INTO content_table (id, main_id, key_name, value) VALUES (%s, %s, %s, %s)"
        content_table_data = (id, main_id, key_name, value)
        cursor.execute(insert_content_table_sql, content_table_data)
                        
    except mysql.connector.Error as err:
        print("插入子表数据时发生错误:{} ".format(err))
        print("main_id:{} key_name:{} value:{}".format(main_id,key_name,value))

def insertMainTable(cursor:MySQLCursor,cn,qq):
    id = 0
    try:
        # 获取当前最大的ID
        cursor.execute("SELECT MAX(id) FROM main_table")
        result = cursor.fetchone()
        id = result[0] if result[0] is not None else 0
        id+=1

        # 插入主表数据
        insert_main_table_sql = "INSERT INTO main_table (id, cn, qq) VALUES (%s, %s, %s)"
        main_table_data = (id, cn, qq)
        cursor.execute(insert_main_table_sql, main_table_data)

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            # print("插入数据违反唯一约束 cn:", cn, "qq:", qq)

            # 查询已存在的数据获取 main_id
            select_main_id_sql = "SELECT id FROM main_table WHERE cn = %s AND qq = %s"
            select_main_id_data = (cn, qq)
            cursor.execute(select_main_id_sql, select_main_id_data)
            result = cursor.fetchone()
            if result:
                id = result[0]
                # print("已存在的 id:", id)
            else:
                print("无法获取已存在的id,cn={},qq={} ".format(cn, qq)) 
        else:
            print("发生其他错误:{},cn={},qq={} ".format(err, cn, qq))

    #返回主表id给子表插入数据
    return id

def deleteSubTable(cursor:MySQLCursor,key_name):
    try:
        delete_content_table_sql = "DELETE FROM content_table WHERE key_name = %s"
        delete_content_table_data = (key_name,)
        cursor.execute(delete_content_table_sql, delete_content_table_data)

        # 检查是否有受影响的行数
        if cursor.rowcount == 0:
            print("没有需要删除的{}数据存在".format(key_name))
        else:
            print("成功删除{}数据".format(key_name))

    except mysql.connector.Error as err:
        print("删除{}数据时发生错误:{} ".format(key_name, err))

def writeToDataBase(file_path):
    # 连接到MySQL数据库
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123',
        database='test1'
    )
    # 创建游标对象
    cursor = cnx.cursor()

    p=path.dirname(__file__)+'/../../excel/'+file_path
    data=readExcel(p)

    key_name = None
    for item in data:
        cn=""
        qq=""
        value=0
        if len(item) == 2:
            # 如果长度为2，说明是标题行，获取了key_name就进行下一次循环
            key_name = item[0]

            # 判断子表是否已经有这类谷子，有的话删除，然后再插入（细粒度为某类谷子）
            deleteSubTable(cursor,key_name)

            continue
        elif len(item) == 3:
            # 如果长度为3，说明是正常数据行
            cn = item[0]
            qq = item[1]
            value = item[2]

        # 插入主表数据，返回子表的外键main_id
        main_id=insertMainTable(cursor,cn,qq)

        # 正常插入子表数据
        insertContentTable(cursor,main_id,key_name,value)

    # 提交事务
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()

    return "导入数据库成功！"

if __name__ == "__main__":
    writeToDataBase("sell_info.xlsx")