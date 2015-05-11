# -*- coding:utf-8 -*-
__author__ = 'user'
import os
import shutil
import stat
import excel
import time
import win32com.client
import sqlite3
from ftplib import FTP
import telnetlib


today_date = str(time.strftime("%Y%m%d", time.localtime()))
base_version_excel = unicode(r'C:\Documents and Settings\user\桌面\上版邮件附件\新一代系统上版申请表【BANCS】【20130814】.xls', "utf-8")
base_code_list_excel = unicode(r'C:\Documents and Settings\user\桌面\上版邮件附件\20130814版本清单.xlsx', "utf-8")
# below 2 file are not important,because no one needs them,but I still need to prepare
unimportant_code_list = unicode(r'C:\Documents and Settings\user\桌面\上版邮件附件\20130814版本清单.xlsx', "utf-8")
unimportant_test_case = unicode(r'C:\Documents and Settings\user\桌面\上版邮件附件\端到端测试版本提交记录_新核心项目组_20130814 第二轮端到端基准版本.xls', "utf-8")
ir_seq = []  # to make sure A region's seq is the same as the excel's
need_compile = []  # this is to decide which copy book need to use cpbookcompile
local_base_dir = r'c:\good\cobol\update\\'
require_no = {'srcb00105214': 'srcb00091055 ',
              'srcb00105550': 'srcb00094712 ',
              'srcb00104079': 'srcb00101992 ',
              'srcb00098373': 'srcb00089644 ',
              'srcb00097305': 'srcb00097208 '}
bug_description = {'srcb00105214': unicode('修改bafe网关接口，使其支持货币兑换报文.', 'utf-8'),
                   'srcb00105550': unicode('补充自贸区账户种类要新增个FTF账户', 'utf-8'),
                   'srcb00104079': unicode('003260-现金结清销户，个人活期一本通下美元子账户，有转息账户，并且都已短信签约，销户成功后短信平台无记录', 'utf-8'),
                   'srcb00098373': unicode('trickle feed 交易报错,程序遗漏', 'utf-8'),
                   'srcb00097305': unicode('关于配合远程集中授权系统调整综合前端及核心授权点的需求', 'utf-8')}
database_file = unicode(r'\\10.20.47.202\共享目录\开发文档\bancsUpdate.db', "utf-8")
conn = sqlite3.connect(database_file)
#conn.execute('''CREATE TABLE IF NOT EXISTS DAILY_UPDATE (
#             IR_NO TEXT,
#             FILE_NAME TEXT,
#             FILE_PATH TEXT,
#             ISSUE_DATE TEXT,
#             MODIFIER TEXT
#             TEST_NO TEXT
#             PRODUCTION_DATE TEXT
#             )''')
#conn.execute('''CREATE INDEX  IF NOT EXISTS UPDATE_PK1
#                ON DAILY_UPDATE (IR_NO,ISSUE_DATE)''')
#conn.execute('''CREATE UNIQUE INDEX  IF NOT EXISTS UPDATE_PK2
#                ON DAILY_UPDATE (IR_NO,FILE_NAME)''')
conn.execute("DELETE FROM DAILY_UPDATE WHERE ISSUE_DATE = ?", (today_date,))
#conn.commit()


def insert_record(record):
    conn.executemany("INSERT INTO DAILY_UPDATE VALUES (?, ?, ?, ?, ?, ?, ?)", record)


def make_writable(path):
    if os.path.exists(path):
        os.chmod(path, stat.S_IWRITE)
        for root, dirs, files in os.walk(path):
            for fname in files:
                full_path = os.path.join(root, fname)
                os.chmod(full_path, stat.S_IWRITE)


def format_to_unix(file_name):
    newlines = []
    changed = 0
    for line in open(file_name, 'rb').readlines():
        if line[-2:] == '\r\n':
            line = line[:-2] + '\n'
            changed = 1
        newlines.append(line)
    if changed:
        open(file_name, 'wb').writelines(newlines)


def dos2unix(file_path):
    if os.path.isfile(file_path):
        format_to_unix(file_path)
    else:
        for root, dirs, files in os.walk(file_path):
            for fname in files:
                full_path = os.path.join(root, fname)
                format_to_unix(full_path)


def put2a():
    region = FTP("10.20.117.28")
    region.login("fnsonlq", "fns123")
    current_ir = ' '
    seq = 0
    cur = conn.cursor()
    cur.execute("SELECT * FROM DAILY_UPDATE WHERE FILE_PATH NOT LIKE \"%LIBRY%\" AND ISSUE_DATE = ? ORDER BY IR_NO",
                (today_date,))
    for ir, filename, filepath, date, modifier, test_no, production_date in cur.fetchall():
        module = filepath[1:].lower()
        if str(filename).endswith("xml") or str(filename).endswith("htm") or str(filename) == "makeio.input" \
                or str(filename).endswith("sqb"):
            continue
        if module == "src":
            module = "exe"
        local_dir = local_base_dir + module
        os.chdir(local_dir)
        if current_ir != ir:
            seq += 1
            current_ir = str(ir)
            print "IR no." + str(seq) + " : " + current_ir
            outer_dir = "/fns/q/r/update/" + today_date + "_" + str(seq)
            ir_seq.append([ir, modifier])
            region.mkd(outer_dir)
            region.cwd(outer_dir)
            region.mkd(module)
            region.cwd(module)
            for codes in os.listdir(local_dir):
                if codes[:codes.find('.')+1] == filename[:filename.find('.')+1]:
                    region.storbinary('STOR '+codes, open(codes, 'rb'))
            if module == "exe":
                region.cwd(outer_dir)
                region.mkd('src')
                region.cwd('src')
                os.chdir(local_base_dir+'src')
                for codes in os.listdir(local_base_dir+'src'):
                    if codes == filename:
                        region.storbinary('STOR '+codes, open(codes, 'rb'))
                region.cwd(outer_dir)
                region.mkd('mflist')
                region.cwd('mflist')
                os.chdir(local_base_dir+'mflist')
                for codes in os.listdir(local_base_dir+'mflist'):
                    if codes[:6] == filename[:6]:
                        region.storbinary('STOR '+codes, open(codes, 'rb'))
                os.chdir(local_dir)
        else:
            try:
                region.cwd(outer_dir + '/' + module)
            except:
                region.mkd(outer_dir + '/' + module)
                region.cwd(outer_dir + '/' + module)
            for codes in os.listdir(local_dir):
                if codes[:codes.find('.')+1] == filename[:filename.find('.')+1]:
                    region.storbinary('STOR '+codes, open(codes, 'rb'))
            if module == "exe":
                os.chdir(local_base_dir+'src')
                try:
                    region.cwd(outer_dir + '/' + 'src')
                except:
                    region.mkd(outer_dir + '/' + 'src')
                    region.cwd(outer_dir + '/' + 'src')
                for codes in os.listdir(local_base_dir+'src'):
                    if codes == filename:
                        region.storbinary('STOR '+codes, open(codes, 'rb'))
                os.chdir(local_dir)
                os.chdir(local_base_dir+'mflist')
                try:
                    region.cwd(outer_dir + '/' + 'mflist')
                except:
                    region.mkd(outer_dir + '/' + 'mflist')
                    region.cwd(outer_dir + '/' + 'mflist')
                for codes in os.listdir(local_base_dir+'mflist'):
                    if codes[:6] == filename[:6]:
                        region.storbinary('STOR '+codes, open(codes, 'rb'))
                os.chdir(local_dir)
    region.quit()
    
    
def get_copy_book():
    """copy books are in different directories,so we
    get it all once from the database and compile them later"""
    cpbook = []
    cur = conn.cursor()
    cur.execute("SELECT FILE_NAME FROM DAILY_UPDATE WHERE FILE_PATH LIKE \"%LIBRY%\" AND ISSUE_DATE = ?", (today_date,))
    for file_name in cur.fetchall():
        cpbook.append(file_name[0])   # we only select one field so we get a tuple,I mean file_name is a tuple
    return cpbook


def insert_related_programme(copy_book, programme_list):
    """insert related programmes into database so that we can
    get the gnts"""
    ir_no = ''
    modifier = ''
    cur = conn.cursor()
    cur.execute("SELECT IR_NO,MODIFIER FROM DAILY_UPDATE WHERE FILE_NAME = ? AND ISSUE_DATE = ?",
                (copy_book, today_date))
    for ir_no, modifier in cur.fetchmany(1):
        pass
    for code in programme_list:
        try:
            conn.execute("insert into daily_update values (?,?,?,?,?,?,?)", (ir_no, code, '$src', today_date, modifier,
                         "TO BE ADDED", 'N'))
        except sqlite3.IntegrityError:
            print "record", ir_no, code, "already exits"
    cur.close()
    
    
def compile_cob(host, user, password):
    region = telnetlib.Telnet(host)
    region.read_until("login:", 3)
    region.write(user + "\n")
    region.read_until("Password:", 3)
    region.write(password + "\n")
    for program in os.listdir(local_base_dir + 'src'):
        print "now processing ", program
        region.write("compilecob " + program + "\n")
        result = region.read_until("Terminal output also present in")
        if result.count("error(s) in compilation:"):
            print "not SUCCESSFUL".ljust(20) + program.center(10) + host.rjust(20)
    region.close()
    
   
def get_gnt(host, user, password):
    """get all the gnt from qa and then we put them
    to A region"""
    if not os.path.exists(local_base_dir + 'exe'):
        os.makedirs(local_base_dir + 'exe')
    cur = conn.cursor()
    cur.execute("SELECT FILE_NAME,ISSUE_DATE FROM DAILY_UPDATE WHERE FILE_PATH = \"$src\" AND ISSUE_DATE = ?",
                (today_date,))
    qa = FTP(host)
    qa.login(user, password)
    os.chdir(local_base_dir + 'exe')
    qa.cwd("/fns/q/r/exe")
    for program, issuedate in cur.fetchall():
        gnt = program[0:program.find(".")+1] + "gnt"
        try:
            qa.retrbinary('RETR ' + gnt, open(gnt, 'wb').write)
        except:
            print "can not get " + gnt + " from old qa"
    qa.quit()
    cur.close()


def get_mflist(host, user, password):
    """get the file in mflist directory for version checking"""
    if not os.path.exists(local_base_dir + 'mflist'):
        os.makedirs(local_base_dir + 'mflist')
    cur = conn.cursor()
    cur.execute("SELECT FILE_NAME,ISSUE_DATE FROM DAILY_UPDATE WHERE FILE_PATH = \"$src\" AND ISSUE_DATE = ?",
                (today_date,))
    qa = FTP(host)
    qa.login(user, password)
    os.chdir(local_base_dir + 'mflist')
    qa.cwd("/fns/q/r/mflist")
    for program, issuedate in cur.fetchall():
        mflist = program[0:program.find(".")+1] + "Z"
        try:
            qa.retrbinary('RETR ' + mflist, open(mflist, 'wb').write)
        except:
            print "can not get " + mflist + " from old qa"
    qa.quit()
    cur.close()

    
    
def compile_copy_book(host, user, password, cpbooks):
    region = telnetlib.Telnet(host)
    region.read_until("login:", 3)
    region.write(user + "\n")
    region.read_until("Password:", 3)
    region.write(password + "\n")
    for filename in cpbooks:
        if filename not in need_compile:
            continue
        programme_list = []
        region.write("cpbookcompile " + str(filename) + "\n")
        result = region.read_until("No failures in COB/PCO Compilations.", 300)
        if result.count("No failures in COB/PCO Compilations") > 0:
            preprogramme_list = result.split("\r\n")
            for i in range(0, len(preprogramme_list)):
                if preprogramme_list[i].count(".COB") + preprogramme_list[i].count(".PCO") > 0:
                    programme_list.append(preprogramme_list[i])
        else:
            print "compile copy book " + filename + " failed in " + host
        if host == "10.20.112.55":
            insert_related_programme(filename, programme_list)
    region.close()
            
            
def put_copy_book(host, user, password, module):
    region = FTP(host)
    region.login(user, password)
    if host == "10.20.143.32":
        region.cwd("/fns/p/r/src/LIBRY" + str(module).upper())
    elif host == "10.20.112.55":
        region.cwd("/fns/q/r/src/LIBRY" + str(module).upper())
    else:
        region.cwd("/fns/d5/r/src/LIBRY" + str(module).upper())
    os.chdir(local_base_dir + str(module))
    for program in os.listdir(local_base_dir + str(module).upper()):
        region.storbinary('STOR '+program, open(program, 'r'))
    region.quit()
    
    
def put_sqb(host, user, password):
    region = FTP(host)
    region.login(user, password)
    if host == "10.20.143.32":
        region.cwd("/fns/p/r/dbdb2/pco")
    elif host == "10.20.112.55":
        region.cwd("/fns/q/r/dbdb2/pco")
    else:
        region.cwd("/fns/d5/r/dbdb2/pco")
    os.chdir(local_base_dir + 'sqb')
    for program in os.listdir(local_base_dir + 'sqb'):
        region.storbinary('STOR '+program, open(program, 'r'))
    region.quit()
    
    
def put_src(host, user, password, floder):
    region = FTP(host)
    region.login(user, password)
    if host == "10.20.143.32":
        region.cwd("/fns/p/r/" + str(floder))
    elif host == "10.20.112.55":
        region.cwd("/fns/q/r/" + str(floder))
    else:
        region.cwd("/fns/d5/r/" + str(floder))
    os.chdir(local_base_dir + str(floder))
    for program in os.listdir(local_base_dir + str(floder)):
        region.storbinary('STOR '+program, open(program, 'r'))
    region.quit()
    
    
def put_files_compile():
    """this function put file to related region,and compile them later
    if need.
    this function's implementation is bad,maybe can improve it
    in the future"""
    has_copy_book = False
    if 'GEN' in os.listdir(local_base_dir):
        has_copy_book = True
        put_copy_book("10.20.143.32", "fnsonlp", "tata123", "gen")
        put_copy_book("10.20.112.55", "fnsonlq", "ccffcc", "gen")
    if 'INV' in os.listdir(local_base_dir):
        has_copy_book = True
        put_copy_book("10.20.143.32", "fnsonlp", "tata123", "inv")
        put_copy_book("10.20.112.55", "fnsonlq", "ccffcc", "inv")
    if 'BOR' in os.listdir(local_base_dir):
        has_copy_book = True
        put_copy_book("10.20.143.32", "fnsonlp", "tata123", "bor")
        put_copy_book("10.20.112.55", "fnsonlq", "ccffcc", "bor")
    if 'CTA' in os.listdir(local_base_dir):
        has_copy_book = True
        put_copy_book("10.20.143.32", "fnsonlp", "tata123", "cta")
        put_copy_book("10.20.112.55", "fnsonlq", "ccffcc", "cta")
    if 'MIS' in os.listdir(local_base_dir):
        has_copy_book = True
        put_copy_book("10.20.143.32", "fnsonlp", "tata123", "mis")
        put_copy_book("10.20.112.55", "fnsonlq", "ccffcc", "mis")
    if 'ATM' in os.listdir(local_base_dir):
        has_copy_book = True
        put_copy_book("10.20.143.32", "fnsonlp", "tata123", "atm")
        put_copy_book("10.20.112.55", "fnsonlq", "ccffcc", "atm")
    if 'src' in os.listdir(local_base_dir):
        put_src("10.20.112.55", "fnsonlq", "ccffcc", "src")
        put_src("10.20.143.32", "fnsonlp", "tata123", "src")
        compile_cob("10.20.143.32", "fnsonlp", "tata123")
        compile_cob("10.20.112.55", "fnsonlq", "ccffcc")
    if 'sql' in os.listdir(local_base_dir):
        put_src("10.20.143.32", "fnsonlp", "tata123", "sql")
        put_src("10.20.112.55", "fnsonlq", "ccffcc", "sql")
        print "have table please compile later"
    if 'cat' in os.listdir(local_base_dir):
        put_src("10.20.143.32", "fnsonlp", "tata123", "cat")
        put_src("10.20.112.55", "fnsonlq", "ccffcc", "cat")
    if 'sqb' in os.listdir(local_base_dir):
        put_sqb("10.20.143.32", "fnsonlp", "tata123")
        put_sqb("10.20.112.55", "fnsonlq", "ccffcc")
        print "have sqb please compile and  put the gnt and exe to A region"
    if 'sh' in os.listdir(local_base_dir):
        put_src("10.20.143.32", "fnsonlp", "tata123", "sh")
        put_src("10.20.112.55", "fnsonlq", "ccffcc", "sh")
    if 'card' in os.listdir(local_base_dir):
        put_src("10.20.143.32", "fnsonlp", "tata123", "card")
        put_src("10.20.112.55", "fnsonlq", "ccffcc", "card")
    if has_copy_book:
        cpbooks = get_copy_book()
        compile_copy_book("10.20.112.55", "fnsonlq", "ccffcc", cpbooks)
        compile_copy_book("10.20.143.32", "fnsonlp", "tata123", cpbooks)
    get_gnt("10.20.112.55", "fnsonlq", "ccffcc")
    get_mflist("10.20.112.55", "fnsonlq", "ccffcc")

def compile_code():
    make_writable(local_base_dir)
    dos2unix(local_base_dir)
    put_files_compile()


def get_file_by_path(filename, filepath, vss, compile_flag):
    if filepath[-3:] != 'cat':
        item_path = "$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRY" + filepath[-3:] + '/' + filename
        dir_path = local_base_dir + filepath[-3:]
        path = vss.VSSItem(item_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path.Get(dir_path + "\\" + filename)
        if compile_flag:
            need_compile.append(filename)
    elif filepath.endswith("cat"):
        path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/cat/" + filename)
        dir_path = local_base_dir + 'cat'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path.Get(dir_path + "\\" + filename)
    else:
        print "warning: " + filename + "  can not get it from vss,may be you can get it from QA directly"


def get_file_by_name(filename, vss):
    file_type = ''
    if filename.endswith('xml'):
        path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/bancslink/xml/Transactions/" + filename)
        if not os.path.exists(local_base_dir + 'xml'):
            os.makedirs(local_base_dir + 'xml')
        path.Get(local_base_dir + 'xml\\\\' + filename)
    elif filename.endswith('htm'):
        path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/bancslink/HTML/" + filename)
        if not os.path.exists(local_base_dir + 'html'):
            os.makedirs(local_base_dir + 'html')
        path.Get(local_base_dir + 'html\\\\' + filename)
    elif '.' in filename:
        file_type = filename[filename.rfind('.')+1:]
    if file_type == 'COB':
        file_type = 'src'
        home_path = local_base_dir + file_type
        if not os.path.exists(home_path):
            os.makedirs(home_path)
        path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/" + file_type + "/" + filename)
        path.Get(home_path + "\\" + filename)
    else:
        if filename.endswith('xml') or filename.endswith('htm'):
            pass
        elif filename.endswith('sqb'):
            path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/dbdb2/pco/" + filename)
            home_path = local_base_dir + file_type
            if not os.path.exists(home_path):
                os.makedirs(home_path)
            path.Get(home_path + "\\" + filename)
        elif filename.endswith('sql') or filename.endswith('md') or filename.endswith('card') or filename.endswith('sh'):
            if filename.endswith('md'):
                file_type = 'sql'
            path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/" + file_type + "/" + filename)
            home_path = local_base_dir + file_type
            if not os.path.exists(home_path):
                os.makedirs(home_path)
            path.Get(home_path + "\\" + filename)
        elif filename.endswith('in'):
            file_type = 'sysin'
            path = vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/sysin/" + filename)
            home_path = local_base_dir + file_type
            if not os.path.exists(home_path):
                os.makedirs(home_path)
            path.Get(home_path + "\\" + filename)
        else:
            print filename, "can not get it from vss,maybe can get from qa"


def store_source(filename, filepath, compile_flag):
    vss = win32com.client.Dispatch('SourceSafe')
    vss.Open(r"\\10.20.47.202\SRCB Document Management\srcsafe.ini", "chenchf", "2000")
    path = str(filepath)
    name = str(filename)
    name = name.strip()
    if name.count('.'):
        get_file_by_name(name, vss)
    else:
        get_file_by_path(name, path, vss, compile_flag)


def get_from_qafile():
    file_record = []
    record_line_no = []
    qa_file = excel.Excel(unicode(r'\\10.20.47.202\共享目录\开发文档\QA file release management(format for dev).xlsx',
                                  "utf-8"),
                          'CC to QA Release Management')
    for i in xrange(qa_file.used_range(), -1, -1):
        row = qa_file.get_row_data(i)
        if qa_file.get_cell_color(i, 1) == 6 and qa_file.get_cell_color(i, 2) == 6:
            break
        elif not row[0]:
            pass
        else:
            print row[0], row[1], row[6], row[9], row[10]
            store_source(row[1], row[2], row[5])
            file_record.append((row[0].strip(), row[1], row[2], today_date, row[4], "TO BE ADDED", 'N'))
            record_line_no.append(i-1)
            qa_file.set_value(i, 13, today_date)
            qa_file.set_value(i, 14, unicode("宋军钊", "utf-8"))
    qa_file.set_row_color(max(record_line_no), 6)
    insert_record(file_record)
    qa_file.quit()


def get_files():
    if os.path.exists(local_base_dir):
        make_writable(local_base_dir)
        shutil.rmtree(local_base_dir)
    get_from_qafile()


def get_test_doc(ir_no, des):
    for test_file in os.listdir(unicode(r'\\10.20.47.202\共享目录\开发文档\生产问题单元测试报告',"utf-8")):
        if test_file.count(ir_no[-5:]) >= 1:
            shutil.copy(unicode(r'\\10.20.47.202\共享目录\开发文档\生产问题单元测试报告\\', "utf-8")+test_file,
                        des+'\\'+test_file)
            break


def prepare_version_app(current_ir, excel_path, seq):
    version_excel = excel.Excel(excel_path, unicode('上版申请', "utf-8"))
    version_excel.set_value(2, 4, str(time.strftime("%Y-%m-%d", time.localtime())))
    version_excel.set_value(2, 8, str(time.strftime("%Y-%m-%d", time.localtime())))
    version_excel.set_value(7, 2, require_no.get(current_ir, "not found"))
    version_excel.set_value(7, 4, current_ir)
    version_excel.set_value(7, 6, bug_description.get(current_ir, "desc not found"))
    version_excel.set_value(17, 4, today_date+'_'+str(seq)+'.tar')
    version_excel.set_value(21, 4, version_excel.get_cell_value(21, 4).replace('20130814', today_date+'_'+str(seq)))
    version_excel.set_value(22, 4, ' ')
    version_excel.quit()


def prepare_version_code(current_ir, excel_path):
    """we should get all the files related to the ir
    so get it from the database"""
    seq = 0
    version_excel = excel.Excel(excel_path, unicode('程序清单', "utf-8"))
    cur = conn.cursor()
    cur.execute("SELECT FILE_NAME,FILE_PATH, MODIFIER FROM DAILY_UPDATE WHERE IR_NO = ? AND ISSUE_DATE = ?",
                (current_ir, today_date))
    for cur_file, cur_path, modifier in cur.fetchall():
        seq += 1
        version_excel.set_value(seq+1, 1, str(seq))
        version_excel.set_value(seq+1, 2, "/fns/p/r/"+cur_path[1:]+"/"+cur_file)
        version_excel.set_value(seq+1, 4, current_ir)
        version_excel.set_value(seq+1, 8, modifier)
        version_excel.set_value(seq+1, 6, ' ')
        version_excel.set_value(seq+1, 7, ' ')
        version_excel.set_value(seq+1, 5, bug_description.get(current_ir, "desc not found"))
    cur.close()
    version_excel.quit()


def prepare_version_excel():
    """add code later"""
    seq = 0
    for current_ir, current_modifier in ir_seq:
        seq += 1
        #version_dir = unicode(r'C:\Documents and Settings\user\桌面\update\\', "utf-8") + today_date + '_' + str(seq)
        version_dir = unicode(r'C:\Documents and Settings\user\桌面\update\\', "utf-8") + \
                      today_date + '--' + require_no.get(current_ir, "not found") + "--" + current_ir
        os.mkdir(version_dir)
        excel_path = version_dir+'\\'+unicode('新一代系统上版申请表【BANCS】【',
                                              "utf-8")+today_date+'_'+str(seq)+unicode('】.xls', "utf-8")
        shutil.copy(base_version_excel, excel_path)
        prepare_version_app(current_ir, excel_path, seq)
        prepare_version_code(current_ir, excel_path)
        get_test_doc(current_ir, version_dir)
        shutil.copy(unimportant_code_list, version_dir+'\\'+today_date+'_'+str(seq)+unicode('版本清单.xlsx', "utf-8"))
        shutil.copy(unimportant_test_case, version_dir+'\\'+unicode('端到端测试版本提交记录_新核心项目组_20130814 '
                                                   '第二轮端到端基准版本.xls', "utf-8"))


def backup_database():
    conn.commit()  # before backup,commit first
    conn.close()
    shutil.copy(database_file, r'c:\\dailyUpdate.db')


def main():
    get_files()
    compile_code()
    put2a()
    prepare_version_excel()
    backup_database()
if __name__ == '__main__':
    main()
    print "remember to modify the app file and send the mail"