import xlsxwriter
from application.testdb.DB import DB

db = DB()
tests = db.getTestResults()

workbook = xlsxwriter.Workbook('example.xlsx')
worksheet = workbook.add_worksheet()

cellPass = workbook.add_format({'font_color': 'green'})
cellFail = workbook.add_format({'bold': True, 'font_color': 'red'})

worksheet.write('A1', '№')
worksheet.write('B1', 'Название теста')
worksheet.write('C1', 'Успех')
worksheet.write('D1', 'Фиаско')
worksheet.write('E1', 'Дата проведения')

for i, test in enumerate(tests):
    worksheet.write('A' + str(i+2), i+1)
    worksheet.write('B' + str(i+2), test['name'])
    if test['result']:
        worksheet.write('C' + str(i+2), 1, cellPass)
    else:
        worksheet.write('D' + str(i+2), 1, cellFail)
    worksheet.write('E' + str(i+2), test['date_time'])
# посчитать количество тестов
worksheet.write('F1', 'успешные тесты')
worksheet.write('G1', 'неуспешные тесты')
worksheet.write('F2', '=SUM(C:C)')
worksheet.write('G2', '=SUM(D:D)')

# делаем графика
chart = workbook.add_chart({'type': 'column'})
chart.add_series({'values': '=Sheet1!$F2'})
chart.add_series({'values': '=Sheet1!$G2'})
worksheet.insert_chart('H7', chart)

# закрыть док
workbook.close()