import mysql.connector
from mysql.connector.cursor import MySQLCursor
import re
import openpyxl
import sys
import os
from os import path
d = path.dirname(__file__)  # 获取当前路径
parent_path = os.path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级

from backend.readSell import readSellInfo
from backend.readCard import readCardInfo

def insertPersonInfoTable(cursor:MySQLCursor,data):
    person_id2card_ids = {}
    person_id2cn_qq= {}
    person_id = None
    card_name = None
    card_id = None
    card_num = None
    cn=""
    qq=""
    for item in data:
        if len(item) == 2:
            # 如果长度为2，说明是标题行，获取了card_name和card_id就进行下一次循环
            match=re.search(r'\d+', item[0])
            card_id=match.group()
            card_name = item[0][match.end():]

            continue
        elif len(item) == 3:
            # 如果长度为3，说明是正常数据行
            cn = item[0]
            qq = item[1]
            card_num = item[2]
        
        # 插入personInfo表
        try:
            # 获取当前最大的ID
            cursor.execute("SELECT MAX(person_id) FROM personInfo")
            result = cursor.fetchone()
            person_id = result[0] if result[0] is not None else 0
            person_id+=1         

            # 插入主表数据
            insert_person_info_sql = "INSERT INTO personInfo (person_id, cn, qq) VALUES (%s, %s, %s)"
            person_info_data = (person_id, cn, qq)
            cursor.execute(insert_person_info_sql, person_info_data)

        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                # print("插入数据违反唯一约束 cn:", cn, "qq:", qq)

                # 查询已存在的数据获取 person_id
                select_person_id_sql = "SELECT person_id FROM personInfo WHERE cn = %s AND qq = %s"
                select_person_id_data = (cn, qq)
                cursor.execute(select_person_id_sql, select_person_id_data)
                result = cursor.fetchone()
                if result:
                    person_id = result[0]
                    # print("已存在的 person_id:", person_id)
                else:
                    print("insertPersonInfoTable无法获取已存在的id,cn={},qq={} ".format(cn, qq)) 
            else:
                print("insertPersonInfoTable发生其他错误:{},cn={},qq={} ".format(err, cn, qq))

        # 插入对应person_id的的card_id，为插入cardindex表做准备
        if person_id not in person_id2card_ids:
            person_id2card_ids[person_id] = [card_id]
        elif card_id not in person_id2card_ids[person_id]:
            person_id2card_ids[person_id].append(card_id)
        
        if person_id not in person_id2cn_qq:
            person_id2cn_qq[person_id] = [cn, qq]
        elif cn not in person_id2cn_qq[person_id]:
            person_id2cn_qq[person_id].append(cn)
            person_id2cn_qq[person_id].append(qq)

    return person_id2card_ids, person_id2cn_qq


def insertIntoCardIndex(cursor: MySQLCursor, data):
    # 插入数据或更新数据
    for person_id, card_ids in data.items():
        try:
            select_sql = "SELECT * FROM cardIndex WHERE person_id = %s"
            cursor.execute(select_sql, (person_id,))
            result = cursor.fetchone()

            if result is None:
                insert_sql = "INSERT INTO cardIndex (person_id, card_ids) VALUES (%s, %s)"
                card_id_str = ','.join(card_ids)
                insert_data = (person_id, card_id_str)
                cursor.execute(insert_sql, insert_data)
            else:
                update_sql = "UPDATE cardIndex SET card_ids = %s WHERE person_id = %s"
                card_id_str = ','.join(card_ids)
                update_data = (card_id_str, person_id)
                cursor.execute(update_sql, update_data)

        except mysql.connector.Error as err:
            print("insertIntoCardIndex发生错误: {}".format(err))

def insertCardInfo(cursor: MySQLCursor, data):
    # 从第三行开始插入或更新数据
    for row in data[2:]:
        try:
            card_id, card_name, card_character, card_type, card_condition, other = row[:6]

            # 检查是否存在相同的card_id
            query = "SELECT * FROM cardInfo WHERE card_id = %s"
            cursor.execute(query, (card_id,))
            result = cursor.fetchone()

            if result:
                # 如果存在相同的card_id，执行更新操作
                query = "UPDATE cardInfo SET card_name = %s, card_character = %s, card_type = %s, card_condition = %s, other = %s WHERE card_id = %s"
                cursor.execute(query, (card_name, card_character, card_type, card_condition, other, card_id))
            else:
                # 如果不存在相同的card_id，执行插入操作
                query = "INSERT INTO cardInfo (card_id, card_name, card_character, card_type, card_condition, other) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (card_id, card_name, card_character, card_type, card_condition, other))
        except mysql.connector.Error as err:
            print("insertCardInfo发生错误: {}".format(err))

# def insertCardNo(cursor: MySQLCursor, data: dict):
#     for person_id, card_ids in data.items():
        

def writeToDataBase():
    # 连接到MySQL数据库
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123',
        database='test1'
    )
    # 创建游标对象
    cursor = cnx.cursor()

    data_sell_info=readSellInfo("sell_info.xlsx")
    data_card_info=readCardInfo("card_info.xlsx")

    # 插入personInfo表
    person_id2card_ids, person_id2cn_qq = insertPersonInfoTable(cursor, data_sell_info)

    # 插入cardIndex表
    insertIntoCardIndex(cursor,person_id2card_ids)

    # 插入cardInfo表
    insertCardInfo(cursor,data_card_info)

    # 按照person_id2card_ids依次创建并插入cardNo表
    # insertCardNo(cursor,person_id2card_ids)
    for item in person_id2cn_qq.items():
        print(item)
    for item in person_id2card_ids.items():
        print(item)
    # 提交事务
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()

    return "导入数据库成功！"

if __name__ == "__main__":
    writeToDataBase()