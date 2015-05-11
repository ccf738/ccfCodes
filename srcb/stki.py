# -*- coding:utf-8 -*-
__author__ = 'qctest'

import sqlite3

DATABASE_FILE  = unicode(r'D:\bgl\bgl.db', 'utf-8')


def get_old_branch(new_branch):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT OLD_BRANCH, NEW_BRANCH FROM BRANCH_ONRF WHERE NEW_BRANCH = ?",  (new_branch, ))
    try:
        old_branch = cur.fetchone()[0]
    except:
        old_branch = -1
    conn.close()
    return str(old_branch)


orig_file = open(r'D:\dup_stki.txt', 'r')
out_file = open(r'D:\dup_stki_out.txt', 'w')
for line in orig_file.readlines():
    out_fields = []
    line = line[:-1]
    orig_record = line.split("|")
    new_branch = orig_record[0]
    new_upper_branch = orig_record[1]
    customer_name = orig_record[2]
    acct_no = orig_record[3]
    out_fields.append(get_old_branch(new_branch))
    out_fields.append(get_old_branch(new_upper_branch.strip()))
    out_fields.append(customer_name)
    out_fields.append(acct_no)
    out_file.write("|".join(out_fields) + '\n')
orig_file.close()
out_file.close()