# -*- coding:utf-8 -*-
__author__ = 'qctest'

import excel

"""把补录上来的下期浮动标识补录表改为迁入程序需要的格式"""


class RateInd():
    def __init__(self):
        self.out_file = open(unicode(r'D:\浮动利率补录\INPFILE', "utf-8"),  "w")
        self.orig_file = excel.Excel(unicode(r'D:\浮动利率补录\20150417最终浮动利率生效标识', "utf-8"), "Sheet1")

    def gen_out_file(self):
        for i in xrange(self.orig_file.used_range(), 2, -1):
            row = self.orig_file.get_row_data(i)
            acct_no = str(int(row[1]))
            serial_no = str(int(row[2]))
            rate_ind = str(int(row[3]))
            self.out_file.write(acct_no + serial_no + rate_ind + "\n")

    def close_files(self):
        self.out_file.close()
        self.orig_file.quit_without_save()


rate_ind = RateInd()
rate_ind.gen_out_file()
rate_ind.close_files()