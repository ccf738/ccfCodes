# -*- coding:utf-8 -*-
__author__ = 'qctest'
"""对利息资本化的账号进行操作，使得核对工作变得简单"""

import sqlite3
DATABASE_FILE  = unicode(r'D:\bgl\bgl.db', 'utf-8')


def get_new_branch(old_branch):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT OLD_BRANCH, NEW_BRANCH FROM BRANCH_ONRF WHERE OLD_BRANCH = ?",  (old_branch, ))
    try:
        new_branch = cur.fetchone()[1]
    except:
        new_branch = -1
    conn.close()
    return new_branch


orig_file = open(r'D:\mig_report\term10.txt', 'r')
out_file = open(r'D:\mig_report\term10_out.txt', 'w')
for line in orig_file.readlines():
    out_fields = []
    line = line[:-1]
    orig_record = line.split("|")
    acct_no = orig_record[0]
    balance = float(orig_record[1])/100
    old_branch = orig_record[2]
    acct_type = orig_record[3]
    interest = float(orig_record[5])/100
    tax = float(orig_record[6])/100
    new_branch = get_new_branch(old_branch)
    out_fields.append(acct_no)
    out_fields.append(new_branch)
    out_fields.append(acct_type)
    out_fields.append(str(balance))
    out_fields.append(str(interest))
    out_fields.append(str(tax))
    out_record = "|".join(out_fields)
    out_file.write(out_record + '\n')
orig_file.close()
out_file.close()

out_detail = open(r'D:\mig_report\term10_out.txt', 'r')
out_branch = open(r'D:\mig_report\term10_branch.txt', 'w')
conn = sqlite3.connect(DATABASE_FILE)
cur = conn.cursor()
conn.execute("CREATE TABLE IF NOT EXISTS DEP_CAP (BRANCH TEXT, PRODUCT TEXT,BALANCE REAL, INTEREST REAL, TAX REAL)")
conn.execute("DELETE FROM DEP_CAP")
for line in out_detail.readlines():
    line = line[:-1]
    detail_fields = line.split("|")
    branch = detail_fields[1]
    product = detail_fields[2]
    balance = float(detail_fields[3])
    interest = float(detail_fields[4])
    tax = float(detail_fields[5])
    conn.execute("insert into dep_cap values (?,?,?,?,?)", (branch, product, balance, interest, tax))
conn.commit()
out_detail.close()
cur.execute("select branch,product,sum(balance),sum(interest),sum(tax) from dep_cap group by branch,product")
for table_branch, table_product, sum_balance, sum_interest, sum_tax in cur.fetchall():
    out_branch_record = []
    out_branch_record.append(table_branch)
    out_branch_record.append(table_product)
    out_branch_record.append(str(sum_balance))
    out_branch_record.append(str(sum_interest))
    out_branch_record.append(str(sum_tax))
    out_branch.write("|".join(out_branch_record) + "\n")
cur.close()
conn.close()
out_branch.close()