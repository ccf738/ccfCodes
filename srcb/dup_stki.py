__author__ = 'qctest'

"""找出同一法人下一个客户多个股金账号的记录
db2 "select UPPER_STOCK_NO,MAST_ACCT，CUSTOMER_NO from stkiexp union select UPPER_STOCK_NO,MAST_ACCT, CUSTOMER_NO from
stki where CUSTOMER_NO in (select distinct CUSTOMER_NO from stkiexp) with ur" > stki1.txt
stki.sh"""


DATABASE_FILE  = unicode(r'D:\bgl\bgl.db', 'utf-8')


import sqlite3


def get_new_branch(old_branch):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT OLD_BRANCH, NEW_BRANCH FROM BRANCH_ONRF WHERE NEW_BRANCH = ?",  (old_branch, ))
    try:
        new_branch = cur.fetchone()[0]
    except:
        new_branch = -1
    conn.close()
    return new_branch

ori_stki = open(r'd:\dup_stki.txt', 'r')
dup_stki = open(r'd:\dup_stock.txt', 'w')
for line in ori_stki.readlines():
    dup_stock_record = []
    line = line[:-1]
    record = line.split("|")
    upper_no = record[0]
    branch_no = record[1].strip()
    customer = record[2]
    acct_no = record[3][2:]
    old_upper_no = get_new_branch(upper_no)
    old_branch_no = get_new_branch(branch_no)
    dup_stock_record.append(old_upper_no)
    dup_stock_record.append(old_branch_no)
    dup_stock_record.append(customer)
    dup_stock_record.append(acct_no)
    out_record = "|".join(dup_stock_record)
    dup_stki.write(out_record + '\n')

ori_stki.close()
dup_stki.close()