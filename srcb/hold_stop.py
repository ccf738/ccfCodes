# -*- coding:utf-8 -*-
__author__ = 'qctest'

"""处理补录的冻结明细表
生成的文件的格式位：
旧网点 8
新网点 5
账号 20
冻结类型 1 (1:全冻，2:金额冻结，3:借方冻结，4:贷方冻结)
冻结原因 2
冻结日期 8
冻结到期日 8
冻结金额 17,3
有权机关名称 60
执法人姓名 40
执法人证件名称 30
执法人证件号码 32
法律文书名称 60
通知书编号 60 """

import excel
import qh_tools


class Hold():
    def __init__(self):
        self.merged_file = open(unicode(r'D:\冻结明细\HOLD_DETAIL.TXT', "utf-8"),  "w")
        self.exp_file = open(unicode(r'D:\冻结明细\HOLD_EXP.TXT', "utf-8"),  "w")


    def handle_stop(self, stop_file, hold_type):
        """账户冻结"""
        for i in xrange(stop_file.used_range(), 1, -1):
            hold_record = []
            row = stop_file.get_row_data(i)
            # 旧网点
            old_branch = str(int(row[0]))
            hold_record.append(old_branch)
            # 新网点
            new_branch = qh_tools.get_new_branch(old_branch)
            hold_record.append(str(new_branch))
            # 账号
            acct_no = qh_tools.is_legal_char(row, row[1], 20, self.exp_file, "acct not right")
            hold_record.append(acct_no)
            # 冻结类型
            hold_record.append(hold_type)
            # 冻结原因
            hold_reason = qh_tools.is_legal_number(row, row[2], 2, 0, self.exp_file, "hold reason not right")
            hold_record.append(hold_reason)
            # 冻结日期
            hold_date = qh_tools.is_legal_char(row, row[3], 8, self.exp_file, "hold date not right")
            hold_record.append(hold_date)
            # 冻结到期日
            hold_to_date = qh_tools.is_legal_char(row, row[4], 8, self.exp_file, "hold to date not right")
            hold_record.append(hold_to_date)
            # 冻结金额
            hold_val = qh_tools.is_legal_number(row, row[5], 17, 3, self.exp_file, "hold val not right")
            hold_record.append(hold_val)
            # 有权机关名称
            try:
                government_agency = row[6].encode("gb2312").ljust(60)
            except:
                government_agency = ' ' * 60
            hold_record.append(government_agency)
            # 执法人姓名
            try:
                low_enfore_officer = row[7].encode("gb2312").ljust(40)
            except:
                low_enfore_officer = ' ' * 40
            hold_record.append(low_enfore_officer)
            # 执法人证件名称
            try:
                officer_id_name = row[8].encode("gb2312").ljust(30)
            except:
                officer_id_name = ' ' * 30
            hold_record.append(officer_id_name)
            # 执法人证件号码
            try:
                officer_id_no = row[9].encode("gb2312").ljust(32)
            except:
                officer_id_no = ' ' * 32
            hold_record.append(officer_id_no)
            # 法律文书名称
            try:
                legal_doc_name = row[10].encode("gb2312").ljust(60)
            except:
                legal_doc_name = ' ' * 60
            hold_record.append(legal_doc_name)
            # 通知书编号
            try:
                notice_no = row[11].encode("gb2312").ljust(60)
            except:
                notice_no = ' ' * 60
            hold_record.append(notice_no)

            # 写入冻结文件
            self.merged_file.write("".join(hold_record) + "\n")
            # 关闭excel
        stop_file.quit_without_save()

    def close_files(self):
        self.merged_file.close()
        self.exp_file.close()

if __name__ == "__main__":
    hold = Hold()
    hold.handle_stop(excel.Excel(unicode(r'D:\冻结明细\冻结明细表', "utf-8"), "Sheet1"), "1")
    hold.handle_stop(excel.Excel(unicode(r'D:\冻结明细\冻结明细表', "utf-8"), "Sheet2"), "2")
    hold.handle_stop(excel.Excel(unicode(r'D:\冻结明细\冻结明细表', "utf-8"), "Sheet3"), "3")
    hold.handle_stop(excel.Excel(unicode(r'D:\冻结明细\冻结明细表', "utf-8"), "Sheet4"), "4")
    hold.close_files()
