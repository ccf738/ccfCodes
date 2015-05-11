# -*- coding:utf-8 -*-
__author__ = 'qctest'

"""
 对补录数据进行预处理
    4个例外文件
        INMT1_EXCEPTION.TXT  金融客户定期例外文件
        INMS1_EXCEPTION.TXT  金融客户活期例外文件
        INMS2_EXCEPTION.TXT  对公客户活期例外文件
        INMT2_EXCEPTION.TXT  金融客户定期例外文件
    6个临时文件用于生成移植中间表
        INMT1.TXT  金融客户定期文件，用于生成 ONRF INMT5
        INMS1.TXT  金融客户活期文件，用于生成 ONRF INMS5
        INMS2.TXT  对公客户活期文件，用于生成 ONRF INMS5
        INMT2.TXT  对公客户定期文件，用于生成 ONRF INMT5
        SAVING_CUS_INFO.TXT  对公客户活期文件，用于生成 CINO CIF ADNM
        TERM_CUS_INFO.TXT   对公客户定期文件， 用于生成 CINO CIF ADNM
    7个移植中间文件
        PCINO.TXT
        PCIF.TXT
        PADNM.TXT
        PINMS6.TXT
        PINMT6.TXT
        SAVEONRF.TXT
        TERMONRF.TXT
"""
import excel
import sqlite3
from datetime import date

CUST_START_NO = 444444444444444  # 活期客户开始序号
CUST_START_NO2 = 444444444444445  # 定期客户开始序号
CUST_START_NO3 = 44444444444446  # 定期金融客户开始序号
CUST_START_NO4 = 44444444444447  # 活期金融客户开始序号
ACCTS = {}  # 用于生成不同账号
TODAY = date(2015, 3, 18)  # 移植日期,用于计算计提，日终+1
SEASON_START_DATE = date(2015, 1, 21)  # 本季度开始日期，用于计算利息
NATU_SEASON_DATE = date(2015, 1, 1)  # 本季度开始日期，用于计算小额管理费天数
DATABASE_FILE = unicode(r'D:\bgl\bgl.db', 'utf-8')
bgl_inv_onrf = open(unicode(r'D:\金融机构存款\acct_onrf.sh', "utf-8"),  "w")
bgl_inv_onrf.write("db2 connect to $DB2_SID\n")
bgl_inv_onrf.write("cd $data/temp/\n")
bgl_inv_onrf.write("rm -f old_acct_onrf.txt\n")
FIN_CUST_INFO = {"customer_no": "66666666666666666666",
                 "id_no": "1",
                 "id_type": "44",
                 "id_expiry_date": "20991231",
                 "branch_no": "10001",
                 "customer_name": "jin rong ke hu",
                 "fin_cust_name": "jin rong ji gou ke hu",
                 "fin_cust_for_name":"jin rong ji gou wai wen ming",
                 "fin_type": "3102",
                  "fin_tier": "3001",
                 "cust_type": "03",
                 "cust_sub_type": "301"}


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


def gen_onrf(acct_info):
    record = ""
    record += acct_info.get("acct_no").ljust(25)
    record += " " * 25
    record += "K"
    record += acct_info.get("customer_no").ljust(22)
    record += acct_info.get("branch")
    record += acct_info.get("product")
    record += acct_info.get("open_date")
    record += " "
    record += acct_info.get("curr_bal")
    record += " " * 60
    record += "00"
    return  record


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
    cif_record += " " * 40
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


def gen_term_info(acct_info):
    record = ""
    record += acct_info.get("acct_no").ljust(25)
    record += " " * 25
    record += acct_info.get("acct_stat")
    record += "N"
    record += "01"
    record += acct_info.get("rate_ind")
    record += acct_info.get("rate")
    from_date = acct_info.get("int_from_date")
    from_date = date(int(from_date[0:4]), int(from_date[4:6]), int(from_date[6:8]))
    till_days = (TODAY - from_date).days
    rate = float(acct_info.get("rate")) / 1000000
    balance = float(acct_info.get("curr_bal")) / 1000
    if acct_info.get("rate_ind") == "M":
        interest = balance * 0.385 / 360 / 100 * till_days
        incr = balance * 0.385 / 360 / 100
    else:
        interest = balance * rate / 360 / 100 * till_days
        incr = balance * rate  / 360 / 100
        if interest < 0:
            print acct_info.get("acct_no"), from_date, rate,till_days
    int_accr = is_legal_number(None, interest, 18, 5, None, None)
    int_incr = is_legal_number(None, incr, 18, 5, None, None)
    record += int_accr
    record += acct_info.get("maturity_int")
    record += int_incr
    record += acct_info.get("int_from_date")
    if  acct_info.get("rate_ind") != "M":
        record += acct_info.get("int_to_date")
    else:
        record += "99999999"
    record += acct_info.get("term_period")
    record += "M"
    if acct_info.get("rate_ind") != "L":
        record += acct_info.get("term_maturity_date")
    else:
        record += "0" * 8
    if acct_info.get("rollover_flag", "R") == "R":
        record += "R "
    else:
        record += "I "
    record += " " * 25
    record += "M  "
    record += acct_info.get("rollover_flag", "R")
    record += "0" * 9
    record += "0" * 8
    record += acct_info.get("int_from_date")
    record += "00"
    record += " "
    record += "0" * 18
    record += "0" * 18
    record += "0" * 18
    record += "01"
    record += "0" * 18
    record += "0"
    record += " "  # 违约标志
    record += "0" * 18
    record += "0" * 8
    record += "0" * 18
    record += "0" * 18
    record += "6"  # 支取方式
    record += "N"
    record += " " * 32
    record += " " * 4
    record += " " * 4
    record += " " * 20
    record += "0"
    record += "N"
    record += "N"
    record += "0" * 8
    record += "0" * 5
    record += "0" * 17
    record += "0" * 5
    record += "0" * 5
    record += "0" * 5
    record += "0" * 5
    record += "0" * 17
    record += " " * 25
    record += "000002"
    record += "0"
    record += "0" * 8
    record += "1"
    record += "0"
    record += "0"
    record += "N"
    record += "0" * 1
    record += "0" * 2
    record += acct_info.get("int_from_date")
    record += "0" * 1
    record += "6"  # 费用减免标准
    record += "0" * 17
    record += "N"
    record += "0"
    record += "0" * 8
    record += "BB"
    record += " " * 80
    return record


def gen_save_info(acct_info):
    record = ""
    record += acct_info.get("acct_no").ljust(25)
    record += " " * 25
    record += acct_info.get("acct_stat")
    record += "N"
    record += acct_info.get("open_date")
    record += "Y"
    record += "N"
    record += " " * 32
    if acct_info.get("rate_type", "1") == "2":
        rate = float(acct_info.get("rate")) / 1000000
        if rate > 90:
            rate = 0.42
            record += "000420000"
        else:
            record += acct_info.get("rate")
    else:
        record += "000000000"
        rate = float(acct_info.get("rate")) / 1000000
    balance = float(acct_info.get("curr_bal")) / 1000
    incr = balance * rate / 360 / 100
    #interest = incr * (TODAY - SEASON_START_DATE).days
    #int_accr = is_legal_number(None, interest, 18, 5, None, None)
    int_incr = is_legal_number(None, incr, 18, 5, None, None)
    record += acct_info.get("int_accr", "0"*18)
    record += int_incr
    record += "E"
    record += "00"
    record += "0" * 18
    record += acct_info.get("acct_attr", "3")
    record += acct_info.get("open_acct_seq_no", "99999999999999999999").ljust(20)
    record += acct_info.get("appr_date", acct_info.get("open_date"))
    record += acct_info.get("open_date")
    record += acct_info.get("appr_no", "99999999999999999999").ljust(20)
    record += "000002"
    record += " " * 20
    record += "0" * 18
    record += "0" * 18
    record += "0" * 18
    record += "BB"
    record += " " * 80
    record += "6"
    record += " " * 4
    record += " " * 20
    record += " " * 1
    record += "0" * 2
    record += "0" * 2
    record += " " * 4
    record += " "
    record += "N"
    record += "N"
    record += "0" * 8
    record += "0" * 5
    record += "0" * 17
    record += "0" * 5
    record += "0" * 5
    record += "0" * 5
    record += "0" * 5
    record += "0" * 17
    record += acct_info.get("curr_bal")
    small_bal_fee_days = (TODAY - NATU_SEASON_DATE).days + 1
    record += str(small_bal_fee_days).rjust(6, "0")
    record += "0" * 8
    record += "1"
    record += "0"
    record += "0"
    record += "0"
    record += "0"
    record += "6"
    record += "1"
    record += "0" * 5
    record += "0" * 17
    record += "0" * 17
    return record


def gen_fin_cus_term():
    """金融客户定期"""
    global ACCTS
    global CUST_START_NO3
    cust_seq = 0
    fin_cus_term = excel.Excel(unicode(r'D:\金融机构存款\金融机构汇总.xlsx', "utf-8"), "4")
    out_fin_cus_term = open(unicode(r'D:\金融机构存款\INMT1.TXT', "utf-8"),  "w")
    exception_file = open(unicode(r'D:\金融机构存款\INMT1_EXCEPTION.TXT', "utf-8"), "w")
    acct_seq = 0  # 用来生成不同的旧账号
    for i in xrange(fin_cus_term.used_range(), 1, -1):
        cust_seq += 1
        record = []
        is_legal = 1
        row = fin_cus_term.get_row_data(i)
        if row[1] is None:
            continue
        # 机构号
        old_branch = is_legal_char(row, row[0], 8, exception_file, "机构号错误")
        if old_branch == -1:
            is_legal = 0
        new_branch = get_new_branch(str(int(row[0])))
        if new_branch == -1:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(int(row[0])) + "|" + "新机构号未找到" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        record.append(str(new_branch).encode("utf-8"))

        # 账号
        acct_no = is_legal_char(row, row[1], 21, exception_file, "账号错误")
        if acct_no == -1:
            is_legal = 0
        seq = ACCTS.get(acct_no, -1)
        if seq == -1:
            ACCTS[acct_no] = 1
            seq = 1
        else:
            seq += 1
            ACCTS[acct_no] = seq
        acct_no = str(seq) + str(acct_no)
        record.append(acct_no)
        # 客户名称
        customer_name = row[2].encode("gb2312")
        record.append(customer_name)
        # 余额
        curr_bal = is_legal_number(row, row[3], 18, 3, exception_file, "余额错误")
        if curr_bal == -1:
            is_legal = 0
        record.append(curr_bal)
        # 账户状态
        acct_stat = is_legal_number(row, row[4], 2, 0, exception_file, "账户状态错误")
        if acct_stat == -1:
            is_legal = 0
        record.append(acct_stat)
        # 资金来源种类
        fund_type = "01"
        record.append(fund_type)
        # 是否计息
        is_calc_int = str(row[6]).upper()
        record.append(is_calc_int)
        # 利率标识
        rate_ind = str(row[8]).upper()
        record.append(rate_ind)
        # 利率
        rate = is_legal_number(row, row[9], 9, 6, exception_file, "利率错误")
        if rate == -1:
            is_legal = 0
        record.append(rate)
        # 已到期账号定期利息
        maturity_int = is_legal_number(row, row[10], 18, 5, exception_file, "到期利息错误")
        if maturity_int == -1:
            is_legal = 0
        record.append(maturity_int)
        # 起息日期
        int_form_date = is_legal_char(row, row[11], 8, exception_file, "起息日期错误")
        if int_form_date == -1:
            is_legal = 0
        record.append(int_form_date)
        # 止息日期
        int_to_date = is_legal_char(row, row[12], 8, exception_file, "止息日期错误")
        if int_to_date == -1:
            is_legal = 0
        record.append(int_to_date)
        # 存期
        term_period = is_legal_number(row, row[13], 3, 0, exception_file, "存期错误")
        if term_period == -1:
            is_legal = 0
        record.append(term_period)
        # 定期到期日
        term_maturity_date = is_legal_char(row, row[14], 8, exception_file, "定期到期日错误")
        if term_maturity_date == -1:
            is_legal = 0
        record.append(term_maturity_date)
        # 转存标志
        try:
            rollover_flag = str(row[15]).upper()
            if rollover_flag == "NONE":
                rollover_flag = "N"
            record.append(rollover_flag)
        except:
            except_record = row[0] + "|" + row[1] + "|" + row[15] + "|" + "转存标志错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 开户日
        open_date = is_legal_char(row, row[16], 8, exception_file, "开户日错误")
        if open_date == -1:
            is_legal = 0
        record.append(open_date)
        # 账户地址
        try:
            acct_addr = row[17].encode("gb2312")
            record.append(acct_addr)
        except:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(row[17]) + "|" + "账户地址错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 客户子类
        customer_sub_type = is_legal_char(row, row[18], 3, exception_file, "客户子类错误")
        if customer_sub_type == -1:
            is_legal = 0
        record.append(customer_sub_type)
        # 金融机构类别
        financial_inst_type = is_legal_char(row, row[19], 4, exception_file, "金融机构类别错误")
        if financial_inst_type == -1:
            is_legal = 0
        record.append(financial_inst_type)
        # 金融机构层级
        financial_inst_tier = is_legal_char(row, row[20], 4, exception_file, "金融机构层级错误")
        if financial_inst_tier == -1:
            is_legal = 0
        record.append(financial_inst_tier)
        # 联系电话
        phone_no = str(row[21]).ljust(15).replace(".", "")
        record.append(phone_no)

        if is_legal == 1:
            out_record = "|".join(record)
            out_record += "|" + str(CUST_START_NO3) + str(cust_seq)
            out_record += "\n"
            out_fin_cus_term.write(out_record)
    fin_cus_term.quit_without_save()
    exception_file.close()
    out_fin_cus_term.close()


def gen_fin_cus_saving():
    """头寸 约定活期 约定定期"""
    global ACCTS, CUST_START_NO4, bgl_inv_onrf
    juristic_customer_no = {}
    fin_cus_save = excel.Excel(unicode(r'D:\金融机构存款\金融机构汇总.xlsx', "utf-8"), "3")
    out_fin_cus_save = open(unicode(r'D:\金融机构存款\INMS1.TXT', "utf-8"),  "w")
    exception_file = open(unicode(r'D:\金融机构存款\INMS1_EXCEPTION.TXT', "utf-8"), "w")
    update_creg = open(unicode(r'D:\金融机构存款\UPDATE_CREG.sh', "utf-8"), "w")
    update_creg.write("db2 connect to $DB2_SID\n")
    update_creg.write("db2 truncate table odat immediate\n")
    update_creg.write("db2 truncate table creg immediate\n")
    update_creg.write("db2 \"import from $input/creg.del of del insert into creg\"\n")
    update_creg.write("db2 \"UPDATE CREG SET NET_AMOUNT = 0\"\n")
    cust_seq = 0
    acct_seq = 0  # 用来生成不同的旧账号
    prev_branch = ""  # 如果网点号相同序号加1，不同则从1开始
    for i in xrange(fin_cus_save.used_range(), 1, -1):
        cust_seq += 1
        record = []
        is_legal = 1
        row = fin_cus_save.get_row_data(i)
        if row[1] is None:
            continue
        # 机构号
        old_branch = is_legal_char(row, row[0], 8, exception_file, "机构号错误")
        if old_branch == -1:
            is_legal = 0
        new_branch = get_new_branch(str(int(row[0])))
        if new_branch == -1:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(int(row[0])) + "|" + "新机构号未找到" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        new_branch = str(new_branch[:4]) + "0"
        record.append(str(new_branch).encode("utf-8"))
        # 账号
        acct_no = is_legal_char(row, row[1], 21, exception_file, "账号错误")
        orig_acct = acct_no
        if acct_no == -1:
            is_legal = 0
        seq = ACCTS.get(acct_no, -1)
        if seq == -1:
            ACCTS[acct_no] = 1
            seq = 1
        else:
            seq += 1
            ACCTS[acct_no] = seq
        acct_no = str(seq) + str(acct_no)
        record.append(acct_no)
        # 客户名称
        try:
            customer_name = row[2].encode("gb2312")
            record.append(customer_name)
        except:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(row[2]) + "|" + "客户名称错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 余额
        curr_bal = is_legal_number(row, row[3], 18, 3, exception_file, "余额错误")
        if curr_bal == -1:
            is_legal = 0
        record.append(curr_bal)
        orig_bal = "%.3f" % (float(float(curr_bal)/1000), )
        # 账户状态
        #acct_stat = is_legal_number(row, row[4], 2, 0, exception_file, "账户状态错误")
        #if acct_stat == -1:
        #    is_legal = 0
        record.append("00")
        # 是否计息
        #is_calc_int = str(row[5]).upper()
        record.append("Y")
        # 利率类型
        if row[6] is None:
            rate_type = "2"
        else:
            rate_type = str(int(row[6]))
        record.append(rate_type)
        # 利率
        rate = is_legal_number(row, row[7], 9, 6, exception_file, "利率错误")
        if rate == -1:
            is_legal = 0
        record.append(rate)
        # 人民币结算账户属性
        if str(int(row[8])).replace(".", "") not in ['1', '2', '3']:
            row[8] = '3'
        acct_attr = is_legal_char(row, row[8], 1, exception_file, "人民币结算账户属性错误")
        if acct_attr == -1:
            is_legal = 0
        record.append(acct_attr)
        # 开户日
        open_date = is_legal_char(row, row[9], 8, exception_file, "开户日错误")
        if open_date == -1:
            is_legal = 0
        record.append(open_date)
        # 账户地址
        try:
            acct_addr = row[10].encode("gb2312")
            record.append(acct_addr)
        except:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(row[10]) + "|" + "账户地址错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 客户子类
        customer_sub_type = is_legal_char(row, row[11], 3, exception_file, "客户子类错误")
        if customer_sub_type == -1:
            is_legal = 0
        record.append(customer_sub_type)
        # 金融机构类别
        financial_inst_type = is_legal_char(row, row[12], 4, exception_file, "金融机构类别错误")
        if financial_inst_type == -1:
            is_legal = 0
        record.append(financial_inst_type)
        # 金融机构层级
        #financial_inst_tier = is_legal_char(row, row[13], 4, exception_file, "金融机构层级错误")
        #if financial_inst_tier == -1:
        #    is_legal = 0
        record.append("3001")
        # 联系电话
        #phone_no = str(row[14]).ljust(15).replace(".", "")
        record.append("999999999")
        # 产品类型
        product = str(int(row[15]))
        record.append(product)
        bgl_inv_onrf.write("db2 -x \"select \'" + old_branch + "\',\'" + orig_acct.rstrip() + "\',check_digit(left(intn_ref_no,16))," + "\'" + orig_bal + "\'," + "\'" + customer_name + "\' from xref where inst_no = \'003\'"
                                                                "and extn_ref_no = \'63" + acct_no.rstrip() + "\'\" >> old_acct_onrf.txt\n")
        if product == '13010104':
            juristic_customer_no[old_branch] = str(CUST_START_NO4) + str(cust_seq)
        if product == "13010101":
            creg_bal = "%.3f" % (float(float(curr_bal)/1000), )
            update_creg.write("db2 \"UPDATE CREG SET VOSTRO_LAST_BAL = " + str(creg_bal) +
                          " WHERE CLEARING_BRANCH = \'" + new_branch + "\'\"\n")
            update_creg.write("db2 \"UPDATE CREG SET VOSTRO_ACCT = (SELECT INTN_REF_NO FROM XREF WHERE INST_NO = \'003\' AND"
                          " EXTN_REF_NO = \'63" + acct_no.strip() + "\') WHERE CLEARING_BRANCH = \'" + new_branch + "\'\"\n")
            update_creg.write("db2 \"INSERT INTO ODAT VALUES (\'003\',(SELECT INTN_REF_NO FROM XREF WHERE "
                              "INST_NO = \'003\' AND EXTN_REF_NO = \'63" + acct_no.strip() + "\'),0,0)\"\n")
        int_accr = is_legal_number(row, row[16], 18, 5, exception_file, "应计利息错误")
        record.append(int_accr)
        if is_legal == 1:
            record[0] = "01000"
            if product != '13010101':
                record[0] = "01001"
            out_record = "|".join(record)
            out_record += "|" + str(CUST_START_NO4) + str(cust_seq)
            out_record += "\n"
            out_fin_cus_save.write(out_record)
    update_creg.write("db2 \"UPDATE CREG SET NOSTRO_LAST_BAL = VOSTRO_LAST_BAL * -1\"\n")
    update_creg.write("db2 \"UPDATE CREG SET CURRENT_BAL = VOSTRO_LAST_BAL\"\n")
    update_creg.close()
    fin_cus_save.quit_without_save()
    exception_file.close()
    out_fin_cus_save.close()


def gen_cop_cus_saving():
    """同业活期 保证金 待结算财政款项"""
    global ACCTS, CUST_START_NO, bgl_inv_onrf
    cop_cus_save = excel.Excel(unicode(r'D:\金融机构存款\金融机构汇总.xlsx', "utf-8"), "1")
    out_cop_cus_save = open(unicode(r'D:\金融机构存款\INMS2.TXT', "utf-8"),  "w")
    out_cop_save_cus_info = open(unicode(r'D:\金融机构存款\SAVING_CUS_INFO.TXT', "utf-8"),  "w")
    exception_file = open(unicode(r'D:\金融机构存款\INMS2_EXCEPTION.TXT', "utf-8"), "w")
    cust_seq = 0  # 用来生成不同的客户号
    for i in xrange(cop_cus_save.used_range(), 1, -1):
        record = []
        cust_seq += 1
        is_legal = 1
        row = cop_cus_save.get_row_data(i)
        if row[1] is None:
            continue
        # 机构号
        old_branch = is_legal_char(row, row[0], 8, exception_file, "机构号错误")
        if old_branch == -1:
            is_legal = 0
        new_branch = get_new_branch(str(int(row[0])))
        if new_branch == -1:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(int(row[0])) + "|" + "新机构号未找到" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        record.append(str(new_branch).encode("utf-8"))
        # 账号
        acct_no = is_legal_char(row, row[1], 21, exception_file, "账号错误")
        orig_acct = acct_no
        if acct_no == -1:
            is_legal = 0
        seq = ACCTS.get(acct_no, -1)
        if seq == -1:
            ACCTS[acct_no] = 1
            seq = 1
        else:
            seq += 1
            ACCTS[acct_no] = seq
        acct_no = str(seq) + str(acct_no)
        record.append(acct_no)
        # 客户名称
        customer_name = row[2].encode("gb2312")
        record.append(customer_name)
        # 余额
        curr_bal = is_legal_number(row, row[3], 18, 3, exception_file, "余额错误")
        if curr_bal == -1:
            is_legal = 0
        record.append(curr_bal)
        orig_bal = "%.3f" % (float(float(curr_bal)/1000), )
        # 产品代码
        product = is_legal_char(row, row[4], 8, exception_file, "产品代码错误处")
        if product == -1:
            is_legal = 0
        record.append(product)
        # 账户状态
        #acct_stat = is_legal_number(row, row[5], 2, 0, exception_file, "账户状态错误")
        #if acct_stat == -1:
        #    is_legal = 0
        record.append("00")
        # 是否计息
        #is_calc_int = str(row[7]).upper()
        record.append("Y")
        # 利率类型
        rate_type = str(int(row[8]))
        if product == '12690103':
            record.append("1")
        else:
            record.append(rate_type)
        # 利率
        rate = is_legal_number(row, row[9], 9, 6, exception_file, "利率错误")
        if rate == -1:
            is_legal = 0
        if product == "12690103":
            record.append("0" * 9)
        else:
            record.append(rate)
        # 人民币结算账户属性
        #acct_attr = is_legal_char(row, row[10], 1, exception_file, "人民币结算账户属性错误")
        #if acct_attr == -1:
        #    is_legal = 0
        record.append("3")
        # 开户许可证编号
        #open_acct_seq_no = str(row[11]).replace(".", "")
        record.append("9" * 20)
        # 核准日期
        open_date = is_legal_char(row, row[13], 8, exception_file, "核准日错误")
        if open_date == -1:
            is_legal = 0
        record.append(open_date)
        # 账户启用日期
        acct_use_date = is_legal_char(row, row[13], 8, exception_file, "启用日期日错误")
        if acct_use_date == -1:
            is_legal = 0
        record.append(acct_use_date)
        # 核准号
        #appr_no = str(row[14]).replace(".", "")
        record.append("9" * 20)
        # 账户地址
        try:
            acct_addr = row[15].encode("gb2312")
            record.append(acct_addr)
        except:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + row[15] + "|" + "账户地址错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 行业分类
        industry_code = "Y9999"
        record.append(industry_code)
        # 企业性质
        bus_owsp = str(row[17]).upper()
        record.append(bus_owsp)
        # 企业经济成分
        ecnm_code = str(int(row[18])).replace(".", "")
        record.append(ecnm_code)
        # 法人代表姓名
        boss_name = row[19].encode("gb2312")
        record.append(boss_name)
        # 法人代表证件类型
        boss_id_type = is_legal_number(row, row[20], 2, 0, exception_file, "法人代表证件类型错误")
        record.append(boss_id_type)
        # 法人代表证件号码
        boss_id = is_legal_char(row, row[21], 32, exception_file, "法人代表证件号码错误")
        if boss_id == -1:
            is_legal = 0
        record.append(boss_id)
        # 法人代表证件到期日
        boss_id_expiry_date = is_legal_char(row, row[22], 8, exception_file, "法人代表证件到期日错误")
        if boss_id_expiry_date == -1:
            is_legal = 0
        record.append(boss_id_expiry_date)
        # 对公客户证件类型
        id_type = is_legal_char(row, row[23], 2, exception_file, "对公客户证件类型错误")
        if id_type == -1:
            is_legal = 0
        record.append(id_type)
        # 对公客户证件号码
        try:
            id_no = str(int(row[24]))
        except:
            id_no = row[24].encode("utf-8")
        record.append(id_no)
        # 对公账户证件到期日
        id_expiry_date = is_legal_char(row, row[25], 8, exception_file, "对公账户证件到期日错误")
        if id_expiry_date == -1:
            is_legal = 0
        record.append(id_expiry_date)
        # 联系电话
        #phone_no = str(row[27]).ljust(15).replace(".", "")
        record.append("99999999")
        # 应计利息
        if product == "12690103":
            record.append("0" * 18)
        else:
            int_available = is_legal_number(row, row[28],18, 5, exception_file, "应计利息错误")
            record.append(int_available)
        bgl_inv_onrf.write("db2 -x \"select \'" + old_branch + "\',\'" + orig_acct.rstrip() + "\',check_digit(left(intn_ref_no,16))," + "\'" + orig_bal + "\'," + "\'" + customer_name + "\' from xref where inst_no = \'003\'"
                                                                    "and extn_ref_no = \'63" + acct_no.rstrip() + "\'\" >> old_acct_onrf.txt\n")
        customer_no = str(CUST_START_NO) + str(cust_seq)
        if is_legal == 1:
            out_record = "|".join(record)
            out_record += "|" + customer_no
            out_record += "\n"
            out_cop_save_cus_info.write(out_record)
        if is_legal == 1:
            out_record = "|".join(record)
            out_record += "|" + customer_no
            out_record += "\n"
            out_cop_cus_save.write(out_record)
    cop_cus_save.quit_without_save()
    exception_file.close()
    out_cop_cus_save.close()


def gen_cop_cus_term():
    """他行存本行对公客户定期"""
    global ACCTS, bgl_inv_onrf
    cop_cus_term = excel.Excel(unicode(r'D:\金融机构存款\金融机构汇总.xlsx', "utf-8"), "2")
    out_cop_cus_term = open(unicode(r'D:\金融机构存款\INMT2.TXT', "utf-8"),  "w")
    out_cop_term_cus_info = open(unicode(r'D:\金融机构存款\TERM_CUS_INFO.TXT', "utf-8"),  "w")
    exception_file = open(unicode(r'D:\金融机构存款\INMT2_EXCEPTION.TXT', "utf-8"), "w")
    cust_seq = 0  # 用来生成不同的客户号
    prev_id_no = ""
    prev_id_type = ""
    prev_customer_no = ""
    for i in xrange(cop_cus_term.used_range(), 1, -1):
        cust_seq += 1
        record = []
        is_legal = 1
        row = cop_cus_term.get_row_data(i)
        if row[1] is None:
            continue
        # 机构号
        old_branch = is_legal_char(row, row[0], 8, exception_file, "机构号错误")
        if old_branch == -1:
            is_legal = 0
        new_branch = get_new_branch(str(int(row[0])))
        if new_branch == -1:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + str(int(row[0])) + "|" + "新机构号未找到" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        record.append(str(new_branch).encode("utf-8"))
        # 账号
        acct_no = is_legal_char(row, row[1], 21, exception_file, "账号错误")
        orig_acct = acct_no
        if acct_no == -1:
            is_legal = 0
        seq = ACCTS.get(acct_no, -1)
        if seq == -1:
            ACCTS[acct_no] = 1
            seq = 1
        else:
            seq += 1
            ACCTS[acct_no] = seq
        acct_no = str(seq) + str(acct_no)
        record.append(acct_no)
        # 产品代码
        product = is_legal_char(row, row[2], 8, exception_file, "产品代码错误")
        if product == -1:
            is_legal = 0
        record.append(product)
        # 客户名称
        customer_name = row[3].encode("gb2312")
        record.append(customer_name)
        # 余额
        curr_bal = is_legal_number(row, row[4], 18, 3, exception_file, "余额错误")
        if curr_bal == -1:
            is_legal = 0
        record.append(curr_bal)
        orig_bal = "%.3f" % (float(float(curr_bal)/1000), )
        # 账户状态
        acct_stat = "00"
        record.append(acct_stat)
        # 资金来源种类
        fund_type = "01"
        record.append(fund_type)
        # 是否计息
        #is_calc_int = str(row[7]).upper()
        record.append("Y")
        # 利率标识
        rate_ind = str(row[9]).upper()
        record.append(rate_ind)
        # 利率
        rate = is_legal_number(row, row[10], 9, 6, exception_file, "利率错误")
        if rate == -1:
            is_legal = 0
        record.append(rate)
        # 已到期账号定期利息
        maturity_int = is_legal_number(row, row[11], 18, 5, exception_file, "到期利息错误")
        if maturity_int == -1:
            is_legal = 0
        record.append(maturity_int)
        # 起息日期
        int_form_date = is_legal_char(row, row[12], 8, exception_file, "起息日期错误")
        if int_form_date == -1:
            is_legal = 0
        record.append(int_form_date)
        # 止息日期
        int_to_date = is_legal_char(row, row[13], 8, exception_file, "止息日期错误")
        if int_to_date == -1:
            is_legal = 0
        record.append(int_to_date)
        # 存期
        term_period = is_legal_number(row, row[14], 3, 0, exception_file, "存期错误")
        if term_period == -1:
            is_legal = 0
        record.append(term_period)
        # 转存标志
        try:
            rollover_flag = str(row[15]).upper()
            record.append(rollover_flag)
        except:
            except_record = row[0] + "|" + row[1] + "|" + row[15] + "|" + "转存标志错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 账户地址
        try:
            acct_addr = row[17].encode("gb2312")
            record.append(acct_addr)
        except:
            except_record = str(int(row[0])) + "|" + str(int(row[1])) + "|" + row[17] + "|" + "账户地址错误" + "\n"
            exception_file.write(except_record)
            is_legal = 0
        # 行业分类
        industry_code = str(row[18]).replace(".", "")
        record.append(industry_code)
        # 企业性质
        bus_owsp = str(row[19]).upper()
        record.append(bus_owsp)
        # 企业经济成分
        ecnm_code = str(int(row[20])).replace(".", "")
        record.append(ecnm_code)
        # 法人代表姓名
        boss_name = row[21].encode("gb2312")
        record.append(boss_name)
        # 法人代表证件类型
        boss_id_type = is_legal_number(row, row[22], 2, 0, exception_file, "法人代表证件类型错误")
        record.append(boss_id_type)
        # 法人代表证件号码
        boss_id = is_legal_char(row, row[23], 32, exception_file, "法人代表证件号码错误")
        if boss_id == -1:
            is_legal = 0
        record.append(boss_id)
        # 法人代表证件到期日
        boss_id_expiry_date = is_legal_char(row, row[24], 8, exception_file, "法人代表证件到期日错误")
        if boss_id_expiry_date == -1:
            is_legal = 0
        record.append(boss_id_expiry_date)
        # 对公客户证件类型
        id_type = is_legal_char(row, row[25], 2, exception_file, "对公客户证件类型错误")
        if id_type == -1:
            is_legal = 0
        record.append(id_type)
        # 对公客户证件号码
        id_no = row[26].encode("utf-8")
        record.append(id_no)
        # 对公账户证件到期日
        id_expiry_date = is_legal_char(row, row[27], 8, exception_file, "对公账户证件到期日错误")
        if id_expiry_date == -1:
            is_legal = 0
        record.append(id_expiry_date)
        bgl_inv_onrf.write("db2 -x \"select \'" + old_branch + "\',\'" + orig_acct.rstrip() + "\',check_digit(left(intn_ref_no,16))," + "\'" + orig_bal + "\'," + "\'" + customer_name + "\' from xref where inst_no = \'003\'"
                                                                    "and extn_ref_no = \'63" + acct_no.rstrip() + "\'\" >> old_acct_onrf.txt\n")
        customer_no = str(CUST_START_NO2) + str(cust_seq)
        out_record = "|".join(record)
        out_record += "|" + customer_no
        out_record += "\n"
        out_cop_term_cus_info.write(out_record)
        if is_legal == 1:
            out_record = "|".join(record)
            out_record += "|" + customer_no
            out_record += "\n"
            out_cop_cus_term.write(out_record)
    cop_cus_term.quit_without_save()
    exception_file.close()
    out_cop_cus_term.close()


def gen_term_record():
    """生成对公客户和金融机构客户的ONRF INMT5"""
    term_inmt5 = open(unicode(r'D:\金融机构存款\PINMT6.TXT', "utf-8"),  "w")
    term_onrf = open(unicode(r'D:\金融机构存款\TERM_ONRF.TXT', "utf-8"),  "w")
    # 金融机构定期
    fin_term_file = open(unicode(r'D:\金融机构存款\INMT1.TXT', "utf-8"),  "r")
    for line in fin_term_file.readlines():
        acct_info = {}
        line = line[:-1]
        record = line.split("|")
        acct_info["branch"] = record[0]
        acct_info["acct_no"] = record[1]
        acct_info["acct_name"] = record[2]
        acct_info["curr_bal"] = record[3]
        acct_info["acct_stat"] = record[4]
        acct_info["fund_type"] = record[5]
        acct_info["is_calc_int"] = record[6]
        acct_info["rate_ind"] = record[7]
        acct_info["rate"] = record[8]
        acct_info["maturity_int"] = record[9]
        acct_info["int_from_date"] = record[10]
        acct_info["int_to_date"] = record[11]
        acct_info["term_period"] = record[12]
        acct_info["term_maturity_date"] = record[13]
        acct_info["rollover_flag"] = record[14]
        acct_info["open_date"] = record[15]
        acct_info["customer_no"] = record[21]
        acct_info["product"] = "13210101"
        onrf_record = gen_onrf(acct_info)
        term_acct_info = gen_term_info(acct_info)
        term_onrf.write(onrf_record + "\n")
        term_inmt5.write(term_acct_info + "\n")
    fin_term_file.close()

    # 对公客户定期
    fin_term_file = open(unicode(r'D:\金融机构存款\INMT2.TXT', "utf-8"),  "r")
    for line in fin_term_file.readlines():
        acct_info = {}
        line = line[:-1]
        record = line.split("|")
        acct_info["branch"] = record[0]
        acct_info["acct_no"] = record[1]
        acct_info["product"] = record[2]
        acct_info["acct_name"] = record[3]
        acct_info["curr_bal"] = record[4]
        acct_info["acct_stat"] = record[5]
        acct_info["fund_type"] = record[6]
        acct_info["is_calc_int"] = record[7]
        acct_info["rate_ind"] = record[8]
        acct_info["rate"] = record[9]
        acct_info["maturity_int"] = record[10]
        acct_info["int_from_date"] = record[11]
        acct_info["int_to_date"] = record[12]
        acct_info["term_period"] = record[13]
        acct_info["term_maturity_date"] = record[12]
        acct_info["rollover_flag"] = record[14]
        acct_info["open_date"] = record[11]
        acct_info["customer_no"] = record[26]
        onrf_record = gen_onrf(acct_info)
        term_acct_info = gen_term_info(acct_info)
        term_onrf.write(onrf_record + "\n")
        term_inmt5.write(term_acct_info + "\n")
    fin_term_file.close()
    term_onrf.close()
    term_inmt5.close()


def gen_save_record():
    """生成对公客户和金融机构客户活期的 ONRF INMT5"""
    save_onrf = open(unicode(r'D:\金融机构存款\SAVE_ONRF.TXT', "utf-8"),  "w")
    save_inms5 = open(unicode(r'D:\金融机构存款\PINMS6.TXT', "utf-8"),  "w")

    # 金融机构活期
    fin_save_file = open(unicode(r'D:\金融机构存款\INMS1.TXT', "utf-8"),  "r")
    for line in fin_save_file.readlines():
        acct_info = {}
        line = line[:-1]
        record = line.split("|")
        acct_info["branch"] = record[0]
        acct_info["acct_no"] = record[1]
        acct_info["acct_name"] = record[2]
        acct_info["curr_bal"] = record[3]
        acct_info["acct_stat"] = record[4]
        acct_info["is_calc_int"] = record[5]
        acct_info["rate_type"] = record[6]
        acct_info["rate"] = record[7]
        acct_info["acct_attr"] = record[8]
        acct_info["open_date"] = record[9]
        acct_info["acct_addr"] = record[10]
        acct_info["customer_no"] = record[17]
        acct_info["product"] = record[15]
        acct_info["int_accr"] = record[16]
        onrf_record = gen_onrf(acct_info)
        term_acct_info = gen_save_info(acct_info)
        save_onrf.write(onrf_record + "\n")
        save_inms5.write(term_acct_info + "\n")
    fin_save_file.close()

    # 对公客户活期
    cop_save_file = open(unicode(r'D:\金融机构存款\INMS2.TXT', "utf-8"),  "r")
    for line in cop_save_file.readlines():
        acct_info = {}
        line = line[:-1]
        record = line.split("|")
        acct_info["branch"] = record[0]
        acct_info["acct_no"] = record[1]
        acct_info["acct_name"] = record[2]
        acct_info["curr_bal"] = record[3]
        acct_info["product"] = record[4]
        acct_info["acct_stat"] = record[5]
        acct_info["is_calc_int"] = record[6]
        acct_info["rate_type"] = record[7]
        acct_info["rate"] = record[8]
        acct_info["acct_attr"] = record[9]
        acct_info["open_acct_seq_no"] = record[10]
        acct_info["appr_date"] = record[11]
        acct_info["appr_no"] = record[13]
        acct_info["open_date"] = record[12]
        acct_info["acct_addr"] = record[14]
        acct_info["int_accr"] = record[26]
        acct_info["customer_no"] = record[27]
        onrf_record = gen_onrf(acct_info)
        term_acct_info = gen_save_info(acct_info)
        save_onrf.write(onrf_record + "\n")
        save_inms5.write(term_acct_info + "\n")
    fin_save_file.close()


def gen_cus_record():
    global FIN_CUST_INFO
    cino_file = open(unicode(r'D:\金融机构存款\PCINO.TXT', "utf-8"),  "w")
    cif_file = open(unicode(r'D:\金融机构存款\PCIF.TXT', "utf-8"),  "w")
    adnm_file = open(unicode(r'D:\金融机构存款\PADNM.TXT', "utf-8"),  "w")

    ## 金融机构客户定期
    #out_fin_term_cus_info = open(unicode(r'D:\金融机构存款\INMT1.TXT', "utf-8"),  "r")
    #for line in out_fin_term_cus_info.readlines():
    #    line = line[:-1]
    #    record = line.split("|")
    #    FIN_CUST_INFO["customer_no"] = record[21]
    #    FIN_CUST_INFO["fin_type"] = record[18]
    #    FIN_CUST_INFO["fin_tier"] = record[19]
    #    FIN_CUST_INFO["branch_no"] = record[0]
    #    cino_record, cif_record, adnm_record1, adnm_record2 = gen_cust_record(FIN_CUST_INFO)
    #    cino_file.write(cino_record + "\n")
    #    cif_file.write(cif_record + "\n")
    #    adnm_file.write(adnm_record1 + "\n")
    #    adnm_file.write(adnm_record2 + "\n")
    #out_fin_term_cus_info.close()

    # 金融机构客户活期
    out_fin_sav_cus_info = open(unicode(r'D:\金融机构存款\INMS1.TXT', "utf-8"),  "r")
    for line in out_fin_sav_cus_info.readlines():
        line = line[:-1]
        record = line.split("|")
        #if record[15] != '13010104':
        #    continue
        FIN_CUST_INFO["customer_no"] = record[17]
        FIN_CUST_INFO["fin_type"] = record[12]
        FIN_CUST_INFO["fin_tier"] = record[13]
        FIN_CUST_INFO["branch_no"] = record[0]
        FIN_CUST_INFO["cust_addr"] = record[10]
        FIN_CUST_INFO["fin_cust_name"] = record[2]
        cino_record, cif_record, adnm_record1, adnm_record2 = gen_cust_record(FIN_CUST_INFO)
        cino_file.write(cino_record + "\n")
        cif_file.write(cif_record + "\n")
        adnm_file.write(adnm_record1 + "\n")
        adnm_file.write(adnm_record2 + "\n")
    out_fin_sav_cus_info.close()

    # 对公活期客户
    out_cop_save_cus_info = open(unicode(r'D:\金融机构存款\SAVING_CUS_INFO.TXT', "utf-8"),  "r")
    for line in out_cop_save_cus_info.readlines():
        cust_info = {}
        line = line[:-1]
        record = line.split("|")
        cust_info["customer_no"] = record[27]
        cust_info["id_no"] = record[23]
        cust_info["id_type"] = record[22]
        cust_info["cust_type"] = "02"
        cust_info["id_expiry_date"] = record[24]
        cust_info["branch_no"] = record[0]
        cust_info["cop_cust_name"] = record[2]
        cust_info["industry_code"] = record[15]
        cust_info["bus_owsp"] = record[16]
        cust_info["ecnm_code"] = record[17]
        cust_info["cop_per_name"] = record[18]
        cust_info["cop_per_id_type"] = record[19]
        cust_info["cop_per_id"] = record[20]
        cust_info["boss_name"] = record[18]
        cust_info["cust_addr"] = record[14]
        cino_record, cif_record, adnm_record1, adnm_record2 = gen_cust_record(cust_info)
        cino_file.write(cino_record + "\n")
        cif_file.write(cif_record + "\n")
        adnm_file.write(adnm_record1 + "\n")
        adnm_file.write(adnm_record2 + "\n")
    out_cop_save_cus_info.close()

    # 对公定期客户
    out_cop_term_cus_info = open(unicode(r'D:\金融机构存款\TERM_CUS_INFO.TXT', "utf-8"),  "r")
    for line in out_cop_term_cus_info.readlines():
        cust_info = {}
        line = line[:-1]
        record = line.split("|")
        cust_info["customer_no"] = record[26]
        cust_info["id_no"] = record[24]
        cust_info["id_type"] = record[23]
        cust_info["cust_type"] = "02"
        cust_info["id_expiry_date"] = record[25]
        cust_info["branch_no"] = record[0]
        cust_info["cop_cust_name"] = record[3]
        cust_info["industry_code"] = record[16]
        cust_info["bus_owsp"] = record[17]
        cust_info["ecnm_code"] = record[18]
        cust_info["cop_per_name"] = record[19]
        cust_info["cop_per_id_type"] = record[20]
        cust_info["cop_per_id"] = record[21]
        cust_info["boss_name"] = record[19]
        cust_info["cust_addr"] = record[15]
        cino_record, cif_record, adnm_record1, adnm_record2 = gen_cust_record(cust_info)
        cino_file.write(cino_record + "\n")
        cif_file.write(cif_record + "\n")
        adnm_file.write(adnm_record1 + "\n")
        adnm_file.write(adnm_record2 + "\n")
    out_cop_term_cus_info.close()


# 对补录文件进行预处理，不合格的生成例外报表
gen_cop_cus_saving()
gen_cop_cus_term()
gen_fin_cus_term()
gen_fin_cus_saving()


# 生成移植中间文件
gen_term_record()
gen_save_record()
gen_cus_record()