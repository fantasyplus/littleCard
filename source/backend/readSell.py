import openpyxl
import re
from os import path

def process_string(string):
    strings=string.split(':')
    if(len(strings)<2):
        return "",""

    string=strings[1]
    # 初始化 cn 和 qq
    cn = ""
    qq = ""

    # 查找 + 符号的位置
    plus_index = string.find("+")

    if plus_index != -1:
        # 如果存在 + 符号
        cn = string[:plus_index].strip()
        qq = string[plus_index+1:].strip()
    else:
        # 如果不存在 + 符号
        # 使用正则表达式进行拆分
        pattern = r"([^\d]+)(\d+)"
        matches = re.findall(pattern, string)
        if len(matches) > 0:
            # 如果找到匹配项
            cn = matches[0][0]
            qq = matches[0][1]

    return cn, qq

def readExcel(file_path):
    print("读取Excel文件:", file_path)
    # 读取Excel文件
    wb = openpyxl.load_workbook(file_path)
    sheet_names=['月影幽光','少女心事','樱的风语']
    # sheet_names=['樱的风语']
    data=[]

    for sheet_name in sheet_names:
        sheet = wb[sheet_name]  # 修改为实际的工作表名
        cn=""
        qq=""
        num=0
        # 读取整个工作表的数据
        for row in sheet.iter_rows():
            row_data=[]
            for i in range(len(row)):
                if(i==0):
                    cn=process_string(row[i].value)[0]
                    qq=process_string(row[i].value)[1]
                    if(cn=="" and qq==""):
                        row_data.append(row[i].value)
                    else:
                        row_data.extend([cn,qq])
                if(i==1):
                    num=row[i].value
                    row_data.append(num)
            data.append(row_data)

    # 关闭Excel文件
    wb.close()
    return data

if __name__ == "__main__":
    file_path='sell_info.xlsx'
    p=path.dirname(__file__)+'/../../excel/'+file_path

    data=readExcel(p)
    for i in range(len(data)):
        print(data[i])