# -*- coding:utf-8 -*-
__author__ = 'qctest'

import excel
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


def is_legal_number(field, field_len, precision):
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


def gen_cust_record(cust_info):
    """create file CINO CIF ADNM"""
    cino_record = ""
    cif_record = ""
    adnm_record1 = ""
    adnm_record2 = ""
    cino_record += cust_info.get("customer_no").ljust(22)
    cino_record += cust_info.get("id_no").ljust(32)
    cino_record += cust_info.get("id_type")
    cino_record += cust_info.get("cust_type", "02")
    cino_record += cust_info.get("cust_sub_type", "201")

    cif_record += cust_info.get("customer_no").ljust(22)
    cif_record += cust_info.get("id_expiry_date")
    cif_record += cust_info.get("branch_no")
    cif_record += "01"
    cif_record += "12"
    cif_record += "0"
    cif_record += cust_info.get("pers_cust_name", " ").ljust(40)
    cif_record += " " * 40
    cif_record += " " * 20
    cif_record += "CN"
    cif_record += "0"
    cif_record += "1"
    cif_record += "0"
    cif_record += "0"
    cif_record += "0" * 8
    cif_record += "0" * 17
    cif_record += "7"
    cif_record += cust_info.get("cop_cust_name", " ").ljust(80)  # 企业客户名称
    cif_record += cust_info.get("industry_code", " ").ljust(5)  #行业分类
    cif_record += "CN"
    cif_record += cust_info.get("bus_owsp", " ")  # 企业性质
    cif_record += cust_info.get("ecnm_code", "1")  # 企业经济成分
    cif_record += cust_info.get("cop_per_name", " ").ljust(20)  # 法人代表姓名
    cif_record += cust_info.get("cop_per_id_type", "01").ljust(2)  # 法人代表证件类型
    cif_record += cust_info.get("cop_per_id_no", " ").ljust(32)  # 法人代表证件号码
    cif_record += "bank business".ljust(30)
    cif_record += "own".ljust(20)
    cif_record += "CNY"
    cif_record += "0" * 17
    cif_record += cust_info.get("fin_cust_name", " ").ljust(120)  # 金融客户名称
    cif_record += cust_info.get("fin_cust_for_name", " ").ljust(150)  #金融客户英文名称
    cif_record += cust_info.get("fin_type", " ").ljust(4)  # 金融机构类别
    cif_record += cust_info.get("fin_tier", " ").ljust(4)  # 金融机构层级
    cif_record += "0"
    cif_record += "0"
    cif_record += "0"
    cif_record += " " * 12
    cif_record += " " * 12
    cif_record += " " * 15
    cif_record += " " * 22
    cif_record += " " * 22
    cif_record += " " * 300
    cif_record += " " * 35
    cif_record += " " * 35
    cif_record += " " * 35
    cif_record += " " * 7
    cif_record += " " * 7
    cif_record += "0" * 17 # 家庭股票额
    cif_record += "0" * 17
    cif_record += "0" * 17
    cif_record += "0" * 17
    cif_record += "0" * 2
    cif_record += "0" * 17
    cif_record += "0" * 17
    cif_record += "0" * 17
    cif_record += "0" * 17
    cif_record += "0" * 17
    cif_record += " " * 60
    cif_record += " " * 40
    cif_record += " " * 40
    cif_record += "17"  # 客户信用等级
    cif_record += "6"
    cif_record += "5"
    cif_record += "0"
    cif_record += "0"
    cif_record += "0" * 20
    cif_record += "0"
    cif_record += "2"
    cif_record += "9"
    cif_record += "0"
    cif_record += "A"
    cif_record += "0"
    cif_record += "0"
    cif_record += "19991231"
    cif_record += "17"  # 企业客户信用等级
    cif_record += "0" * 8
    cif_record += " " * 15
    cif_record += "9"
    cif_record += " " * 60
    cif_record += "0" * 8
    cif_record += "0" * 8
    cif_record += "23"
    cif_record += "01"
    cif_record += "0"
    cif_record += "4"
    cif_record += "4"
    cif_record += "0"
    cif_record += "4"
    cif_record += " " * 40
    cif_record += " " * 40
    cif_record += "9"
    cif_record += " " * 40
    cif_record += " " * 16
    cif_record += "9"
    cif_record += "9"
    cif_record += "9"
    cif_record += "foreign_name".ljust(120)
    cif_record += " " * 60
    cif_record += " " * 26
    cif_record += "N"
    cif_record += cust_info.get("boss_name", "wu xing ming").ljust(20)  # 法人代表姓名
    cif_record += "CNY"
    cif_record += "0" * 17
    cif_record += "CN"
    cif_record += "0" * 8
    cif_record += "00"
    cif_record += " " * 24
    cif_record += " " * 20
    cif_record += "0"
    cif_record += "0"
    cif_record += "CN"
    cif_record += "0" * 8
    cif_record += " " * 200
    cif_record += "0"
    cif_record += "0"
    cif_record += "0"
    cif_record += cust_info.get("id_no", "mei you id ").ljust(32)  # 组织机构代码号
    cif_record += " " * 32
    cif_record += " " * 32
    cif_record += "19991231"
    cif_record += " " * 20
    cif_record += " " * 22
    cif_record += " " * 16
    cif_record += " " * 20
    cif_record += " " * 22
    cif_record += " " * 16
    cif_record += " " * 23
    cif_record += " "
    cif_record += "0" * 4  # 企业创建年份
    cif_record += "0" * 7
    cif_record += " " * 10
    cif_record += " " * 10
    cif_record += " " * 10
    cif_record += "99"
    cif_record += "99"
    cif_record += "99"
    cif_record += " " * 10
    cif_record += "0" * 17
    cif_record += " " * 3
    cif_record += "0" * 17
    cif_record += " " * 32
    cif_record += "0" * 8
    cif_record += "0" * 17

    adnm_record1 += cust_info.get("customer_no").ljust(22)
    adnm_record2 += cust_info.get("customer_no").ljust(22)
    adnm_record1 += "00"
    adnm_record2 += "01"
    if int(cust_info.get("id_type")) < 12:
        adnm_record1 += "01"
        adnm_record2 += "02"
    else:
        adnm_record1 += "03"
        adnm_record2 += "04"
    adnm_record1 += cust_info.get("cust_addr", "qing hai").ljust(120)
    adnm_record2 += cust_info.get("cust_addr", "qing hai").ljust(120)
    adnm_record1 += " " * 20
    adnm_record2 += " " * 20
    adnm_record1 += " " * 20
    adnm_record2 += " " * 20
    adnm_record1 += " " * 20
    adnm_record2 += " " * 20
    adnm_record1 += "0" * 8
    adnm_record2 += "0" * 8
    adnm_record1 += " " * 22
    adnm_record2 += " " * 22
    adnm_record1 += " " * 22
    adnm_record2 += " " * 22
    adnm_record1 += " " * 16
    adnm_record2 += " " * 16
    adnm_record1 += " " * 22
    adnm_record2 += " " * 22
    adnm_record1 += " " * 30
    adnm_record2 += " " * 30
    adnm_record1 += " " * 30
    adnm_record2 += " " * 30
    adnm_record1 += "19991231"
    adnm_record2 += "19991231"
    adnm_record1 += "20991231"
    adnm_record2 += "20991231"
    adnm_record1 += "0" * 8
    adnm_record2 += "0" * 8
    adnm_record1 += "0" * 5
    adnm_record2 += "0" * 5

    return cino_record, cif_record, adnm_record1, adnm_record2


def create_trust_loan_detail():
    acct_seq = 1
    acct_list = set([])
    customer_no_start = 333344441111
    customer_seq = 1
    loan_detail = excel.Excel(unicode(r'D:\委托贷款\委托贷款明细.xlsx', "utf-8"), "Sheet1")
    loan_middle = open(unicode(r'D:\委托贷款\PBORM.TXT', "utf-8"),  "w")
    pre_cust_file = open(unicode(r'D:\委托贷款\PRE_CUST.TXT', "utf-8"),  "w")
    for i in xrange(loan_detail.used_range(), 2, -1):
        middle_file_record = []
        customer_record = []
        row = loan_detail.get_row_data(i)
        branch_no = str(int(row[0]))
        new_branch = str(get_new_branch(branch_no))
        middle_file_record.append(new_branch)

        acct_no = str(int(row[1]))
        if acct_no in acct_list:
            old_acct_no =  str(acct_no) + str(acct_seq)
            acct_seq += 1
        else:
            old_acct_no = acct_no
        acct_list.add(acct_no)
        middle_file_record.append("7" + old_acct_no.ljust(24))

        acct_stat = str(int(row[5])).rjust(2, '0')
        middle_file_record.append(acct_stat)

        open_date = str(int(row[7]))
        maturity_date = str(int(row[8]))
        middle_file_record.append(open_date)
        middle_file_record.append(maturity_date)

        try:
            adv_bal = float(row[11])
        except:
            adv_bal = 0
        adv_bal = is_legal_number(adv_bal, 18, 3)
        middle_file_record.append(adv_bal)

        try:
            loan_bal = float(row[12])
        except:
            loan_bal = 0
        loan_bal = is_legal_number(loan_bal, 18, 3)
        middle_file_record.append(loan_bal)

        try:
            theo_loan_bal = float(row[13])
        except:
            theo_loan_bal = 0
        theo_loan_bal = is_legal_number(theo_loan_bal, 18, 3)
        middle_file_record.append(theo_loan_bal)

        try:
            unpd_prin = float(row[14])
        except:
            unpd_prin = 0
        unpd_prin = is_legal_number(unpd_prin, 18, 3)
        middle_file_record.append(unpd_prin)

        customer_no = str(customer_no_start) + str(customer_seq)
        customer_seq += 1
        customer_no = customer_no.ljust(22)

        middle_file_record.append(customer_no)
        if int(row[3]) < 12:
            loan_type = "1"
        else:
            loan_type = "2"
        middle_file_record.append(loan_type)
        middle_file_record.append(str(int(row[17])))
        loan_middle.write("".join(middle_file_record) + "\n")


        customer_name = row[2].encode("gb2312")
        id_type = is_legal_number(row[3],2,0)
        id_no = str(row[4]).ljust(32)
        customer_record.append(customer_no)
        customer_record.append(customer_name)
        customer_record.append(id_type)
        customer_record.append(id_no)
        customer_record.append(new_branch)
        pre_cust_file.write("|".join(customer_record) + "\n")
    loan_detail.quit_without_save()
    loan_middle.close()
    pre_cust_file.close()


def create_customer_info():
    pre_info = open(unicode(r'D:\委托贷款\PRE_CUST.TXT', "utf-8"),  "r")
    loan_cino = open(unicode(r'D:\委托贷款\LOAN_CINO.TXT', "utf-8"),  "w")
    loan_cif = open(unicode(r'D:\委托贷款\LOAN_CIF.TXT', "utf-8"),  "w")
    loan_adnm = open(unicode(r'D:\委托贷款\LOAN_ADNM.TXT', "utf-8"),  "w")
    for line in pre_info.readlines():
        line = line[:-1]
        cust_info = {}
        record = line.split("|")
        cust_info["customer_no"] = record[0]
        cust_info["id_no"] = record[3]
        cust_info["id_type"] = record[2]
        if int(record[2]) < 12:
            cust_info["cust_type"] = "01"
            cust_info["cust_sub_type"] = "101"
            cust_info["pers_cust_name"] = record[1]
        else:
            cust_info["cop_cust_name"] = record[1]
        cust_info["id_expiry_date"] = "20991231"
        cust_info["branch_no"] = record[4]
        cino_record, cif_record, adnm_record1, adnm_record2 = gen_cust_record(cust_info)
        loan_cino.write(cino_record + "\n")
        loan_cif.write(cif_record + "\n")
        loan_adnm.write(adnm_record1 + "\n")
        loan_adnm.write(adnm_record2 + "\n")
    pre_info.close()
    loan_cino.close()
    loan_cif.close()
    loan_adnm.close()


if __name__ == "__main__":
    create_trust_loan_detail()
    create_customer_info()
