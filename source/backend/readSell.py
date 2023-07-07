import openpyxl
import re
from os import path

# def processString(string):
#     strings=string.split(':')
#     if(len(strings)<2):
#         return "",""

#     string=strings[1]
#     # 初始化 cn 和 qq
#     cn = ""
#     qq = ""

#     # 查找 + 符号的位置
#     plus_index = string.find("+")

#     if plus_index != -1:
#         # 如果存在 + 符号
#         cn = string[:plus_index].strip()
#         qq = string[plus_index+1:].strip()
#     else:
#         # 如果不存在 + 符号
#         # 使用正则表达式进行拆分
#         pattern = r"([^\d]+)(\d+)"
#         matches = re.findall(pattern, string)
#         if len(matches) > 0:
#             # 如果找到匹配项
#             cn = matches[0][0]
#             qq = matches[0][1]

#     return cn, qq
def processString(string):
    pattern = r'cn\+群内qq:(.*)'
    result = re.search(pattern, string)
    cn_qq_str=""
    cn=""
    qq=""

    if result:
        cn_qq_str = result.group(1)
    else:#如果没有cn+群内qq:，则直接返回，第一行标题的特殊处理
        return cn,qq
        
    pattern = r'(.*?)\s*(?=\d{8,})'
    result = re.findall(pattern, cn_qq_str)

    cn = result[0]
    # 去除末尾的 + 号
    if cn[-1] == '+':
        cn = cn[:-1]

    qq = re.search(r'\d{8,}', cn_qq_str).group()

    return cn,qq

def readSellInfo(file_path):
    p=path.dirname(__file__)+'/../../excel/'+file_path
    # 读取Excel文件
    wb = openpyxl.load_workbook(p)
    sheet_names=['月影幽光','少女心事','樱的风语']
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
                    cn,qq=processString(row[i].value)
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
    file_name='sell_info.xlsx'

    data=readSellInfo(file_name)
    for i in range(len(data)):
        print(data[i])