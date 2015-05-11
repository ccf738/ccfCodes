# -*- coding:utf-8 -*-
__author__ = 'qctest'

import excel
import sqlite3

DATABASE_FILE  = unicode(r'D:\bgl\bgl.db', 'utf-8')
clear_center_subject = ['10020101','10020201','10110101','10110201','10119901','10120101','10120102',
                        '10120103','10120201','10120301','20190101','20190201','20190301','20190401',
                        '20190501','20199901','20200101','20200201','22411201']

def load_new_bgl():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS NEW_BGL (BRANCH TEXT, SUBJECT_NO TEXT, BGL_ACCT TEXT)")
    conn.execute("CREATE UNIQUE INDEX  IF NOT EXISTS NEW_BGL_PK ON NEW_BGL (BRANCH, SUBJECT_NO)")
    conn.execute("DELETE FROM NEW_BGL")
    cur.execute("SELECT * FROM NEW_BGL")
    rows_selected = len(cur.fetchall())
    if rows_selected > 0:
        print "NEW BGL DATA ALREADY LOADED"
        conn.close()
        return
    new_bgl = excel.Excel(unicode(r'D:\bgl\新核心内部帐', "utf-8"), "Sheet1")
    for i in xrange(new_bgl.used_range(), 1, -1):
        row = new_bgl.get_row_data(i)
        branch_no = row[0]
        acct_no = row[1]
        subject_no = row[2]
        try:
            conn.execute("INSERT INTO NEW_BGL VALUES (?, ?, ?)", (branch_no, subject_no, acct_no))
        except:
            print branch_no, subject_no
    conn.commit()
    conn.close()
    new_bgl.quit_without_save()

def load_branch_onrf():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS BRANCH_ONRF (OLD_BRANCH TEXT, NEW_BRANCH TEXT)")
    conn.execute("DELETE FROM BRANCH_ONRF")
    cur.execute("SELECT * FROM BRANCH_ONRF")
    rows_selected = len(cur.fetchall())
    if rows_selected > 0:
        print "NEW BRANCH ONRF ALREADY LOADED"
        conn.close()
        return
    branch_onrf = excel.Excel(unicode(r'D:\bgl\新旧机构代码对照表', "utf-8"), "Sheet1")
    for i in xrange(branch_onrf.used_range(), 1, -1):
        row = branch_onrf.get_row_data(i)
        if row[1] is None or row[2] is None:
            continue
        old_branch = str(int(row[1]))
        new_branch = str(int(row[2])).rjust(5, "0")
        try:
            conn.execute("INSERT INTO BRANCH_ONRF VALUES (?, ?)", (old_branch, new_branch))
        except:
            print old_branch, new_branch
    conn.commit()
    conn.close()
    branch_onrf.quit_without_save()

def load_glcc_onrf():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS GLCC_ONRF (OLD_GLCC TEXT, NEW_GLCC TEXT)")
    conn.execute("CREATE UNIQUE INDEX  IF NOT EXISTS GLCC_ONRF_PK ON GLCC_ONRF (OLD_GLCC)")
    conn.execute("DELETE FROM GLCC_ONRF")
    cur.execute("SELECT * FROM GLCC_ONRF")
    rows_selected = len(cur.fetchall())
    if rows_selected > 0:
        print "GLCC ONRF ALREADY LOADED"
        conn.close()
        return
    glcc_onrf = excel.Excel(unicode(r'D:\bgl\新旧科目对照表', "utf-8"), "mig_use")
    for i in xrange(glcc_onrf.used_range(), 1, -1):
        row = glcc_onrf.get_row_data(i)
        if row[0] is None:
            continue
        new_glcc = str(int(row[0]))
        old_glcc = str(int(row[1]))
        #表外前补零
        if len(new_glcc) == 7:
            new_glcc = "0" + new_glcc
        if len(old_glcc) in [5, 7]:
            old_glcc = "0" + old_glcc
        try:
            conn.execute("INSERT INTO GLCC_ONRF VALUES (?, ?)", (old_glcc, new_glcc))
        except:
            print old_glcc, new_glcc
    conn.commit()
    conn.close()
    glcc_onrf.quit_without_save()


def load_all_old_glcc(subject_list):
    glcc_onrf = excel.Excel(unicode(r'D:\bgl\新旧科目对照表', "utf-8"), "mig_use")
    for i in xrange(glcc_onrf.used_range(), 1, -1):
        row = glcc_onrf.get_row_data(i)
        if row[0] is None:
            continue
        old_glcc = str(int(row[1]))
        if len(old_glcc) in [5, 7]:
            old_glcc = "0" + old_glcc
        subject_list.append(old_glcc)
    glcc_onrf.quit_without_save()


def get_old_glcc(long_glcc, third_level_list):
    """long glcc 是9位的科目,如果不在third_level_list里面，则用8位的去找，
    如果8位的科目还不在third_level_list里面，则认为这个科目按2极迁移"""
    if long_glcc in third_level_list:
        return long_glcc
    if long_glcc[:-1] in third_level_list:
        return long_glcc[:-1]
    if long_glcc[:-2] in third_level_list:
        return long_glcc[:-2]
    if long_glcc[:-4] in third_level_list:
        return long_glcc[:-4]
    return long_glcc[:4]


def get_bgl_glcc():
    bgl_glcc = []
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT SUBJECT_NO FROM NEW_BGL")
    for new_glcc in cur.fetchall():
        bgl_glcc.append(new_glcc[0])
    cur.close()
    conn.close()
    return bgl_glcc

class Data():
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cur = self.conn.cursor()
        #self.conn.execute("delete from glcc_onrf where substr(old_glcc,1,4) in ('1295', '1291', '1411', '1421', '1422', '1511', '1621', '1521', '1541', '1531', '1611', '1621', '2415', '2651', '4639', '4641', '2316', '5121', '5151', '5141', '5321', '5331', '5341', '1623', '5361', '5501')")
        #self.conn.commit()
    def get_new_branch(self, old_branch):
        #get new branch_no from branch_onrf
        self.cur.execute("SELECT OLD_BRANCH, NEW_BRANCH FROM BRANCH_ONRF WHERE OLD_BRANCH = ?",  (old_branch, ))
        try:
            return self.cur.fetchone()[1]
        except:
            return "-1"

    def get_new_acct(self, branch, subject_no):
        subject_no.rjust(8, '0')
        self.cur.execute("SELECT COUNT(1) FROM NEW_BGL WHERE BRANCH = ? AND SUBJECT_NO  = ?", (branch, subject_no))
        no_of_acct = self.cur.fetchone()[0]
        if no_of_acct == 0:
            return "新核心无此科目内部帐"
        if no_of_acct > 1:
            return_msg = str(no_of_acct) + " accts found| "
            self.cur.execute("SELECT BRANCH, BGL_ACCT FROM NEW_BGL WHERE BRANCH = ? AND SUBJECT_NO = ?", (branch, subject_no))
            for _, acct in self.cur.fetchall():
                return_msg = return_msg + str(acct).strip() + " "
            return return_msg
        self.cur.execute("SELECT BGL_ACCT FROM NEW_BGL WHERE BRANCH = ? AND SUBJECT_NO = ?", (branch, subject_no))
        return self.cur.fetchone()[0]

    def get_new_glcc(self, old_glcc):
        self.cur.execute("SELECT OLD_GLCC, NEW_GLCC FROM GLCC_ONRF WHERE OLD_GLCC = ?", (old_glcc, ))
        try:
            return self.cur.fetchone()[1]
        except:
            return "-1"


class Out_file():
    def __init__(self):
        self.orig_file = open(r'D:\bgl\old_bgl.txt', 'r')
        self.out_file = open(r'D:\bgl\bgl_onrf.txt', 'w')

    def get_row_data(self):
        #usr generator to get each row date in outfile
        for line in self.orig_file.readlines():
            yield line

        pass
    def write_exception(self, data, exception_msg):
        #data.append(" ")
        data.append(exception_msg)
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        try:
            self.out_file.write(",".join(data) + "\n")
        except:
            print "write exception", data, exception_msg

    def write_new_acct(self, data, branch, glcc, acct_no):
        #data.append(" ")
        data.append(str(glcc))
        data.append(str(acct_no))
        data.append("")
        data.append(str(branch))
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        data.append("")
        try:
            self.out_file.write(",".join(data) + "\n")
        except:
            print "write normal", data, branch, glcc, acct_no

    def quit(self):
        self.orig_file.close()
        self.out_file.close()


#load_new_bgl()
#load_branch_onrf()
load_glcc_onrf()
bgl_glcc = get_bgl_glcc()
data = Data()
out_file = Out_file()
third_level_glcc = []  # 三级科目列表
load_all_old_glcc(third_level_glcc)
i = 0
for line in out_file.get_row_data():
    i += 1
    if i % 5000 == 0:
        print i, "rows processed"
    line = str(line).replace("\n", "")
    line = line[:-1] + "|"
    line_data = str(line).split("|")
    old_branch = line_data[0]
    acct_no = line_data[3]
    old_glcc = get_old_glcc(acct_no[10:20], third_level_glcc)
    line_data[1] = str(line_data[1]).split(".")[0]
    #if line_data[4] == "":
    #    line_data[4] = "noname"
    #    line_data.append("")
    line_data.pop(4)
    line_data.pop()
    #get new branch no
    new_branch = data.get_new_branch(old_branch)
    if new_branch == "-1":
        out_file.write_exception(line_data, "新机构号未找到")
        continue
    new_branch.rjust(5, "0")
    #get new glcc
    new_glcc = data.get_new_glcc(old_glcc)
    if new_glcc == "10120101" and new_branch == "01000":
        new_glcc = "10310101"
    if new_branch != '01000' and new_glcc == '10310101':
        out_file.write_exception(line_data, "除了省清算其他机构的不应该有这个科目的账号")
        continue
    if old_branch in ['85820101', '85830101', '85860101'] and new_glcc == '10120101':
        new_branch = '81001'
    if new_glcc == "-1":
        out_file.write_exception(line_data, "新科目号未找到")
        continue
    #get new bgl acct
    #if new_glcc in clear_center_subject:
    #    new_branch = new_branch[0:4] + "0"
    new_bgl = data.get_new_acct(new_branch, new_glcc)
    if len(new_bgl) != 16:
        if new_glcc in bgl_glcc:
            new_bgl = "此机构无此科目内部帐"
        out_file.write_exception(line_data, new_bgl)
        continue
    #write new bgl information to bgl onrf
    out_file.write_new_acct(line_data, new_branch, new_glcc, new_bgl)
out_file.quit()