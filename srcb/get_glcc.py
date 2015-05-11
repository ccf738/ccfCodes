# -*- coding:utf-8 -*-
__author__ = 'qctest'


"""
从迁移环境拿所有报表文件，并导入到EXCEL中
生成的所有报表都在D:\mig_report\总账核对\YYYY-MM-DD HH-MM-SS\目录下
"""

import excel
import shutil
from ftplib import FTP
import os
import time

REGION = ["10.1.2.33","fnsonlmd","fnsonlmd", "/fns/md/r/data/temp/"]
# 需要导入到EXCEL的文本文件名：0EXCEL文件名 1Sheet名 2字段数 3文本文件目录 4分割符 5模板名称
FILE_LIST = {"TATANOCGL": ["TATA无CGL科目总账", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "TATAGLCC": ["TATA全量科目总账", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "TATACGL": ["TATACGL科目总账", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "TAINTEREST": ["贷款所有利息科目总账", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "TAONSHEET": ["贷款表内利息科目总账", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "TAOFFSHEET": ["贷款表外利息科目总账", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "cinexcel.csv": ["东华有TATA无", 'Sheet1', 6, 'server', '|', unicode('东华有TATA无模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "cintable.csv": ["东华无TATA有", 'Sheet1', 4, 'server', '|', unicode('GLCC模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "cinboth.csv": ["两个都有", 'Sheet1', 10, 'server', '|', unicode('两个都有模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "bgl_onrf.txt": ["内部帐对照表", 'Sheet1', 14, r'D:\bgl\\', ',', unicode('内部账对照表模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             #"term10_out.txt": ["利息资本化明细", 'Sheet1', 6, r'D:\mig_report\\', '|', unicode('资本化明细模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             #"term10_branch.txt": ["利息资本化汇总", 'Sheet1', 5, r'D:\mig_report\\', '|', unicode('资本化汇总模板.xlsx', 'utf-8'), unicode('总账核对', 'utf-8')],
             "TAX_REPORT.TXT":["利息税明细", "Sheet1", 5, "server", " ", unicode("利息税模板.xlsx", "utf-8"), unicode("分户核对","utf-8" )],
             "old_acct_onrf.txt": ["补录账号信息", "Sheet1", 5, "server", " ", unicode("补录账号信息模板.xlsx", "utf-8"), unicode("分户核对", "utf-8")],
             "DEP_REPORT.TXT": ["存款分户核对", 'Sheet1', 6, 'server', ' ', unicode('存款分户模板.xlsx', 'utf-8'), unicode('分户核对', 'utf-8')],
             "LOAN_REPORT1.TXT": ["贷款分户核对", unicode('有余额', 'utf-8'), 10, 'server', ' ', unicode('贷款分户模板.xlsx', 'utf-8'), unicode('分户核对', 'utf-8')],
             "LOAN_REPORT2.TXT": ["贷款分户核对", unicode('无余额', 'utf-8'), 10, 'server', ' ', unicode('贷款分户模板.xlsx', 'utf-8'), unicode('分户核对', 'utf-8')],
             "BGL_REPORT.TXT": ["内部账分户核对", 'Sheet1', 6, 'server', ' ', unicode('内部帐分户模板.xlsx', 'utf-8'), unicode('分户核对', 'utf-8')],
             "HOLD_REPORT.TXT": ["冻结核对表", unicode('金额冻结', 'utf-8'), 3, 'server', ' ', unicode('冻结模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             "STOP_REPORT1.TXT": ["冻结核对表", unicode('借方冻结', 'utf-8'), 2, 'server', ' ', unicode('冻结模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             "STOP_REPORT2.TXT": ["冻结核对表", unicode('账户冻结', 'utf-8'), 2, 'server', ' ', unicode('冻结模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             "LOST_REPORT1.TXT": ["挂失核对表", unicode('书面挂失', 'utf-8'), 3, 'server', ' ', unicode('挂失模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             "LOST_REPORT2.TXT": ["挂失核对表", unicode('密码挂失', 'utf-8'), 3, 'server', ' ', unicode('挂失模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             #"passlost.txt": ["挂失核对表", unicode('密码挂失明细', 'utf-8'), 7, 'server', ' ', unicode('挂失模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             #"vochlost.txt": ["挂失核对表", unicode('书面挂失明细', 'utf-8'), 12, 'server', '|', unicode('挂失模板.xlsx', 'utf-8'), unicode('风险核对', 'utf-8')],
             }
LOCAL_DIRECTORY = unicode(r'D:\mig_report\总账核对\\' + str(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())) + '\\', 'utf-8')
TEMPLATE_DIRECTORY = unicode(r'D:\mig_report\总账核对\模板\\', "utf-8")

class GetGlccFile():
    def __init__(self, region):
        self.ip = region[0]
        self.user = region[1]
        self.pwd = region[2]
        self.directory = region[3]
        try:
            self.source_region = FTP(self.ip)
            self.source_region.login(self.user, self.pwd)
            self.source_region.cwd(self.directory)
        except:
            print "connect to %s with %s,%s error" % (self.ip, self.user, self.pwd)
            exit(1)

    def get_files(self):
        os.mkdir(LOCAL_DIRECTORY)
        os.chdir(LOCAL_DIRECTORY)
        os.mkdir(unicode('分户核对', 'utf-8'))
        os.mkdir(unicode('风险核对', 'utf-8'))
        os.mkdir(unicode('总账核对', 'utf-8'))
        for gl_file in FILE_LIST.keys():
            text_directory = FILE_LIST[gl_file][3]
            text_file_name = gl_file
            # 如果文件不在服务器上，则不用去拿
            if text_directory != 'server':
                continue
            try:
                self.source_region.retrbinary("RETR " + text_file_name, open(text_file_name, 'w').write)
            except:
                print "there's no %s file in %s region,please delete the excel file after this program finished" \
                      % (text_file_name, self.ip)

    def load_to_excel(self):
        os.chdir(LOCAL_DIRECTORY)
        for key in FILE_LIST.keys():
            text_file_name = key
            excel_name = unicode(FILE_LIST[key][0], 'utf-8')
            sheet_name = FILE_LIST[key][1]
            variable_count = FILE_LIST[key][2]
            text_directory = FILE_LIST[key][3].replace('server', '')  # 服务器上的文件拿下来就在工作目录，不用加路径名
            split_char = FILE_LIST[key][4] if FILE_LIST[key][4] != ' ' else None
            template_name = FILE_LIST[key][5]
            target_directory = FILE_LIST[key][6]
            # 把模板拷贝到工作目录，以便数据导入
            target_excel = LOCAL_DIRECTORY + target_directory + '\\' + excel_name + ".xlsx"
            if not os.path.exists(target_excel):
                shutil.copy(TEMPLATE_DIRECTORY + template_name, target_excel)
            source_file = open(text_directory + text_file_name, "r")
            target_excel = excel.Excel(target_excel, sheet_name)

            # 打开源文件，把文件内容放到whole_record变量中
            file_length = 0
            whole_record = []  # 文件内容形式以列表的方式存在此变量中，以便一次性写入EXCEL中
            for line_no, line in enumerate(source_file.readlines()):
                file_length += 1
                line = line[:-1]
                record = line.split(split_char)
                if text_file_name == 'bgl_onrf.txt':
                    record[6] = record[6].decode('utf-8').encode('gb2312')
                whole_record.append(record)
            source_file.close()

            # 删除从服务器上拿下来的文本文件
            try:
                os.remove(text_file_name)
            except:
                pass

            # 导入EXCEL,设置边框， 退出EXCEL
            target_excel.set_range_value((2, 1), (file_length+1, variable_count), whole_record)
            print "已处理完 %s,%s, 文件总记录数为%d条" % (FILE_LIST[key][0], key, file_length)
            target_excel.set_range_border(target_excel.get_range([1, 1], [file_length+1, variable_count]))
            target_excel.quit()

    def disconnect(self):
        self.source_region.close()

if __name__ == "__main__":
    start_time = time.time()
    get_glcc = GetGlccFile(REGION)
    get_glcc.get_files()
    get_glcc.load_to_excel()
    get_glcc.disconnect()
    end_time = time.time()
    print "程序已跑完"
    print "生成所有报表总共用了 %.1f 分钟" % ((end_time - start_time) / 60, )