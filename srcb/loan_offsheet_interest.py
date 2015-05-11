# -*- coding:utf-8 -*-
__author__ = 'qctest'

import excel
import qh_tools

class OffsheetInterest():
    def __init__(self, path, sheet):
        self.orig_excel = excel.Excel(path, sheet)
        self.update_file = open(unicode(r'D:\贷款表外息\update_offsheet_bgl_bal.sh', 'utf-8)'), 'w')

    def generate_result_file(self):
        self.update_file.write("db2 connect to $DB2_SID\n")
        for i in xrange(self.orig_excel.used_range(), 1, -1):
            row = self.orig_excel.get_row_data(i)
            if row[0] is None:
                continue
            if row[1] == 0:
                continue
            old_branch = str(int(row[0]))
            new_branch = str(qh_tools.get_new_branch(old_branch))
            if new_branch == "-1":
                print row[0], "no new branch found"
                continue
            add_value = "%.3f" % (row[1], )
            self.update_file.write("db2 \"update gldm set cum_curr_val = cum_curr_val - " + add_value +
                            " where substr(gl_class_code,9,8)= \'01300104\' and branch = \'" + new_branch + "\'\"\n")

    def close_files(self):
        self.orig_excel.quit_without_save()
        self.update_file.close()

if __name__ == "__main__":
    from_file = OffsheetInterest(unicode(r'D:\贷款表外息\20150417表外利息', 'utf-8'), "Sheet1")
    from_file.generate_result_file()
    from_file.close_files()