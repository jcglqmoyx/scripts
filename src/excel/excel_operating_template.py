import pprint

import openpyxl

filename = 'original.xlsx'  # Excel文件路径
sheet_name = 'Sheet1'  # 要处理的工作表的名称

begin_row = 2
end_row = 106

begin_col = 'B'
end_col = 'D'

work_book = openpyxl.load_workbook(filename)  # 加载Excel文件对象
sheet = work_book[sheet_name]  # 要处理的工作表对象

items = {}
for row in range(begin_row, end_row + 1):
    PIDs = sheet['A' + str(row)].value
    PIDs = str(PIDs).split(';')
    # print(PIDs)
    BNS = sheet['B' + str(row)].value
    total_cost = sheet['C' + str(row)].value
    max_qps = sheet['D' + str(row)].value

    for pid in PIDs:
        items[pid] = {}
        items[pid]['BNS'] = BNS
        items[pid]['total_cost'] = total_cost
        items[pid]['max_qps'] = max_qps

pprint.pprint(items)
print("\n表格读取完毕...\n开始处理并导出新表格...")

result_workbook = openpyxl.Workbook()  # 创建新的Excel workbook对象

result_sheet = result_workbook.active
result_sheet['A1'] = 'PID'
result_sheet['B1'] = 'BNS'
result_sheet['C1'] = '总成本'
result_sheet['D1'] = '实例最大承载QPS'

# 逐行写入数据
row = 2
for pid, values in items.items():
    result_sheet['A' + str(row)] = pid
    result_sheet['B' + str(row)] = values['BNS']
    result_sheet['C' + str(row)] = values['total_cost']
    result_sheet['D' + str(row)] = values['max_qps']
    row += 1

result_workbook.save('result.xlsx')  # 保存
print('\n处理完毕')
