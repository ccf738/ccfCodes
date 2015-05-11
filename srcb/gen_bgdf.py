# -*- coding:utf-8 -*-
__author__ = 'qctest'
"""检查补录表的正确性，将合格的记录生成文件供cobol程序处理生成FAGD,CTAM,CONBB移植中间文件"""

import excel
import sqlite3



DATABASE_FILE  = unicode(r'D:\bgl\bgl.db', 'utf-8')


def is_legal_char(row, field, field_len, exp_file, exp_msg):
    try:
        return str(int(field)).ljust(field_len)
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


def preprocess_bgdf():
    BGDF_FILE = unicode(r'd:\银行承兑汇票补录\银行承兑汇票补录表.xls', "utf-8")
    BGDF_SHEET = "bgdf"
    PRE_FILE = open(unicode(r'd:\银行承兑汇票补录\PRE_BGDF.TXT', "utf-8"), "w")
    EXP_FILE = open(unicode(r'd:\银行承兑汇票补录\EXP_FILE.TXT', "utf-8"), "w")
    bgdf_additional_file = excel.Excel(BGDF_FILE, BGDF_SHEET)
    for i in xrange(bgdf_additional_file.used_range(), 2, -1):
        record = []
        is_legal = 1
        row = bgdf_additional_file.get_row_data(i)
        if row[0] is None:
            continue
        #机构号
        branch = is_legal_char(row, row[0], 8,  EXP_FILE, "机构号错误")
        if branch == -1:
            is_legal = 0
        new_branch = get_new_branch(branch)
        if new_branch == -1:
            is_legal = 0
        record.append(str(new_branch))
        #汇票号码
        draft_no = is_legal_number(row, row[1], 12, 0, EXP_FILE, "汇票号码错误")
        if draft_no == -1:
            is_legal = 0
        record.append("42" + draft_no[6:])
        #合同号码
        try:
            contract_no = row[2].encode("gb2312").ljust(100)
            record.append(contract_no)
        except:
            is_legal = 0
            EXP_FILE.write(str(row[0] + "|" + str(row[1])) + "|" + str(row[2]) + "|", "合同号错误")
        #收款人行号
        try:
            payee_bank = row[3].encode("gb2312").ljust(72)
            record.append(payee_bank)
        except:
            is_legal = 0
            print row[3]
            EXP_FILE.write(str(row[0]) + "|" + str(row[1]) + "|" + str(row[3]) + "|", "收款人行号错误")
        #收款人账号
        try:
            payee_acct_no = str(row[4]).ljust(32).replace(".", "")
            record.append(payee_acct_no)
        except:
            is_legal = 0
            EXP_FILE.write(str(row[0]) + "|" + str(row[1]) + "|" + str(row[4]) + "|", "收款人账号错误")
        # 收款人名称
        try:
            payee_name = row[5].encode("gb2312").ljust(72)
            record.append(payee_name)
        except:
            is_legal = 0
            EXP_FILE.write(str(row[0]) + "|" + str(row[1]) + "|" + str(row[5]) + "|", "收款人名称错误")
        # 票面金额
        draft_amt = is_legal_number(row, row[8], 17, 3, EXP_FILE, "票面金额错误")
        if draft_amt == -1:
            is_legal = 0
        record.append(draft_amt)
        # 签发日期
        issue_date = is_legal_char(row, row[9], 8, EXP_FILE, "签发日期错误")
        if issue_date == -1:
            is_legal = 0
        record.append(issue_date)
        # 到期日期
        maturity_date = is_legal_char(row, row[10], 8, EXP_FILE, "到期日期错误")
        if maturity_date == -1:
            is_legal = 0
        record.append(maturity_date)
        # 交易类型
        tran_type = is_legal_char(row, row[11], 1, EXP_FILE, "交易类型错误")
        if tran_type == -1:
            is_legal = 0
        tran_type = "0" + tran_type
        record.append(tran_type)
        # 转让标志
        transfer_type = is_legal_char(row, row[12], 1, EXP_FILE, "转让标志错误")
        if transfer_type == -1:
            is_legal = 0
        transfer_type = "0" + transfer_type
        record.append(transfer_type)
        # 出票人账号
        escrow_acct = is_legal_char(row, row[13], 25, EXP_FILE, "出票人账号错误")
        if escrow_acct == -1:
            is_legal = 0
        record.append(escrow_acct)
        # 银行承兑汇票专用章
        act_bank_sl_no = is_legal_char(row, row[15], 15, EXP_FILE, "银行承兑汇票专用章错误")
        if act_bank_sl_no == -1:
            is_legal = 0
        record.append(act_bank_sl_no)
        if is_legal == 1:
            file_record = "|".join(record)
            file_record += "\n"
            PRE_FILE.write(file_record)

    bgdf_additional_file.quit_without_save()
    PRE_FILE.close()
    EXP_FILE.close()

    # 生成BGDF文件供cobol处理
    pre_file = open(unicode(r'd:\银行承兑汇票补录\PRE_BGDF.TXT', "utf-8"), "r")
    cobol_file = open(unicode(r'd:\银行承兑汇票补录\COB_BGDF.TXT', "utf-8"), "w")
    for line in pre_file.readlines():
        file_record = ""
        line = line[:-1]
        record = line.split("|")
        file_record += record[0]
        file_record += record[1]
        file_record += record[2]
        file_record += record[3]
        file_record += record[4]
        file_record += record[5]
        file_record += record[6]
        file_record += record[7]
        file_record += record[8]
        file_record += record[9]
        file_record += record[10]
        file_record += record[11]
        file_record += record[12]
        file_record += "\n"
        cobol_file.write(file_record)
    pre_file.close()
    cobol_file.close()

preprocess_bgdf()
