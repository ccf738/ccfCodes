# -*- coding:utf-8 -*-
__author__ = 'qctest'
import os
import shutil
import stat
import excel
import time
import win32com.client
import sqlite3
year = 2002
acct_seq = 0
num_seq = 0
id_seq = 0
def set_acct_no(file_name, branch_no, row_no):
    global acct_seq
    acct_seq += 1
    acct_no = "68" + str(branch_no) + "709" + str(acct_seq).rjust(7,'0')
    file_name.set_value(row_no, 2, acct_no)

def set_acct_seq(file_name, row_no):
    global year, num_seq
    num_seq += 1
    if num_seq == 10000:
        num_seq = 1
        year += 1
    loan_seq = str(year) + "9" + str(num_seq).rjust(4, '0')
    file_name.set_value(row_no, 4, loan_seq)

def set_id_no(file_name, branch_no,row_no, id_type, name_len):
    global id_seq
    id_seq += 1
    file_name.set_value(row_no, 20, '01')
    if name_len <= 4:
        id_type = "11"
        id_no = "zhdk" + str(branch_no) + str(id_seq).rjust(6,'0')
    else:
        id_type = "44"
        id_no = "zhkr" + str(id_seq).rjust(6, '0')
    file_name.set_value(row_no, 19, id_no)
    file_name.set_value(row_no, 18, id_type)

rep_loan_file = excel.Excel(unicode(r'D:\陈超峰\陈超峰\数据\20141203接收的20141124补录\1124补录发何东杰\置换贷款汇总表.xlsx', "utf-8"), "zhdk")
for i in xrange(rep_loan_file.used_range(), 2, -1):
    row = rep_loan_file.get_row_data(i)
    if row[2] is None:
        continue
    try:
        branch_no = int(row[0])
    except:
        branch_no = '85611001'
    id_type = row[18]
    set_acct_no(rep_loan_file,branch_no,i)
    set_acct_seq(rep_loan_file,i)
    if row[18] is None or row[19] is None:
        set_id_no(rep_loan_file,branch_no,i,id_type, len(row[2]))
rep_loan_file.quit()