__author__ = 'qctest'

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

def is_legal_char(row, field, field_len, exp_file, exp_msg):
    try:
        return str(int(field)).ljust(field_len)
    except:
        try:
            return str(field).ljust(field_len)
        except:
            exp_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(field) + "|" + exp_msg + "\n"
            exp_file.write(exp_record)
            return -1


def is_legal_number(row, field, field_len, precision, exp_file, exp_msg):
    try:
        result = float(field)
        if precision == 3:
            result = "%.3f" % (result, )
        elif precision == 4:
            result = "%.4f" % (result, )
        elif precision == 5:
            result = "%.5f" % (result, )
        elif precision == 6:
            result = "%.6f" % (result, )
        elif precision == 0:
            result = "%.0f" % (result, )
        return result.replace(".", "").rjust(field_len, "0")
    except:
        exp_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(field) + "|" + exp_msg + "\n"
        exp_file.write(exp_record)
        return -1