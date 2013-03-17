'''
Created on 2012-8-13

@author: ccf
'''
import win32com.client
from ftplib import FTP
import os
shell = []
cat = []
value = ''
app = win32com.client.Dispatch('Excel.Application')
workbook = app.Workbooks.Open(r'C:\Users\ccf\Desktop\change list.xlsx')
print workbook.Sheets.Count
sheet = workbook.Sheets('ccf1')
print sheet.UsedRange.Rows.Count
for i in range(1,sheet.UsedRange.Rows.Count):
    row = sheet.UsedRange.Rows[i].Value[0]
    if row[0]:
        value = row[0]
        value = value.strip()
        if value not in cat:
            cat.append(value)
            value = ''
    if row[1]:
        value = row[1]
        value = value.strip()
        if value not in shell:
            shell.append(value)
            value = ' '
workbook.Close()
app.Quit()


ftp = FTP('10.20.147.12')
ftp.login('fnsonlpd','srcb123')
if cat:
    os.chdir('C:\\Users\\ccf\\Desktop\\programmes\\cat')
    ftp.cwd('/fns/p/r/cat')
    for codes in cat:
        ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
if shell:
    os.chdir('C:\\Users\\ccf\\Desktop\\programmes\\shell')
    ftp.cwd('/fns/p/r/sh')
    for codes in shell:
        ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
ftp.quit()
jobs = open(r'C:\Users\ccf\Desktop\list','w')
for job in shell:
    jobs.write(job + '\n')
for job in cat:
    jobs.write(job + '\n')
jobs.close()