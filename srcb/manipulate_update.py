# -*- coding:utf-8 -*-
__author__ = 'user'
import sqlite3
import excel


database_file = unicode(r'\\10.20.47.202\共享目录\开发文档\bancsUpdate.db', "utf-8")
table_schema = []
conn = sqlite3.connect(database_file)
cur = conn.cursor()
cur.execute("PRAGMA table_info(daily_update)")
for column in cur.fetchall():  # including column name,data type,whether or not the column can be null,default value
    table_schema.append(column[1])


operation = ''


def add_column():
    conn.execute("ALTER TABLE DAILY_UPDATE ADD COLUMN PRODUCTION_DATE TEXT")
    conn.commit()
    conn.close()


def modify():
    conn.execute("UPDATE DAILY_UPDATE SET PRODUCTION_DATE = '20140724' WHERE IR_NO = 'srcb00104831'")
    conn.commit()


def delete():
    conn.execute("delete from daily_update where issue_date = '20140723'")
    conn.commit()


#def fuzzy_select(field_value):
#    copy_tag = []
#    sql_cmd = "select file_name from daily_update where 1=1"
#    for i in range(0, len(table_schema)):
#        if field_value[i]:
#            sql_cmd += " and " + table_schema[i] + " like " + '\'%' + field_value[i] + '%\''
#    sql_cmd = "select * from daily_update where file_name in (" + sql_cmd + ") order by file_name,issue_date,production_date"
#    cur.execute(sql_cmd)
#    for ir_no, filename, file_path, issuedate, modifier, test_no, production_date in cur.fetchall():
#        print ir_no, filename, file_path, issuedate, modifier, test_no, production_date
#        copy_tag.append(ir_no)
#    sql_cmd = "select * from daily_update where production_date = 'N' and file_path like '%LIBRY%' and ir_no in ("
#    for tag in copy_tag:
#        sql_cmd += "'" + tag + "',"
#    sql_cmd += ")"
#    sql_cmd = sql_cmd.replace(",)", ")")
#    cur.execute(sql_cmd)
#    print "below are some copy books,may be need to be roll back!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#    for ir_no, filename, file_path, issuedate, modifier, test_no, production_date in cur.fetchall():
#        print ir_no, filename, file_path, issuedate, modifier, test_no, production_date


def fuzzy_select(field_value):
    copy_book_list = []
    program_list = []
    search_condition = []

    # get the date and file name for this bug updated to test region
    cur.execute("select issue_date,file_name,file_path from daily_update where ir_no = ?", (field_value[0], ))
    for uat_date, filename, file_path in cur.fetchall():
        end_date = uat_date
        if filename not in program_list and file_path == '$src':
            program_list.append(filename)

    # determine which date's version we should use to roll back for production
    for program in program_list:
        cur.execute("select max(issue_date) from  (select issue_date issue_date from daily_update where "
                    "production_date != 'N' and file_name = ?)", (program, ))
        search_date = cur.fetchone()[0]
        if end_date >= search_date:
            search_condition.append((program, end_date))
        else:
            search_condition.append((program, search_date))
    print end_date

    # print the roll back message
    for condition in search_condition:
        cur.execute("select * from daily_update where file_name = ? and issue_date <= ?",
                    (condition[0], condition[1]))
        for ir_no, filename, file_path, issuedate, modifier, test_no, production_date in cur.fetchall():
            if issuedate < end_date and production_date != 'N':
                continue
            print ir_no, filename, file_path, issuedate, modifier, test_no, production_date

    # for copy book roll back
    cur.execute("select file_name,file_Path from daily_update where file_path like '%LIBRY%' and production_date = 'N' "
                "and ir_no != ?", (field_value[0], ))
    for copy_book, _ in cur.fetchall():
        if copy_book not in copy_book_list:
            copy_book_list.append(copy_book)
    for program_name in program_list:
        program_data = open(r'C:\Documents and Settings\user\chencf1_BANCS_NB_DEV_2\vobs\BANCS_NB\r\src\\'
                            + program_name).read()
        for copy_book in copy_book_list:
            if copy_book in program_data:
                print "copy book %s need to roll back for program %s" % (copy_book, program_name)

def select(field_value):
    sql_cmd = "select * from daily_update where 1=1"
    for i in range(0, len(table_schema)):
        if field_value[i]:
            sql_cmd += " and " + table_schema[i] + "=" + '\'' + field_value[i] + '\''
    sql_cmd += ' order by issue_date'
    print sql_cmd
    cur.execute(sql_cmd)
    #for ir_no in cur.fetchall():
    #    print ir_no
    #cur.execute("select * from daily_update where production_date = 'N' ORDER BY ir_no")
    for ir_no, filename, file_path, issuedate, modifier, test_no, production_date in cur.fetchall():
        print ir_no, filename, issuedate, modifier, test_no, production_date
    #cur.execute("select * from daily_update where file_path like '%LIBRY%' ORDER BY ISSUE_DATE")
    #for ir_no, filename, file_path, issuedate, modifier, test_no, production_date in cur.fetchall():
    #    print ir_no, filename, issuedate, modifier, test_no, production_date
    #cur.execute("select distinct ir_no,production_date from daily_update  group by ir_no order by issue_date")
    #print "-"*20
    #for ir_no in cur.fetchall():
    #    print ir_no
    cur.execute("select  ir_no, issue_date from daily_update where ir_no in ('srcb00092197','srcb00097888','srcb00098693','srcb00099210','srcb00099395','srcb00099820','srcb00099873','srcb00101145','srcb00101864','srcb00103235','srcb00104026','srcb00104831') group by ir_no,issue_date order by issue_date")
    for ir in cur.fetchall():
        print ir


def insert():
    record = ('srcb00092538', 'bancs.eod.crasafm.file', '$sh', '20140318', unicode('余斌米', 'utf-8'), 'TO BE ADDED', 'N')
    conn.execute("insert into daily_update values (?,?,?,?,?, ?,?)", record)
    conn.commit()


def db_to_excel():
    row_number = 1
    qa_file = excel.Excel(unicode(r'\\10.20.47.202\共享目录\开发文档\QA file release management(format for dev).xlsx',
                                  "utf-8"),
                          'CC to QA Release Management')
    excel_file = excel.Excel(r'c:\version.xlsx', 'Sheet1')
    cur.execute("select * from daily_update where production_date = 'N'")
    for record in cur.fetchall():
        if '78800' in record[0]:
            continue
        for column_number in range(1, 8):
            excel_file.set_value(row_number, column_number, record[column_number-1])
        for i in xrange(qa_file.used_range(), 0, -1):
            if qa_file.get_cell_value(i, 1) is None:
                continue
            #print record[0], record[1]
            if qa_file.get_cell_value(i, 1).strip() == record[0] and qa_file.get_cell_value(i, 2).strip() == record[1]:
                excel_file.set_value(row_number, 8, qa_file.get_cell_value(i, 7))
                break
        row_number += 1
    excel_file.quit()
    qa_file.quit_without_save()


if __name__ == "__main__":
    #db_to_excel()
    #add_column()
    #insert()
    #modify()
    #delete()
    ###################################
    #select(['',  # IR_NO
    #        '',  # FILE_NAME
    #        '',  # FILE_PATH
    #        '20140724',  # ISSUE_DATE
    #        '',  # MODIFIER
    #        '',  # TEST_NO
    #        ''])  # PRODUCTION_DATE
    ###################################
    #fuzzy_select(['srcb00092197',  # IR_NO
    #              '',  # FILE_NAME
    #              '',  # FILE_PATH
    #              '',  # ISSUE_DATE
    #              '',  # MODIFIER
    #              '',  # TEST_NO
    #              ''])  # PRODUCTION_DATE
    ########################################
    #insert()
    cur.close()
    conn.close()