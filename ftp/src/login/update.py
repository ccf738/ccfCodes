'''
Created on 2013-2-17

@author: ccf
'''
import win32com.client
from ftplib import FTP
import os
import shutil
import telnetlib
import time
import stat
import io
def Getbnd(host,user,password,module):
    if not os.path.exists(r'C:\good\cobol\update\dbdb2\exe'):
        os.makedirs(r'C:\good\cobol\update\dbdb2\exe')
    if not os.path.exists(r'C:\good\cobol\update\dbdb2\bnd'):
        os.makedirs(r'C:\good\cobol\update\dbdb2\bnd')
    qa = FTP(host)
    qa.login(user, password)
    os.chdir(r'C:\good\cobol\update\dbdb2\exe')
    qa.cwd("/fns/q/r/dbdb2/exe")
    for code in os.listdir(r'C:\good\cobol\update\\' + module):
        fileName = code[0:code.find(".")+1]
        if "sql" == module:
            gnt = "DBIO" + fileName.upper() + "gnt"
        else:
            gnt = fileName + "gnt"
        print gnt
        print qa.pwd()
        qa.retrbinary('RETR ' + gnt, open(gnt, 'wb').write)
    os.chdir(r'C:\good\cobol\update\dbdb2\bnd')
    qa.cwd("/fns/q/r/dbdb2/bnd")
    for code in os.listdir(r'C:\good\cobol\update\\' + module):
        fileName = code[0:code.find(".")+1]
        if "sql" == module:
            bnd = "DBIO" + fileName.upper() + "bnd"
        else:
            bnd = fileName + "bnd"
        qa.retrbinary('RETR ' + gnt, open(bnd, 'wb').write)
    qa.quit()
def PutSqxToA():
    Aregion = FTP("10.20.117.28")
    Aregion.login("fnsonlq", "fns123")
    os.chdir(r'C:\good\cobol\update\dbdb2\exe')
    try:
        Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())))
    except:
        Aregion.mkd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())))
        Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())))
    Aregion.mkd("dbdb2")
    Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())) + "/dbdb2")
    Aregion.mkd("exe")
    Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())) + "/dbdb2/exe")
    for codes in os.listdir(r'C:\good\cobol\update\dbdb2\exe'):
        Aregion.storbinary('STOR '+codes, open(codes, 'rb'))
    os.chdir(r'C:\good\cobol\update\dbdb2\bnd')
    Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())) + "/dbdb2")
    Aregion.mkd("bnd")
    Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())) + "/dbdb2/bnd")
    for codes in os.listdir(r'C:\good\cobol\update\dbdb2\bnd'):
        Aregion.storbinary('STOR '+codes, open(codes, 'rb'))
    Aregion.quit()
def CompileSql(host,user,password):
    print "compile SQLS start on " + host + " user: " + user + ''.center(10,"-")
    region = telnetlib.Telnet(host)
    region.read_until("login:", 3) 
    region.write(user + "\n")
    region.read_until("Password:", 3)
    region.write(password + "\n")
    for code in os.listdir(r'C:\good\cobol\update\sql'):
        tableName = code[0:code.find(".")]
        region.write("conn\n")
        time.sleep(3)
        region.write("db2 \"create table " + tableName + "_bkp like " + tableName + "\"\n")
        result = region.read_until("The SQL command completed successfully.", 1)
        if result.count("The SQL command completed successfully."):
            region.write("db2 \"insert into " + tableName + "_bkp select * from " + tableName + "\"")
            region.read_until("The SQL command completed successfully.", 100)
            region.write("db2 \"drop table " + tableName + "\"\n")
            region.read_until("The SQL command completed successfully.", 100)
        else:
            if result.count("The name of the object to be created is identical to the existing"):
                region.write("db2 \"delete from " + tableName + "_bkp\"\n")
                region.read_until("The SQL command completed successfully.", 100)
                region.write("db2 \"insert into " + tableName + "_bkp select * from " + tableName + "\"\n")
                region.read_until("The SQL command completed successfully.", 600)
                region.write("db2 \"drop table " + tableName + "\"\n")
                region.read_until("The SQL command completed successfully.", 100)
            else:
                print tableName + " compile have some problem please check"
                continue
        region.write("makeddl -o nn rdev " + tableName + "\n")
        region.read_until("okay [Y/N]?", 3)
        region.write("Y\n")
        result = region.read_until("generate successful", 3)
        if result.count("generate successful"):
            pass
        else:
            region.write("makeddl -o nn rdev " + tableName + "\n")
            region.read_until("okay [Y/N]?", 3)
            region.write("Y\n")
            result = region.read_until("generate successful", 3)
            if result.count("generate successful"):
                pass
            else:
                print "compile table " + tableName + " not successful" + host.rjust(20)
        region.write("cd $dbsrc/sql\n")
        time.sleep(1)
        region.read_very_eager()
        region.write(tableName + "tbcr.sh\n")
        time.sleep(5)
        region.write("makeio -on " + tableName + "\n")
        result = region.read_until("makeio: generate successful", 3)
        if result.count("makeio: generate successful"):
            pass
        else:
            print "makeio error " + tableName + host.rjust(20)
            print result
        region.write("cd $dbsrc/pco\n")
        time.sleep(1)
        region.write("precompile DBIO" + tableName.upper() + "\n")
        result = region.read_until("The TERMINATE command completed successfully.", 3)
        if result.count("Precompilation or binding was ended with \"0\""):
            pass
        else:
            print "precompile " + tableName + " has problem please check" + host.rjust(20)
            print result
            continue
        region.write("compile -o dbi DBIO" + tableName.upper() + "\n")
        result = region.read_until("compile: succesful compile",3)
        if result.count("compile: succesful compile"):
            pass
        else:
            print "compile -o dbi " + tableName + " has problem please check " + host.rjust(20)
            print result
            continue
        region.write("compile -o u DBIO" + tableName.upper() + "\n")
        time.sleep(1)
        region.write("cd $dbsrc/bnd\n")
        time.sleep(1)
        region.read_very_eager()
        region.write("db2 bind DBIO" + tableName.upper() + ".bnd\n")
        result = region.read_until("warnings.", 3)
        if result.count("Binding was ended with \"0\" errors"):
            pass
        else:
            print "bind " + tableName + " has problem please check"
            print result
            continue
        region.write("db2 \"insert into " + tableName + " select * from " + tableName + "_bkp\"\n")
        print tableName + " compiled successfully in" +  host.rjust(20)
    region.close()
    print "compile COBS end on " + host + " user: " + user + ''.center(10,"-")
def makeWritable(path):
    if os.path.exists(path):
        os.chmod(path, stat.S_IWRITE)
        for root, dirs, files in os.walk(path):
            for fname in files:
                full_path = os.path.join(root, fname)
                os.chmod(full_path ,stat.S_IWRITE)
                dos2unix(full_path)
def dos2unix(fname):
    newlines = []
    changed  = 0
    for line in open(fname, 'rb').readlines():
        if line[-2:] == '\r\n':
            line = line[:-2] + '\n'
            changed = 1
        newlines.append(line)
    if changed:
        open(fname, 'wb').writelines(newlines)
def PutSqb(host,user,password):
    region = FTP(host)
    region.login(user, password)
    if host == "10.20.143.32":
        region.cwd("/fns/p/r/dbdb2/pco")
    elif host == "10.20.112.55":
        region.cwd("/fns/q/r/dbdb2/pco")
    else:
        region.cwd("/fns/d5/r/dbdb2/pco")
    os.chdir(r'C:\good\cobol\update\sqb')
    for program in os.listdir(r'C:\good\cobol\update\sqb'):
        region.storbinary('STOR '+program, open(program, 'r'))
    region.quit()
def PutSrc(host,user,password,floder):
    region = FTP(host)
    region.login(user, password)
    if host == "10.20.143.32":
        region.cwd("/fns/p/r/" + str(floder))
    elif host == "10.20.112.55":
        region.cwd("/fns/q/r/" + str(floder))
    else:
        region.cwd("/fns/d5/r/" + str(floder))
    os.chdir(r'C:\good\cobol\update\\' + str(floder))
    for program in os.listdir(r'C:\good\cobol\update\\' + str(floder)):
        region.storbinary('STOR '+program, open(program, 'r'))
    region.quit()
def PutCopybook(host,user,password,module):
    region = FTP(host)
    region.login(user, password)
    if host == "10.20.143.32":
        region.cwd("/fns/p/r/src/LIBRY" + str(module).upper())
    elif host == "10.20.112.55":
        region.cwd("/fns/q/r/src/LIBRY" + str(module).upper())
    else:
        region.cwd("/fns/d5/r/src/LIBRY" + str(module).upper())
    os.chdir(r'C:\good\cobol\update\\' + str(module))
    for program in os.listdir(r'C:\good\cobol\update\\' + str(module)):
        region.storbinary('STOR '+program, io.open(program, 'U'))
    region.quit()
def CompileSqb(host,user,password):
    print "compile SQBS start on " + host + " user: " + user + ''.center(10,"-")
    region = telnetlib.Telnet(host)
    region.read_until("login:", 3) 
    region.write(user + "\n")
    region.read_until("Password:", 3)
    region.write(password + "\n")
    if "10.20.143.32" == host:
        path = "/fns/p/r/dbdb2/"
    elif "10.20.112.55" == host:
        path = "/fns/q/r/dbdb2/"
    else:
        path = "/fns/d5/r/dbdb2/"
    region.write("cd " + path + "pco\n")
    for code in os.listdir(r'C:\good\cobol\update\sqb'):
        sqb = code[0:code.find(".")]
        print sqb
        region.write("precompile " + sqb + "\n")
        result = region.read_until("The TERMINATE command completed successfully.", 3)
        if result.count("Precompilation or binding was ended with \"0\""):
            pass
        else:
            print "precompile " + code + " has problem please check " + host
            continue
        region.write("compile -o dbi " + sqb + "\n")
        result = region.read_until("compile: succesful compile",3)
        if result.count("compile: succesful compile"):
            pass
        else:
            print "compile -o dbi " + code + " has problem please check " + host
            continue
        region.write("compile -o u " + sqb + "\n")
        time.sleep(1)
        region.write("cd " + path + "bnd\n")
        time.sleep(1)
        region.write("conn\n")
        time.sleep(1)
        region.read_very_eager()
        region.write("db2 bind " + sqb + ".bnd\n")
        result = region.read_until("warnings.", 3)
        if result.count("Binding was ended with \"0\" errors"):
            pass
        else:
            print "bind " + code + " has problem please check " + host 
            continue
        print code + " compile successfully"
    region.close()
    print "compile COBS end on " + host + " user: " + user + ''.center(10,"-")
def CompileCob(host,user,password):
    print "compile COBS start on " + host + " user: " + user + ''.center(10,"-")
    region = telnetlib.Telnet(host)
    region.read_until("login:", 3)
    region.write(user + "\n")
    region.read_until("Password:", 3)
    region.write(password + "\n")
    for program in os.listdir(r'C:\good\cobol\update\src'):
        region.write("compilecob " + program + "\n")
        result = region.read_until("Terminal output also present in")
        if result.count("error(s) in compilation:"):
            print "not SUCCESSFUL".ljust(20) + program.center(10) + host.rjust(20)
        else:
            print "SUCCESSFUL".ljust(20) + program.center(10) + host.rjust(20)
    region.close()
    print "compile COBS end on " + host + " user: " + user + ''.center(10,"-")
def GetGnt(host,user,password):
    if not os.path.exists(r'C:\good\cobol\update\exe'):
        os.makedirs(r'C:\good\cobol\update\exe')
    qa = FTP(host)
    qa.login(user, password)
    os.chdir(r'C:\good\cobol\update\exe')
    qa.cwd("/fns/q/r/exe")
    for program in os.listdir(r'C:\good\cobol\update\src'):
        gnt = program[0:program.find(".")+1] + "gnt"
        qa.retrbinary('RETR ' + gnt, open(gnt, 'wb').write)
    qa.quit()
def PutToARegion(module):
    Aregion = FTP("10.20.117.28")
    Aregion.login("fnsonlq", "fns123")
    os.chdir(r'C:\good\cobol\update\\' + module)
    try:
        Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())))
    except:
        Aregion.mkd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())))
        Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())))
    Aregion.mkd(str(module))
    Aregion.cwd("/fns/q/r/update/" + str(time.strftime("%Y%m%d", time.localtime())) + "/" + str(module))
    for codes in os.listdir(r'C:\good\cobol\update\\' + module):
        Aregion.storbinary('STOR '+codes, open(codes, 'rb'))
    Aregion.quit()
def Putfiles():
    if 'gen' in os.listdir(r'C:\good\cobol\update'):
        PutCopybook("10.20.117.17","fnsonld5","fnsonld5","gen")
        PutCopybook("10.20.143.32","fnsonlp","fnsonlp","gen")
        PutCopybook("10.20.112.55","fnsonlq","fnsqa","gen")
    if 'inv' in os.listdir(r'C:\good\cobol\update'):
        PutCopybook("10.20.117.17","fnsonld5","fnsonld5","inv")
        PutCopybook("10.20.143.32","fnsonlp","fnsonlp","inv")
        PutCopybook("10.20.112.55","fnsonlq","fnsqa","inv")
    if 'bor' in os.listdir(r'C:\good\cobol\update'):
        PutCopybook("10.20.117.17","fnsonld5","fnsonld5","bor")
        PutCopybook("10.20.143.32","fnsonlp","fnsonlp","bor")
        PutCopybook("10.20.112.55","fnsonlq","fnsqa","bor")
    if 'cta' in os.listdir(r'C:\good\cobol\update'):
        PutCopybook("10.20.117.17","fnsonld5","fnsonld5","cta")
        PutCopybook("10.20.143.32","fnsonlp","fnsonlp","cta")
        PutCopybook("10.20.112.55","fnsonlq","fnsqa","cta")
    if 'mis' in os.listdir(r'C:\good\cobol\update'):
        PutCopybook("10.20.117.17","fnsonld5","fnsonld5","mis")
        PutCopybook("10.20.143.32","fnsonlp","fnsonlp","mis")
        PutCopybook("10.20.112.55","fnsonlq","fnsqa","mis")
    if 'atm' in os.listdir(r'C:\good\cobol\update'):
        PutCopybook("10.20.117.17","fnsonld5","fnsonld5","atm")
        PutCopybook("10.20.143.32","fnsonlp","fnsonlp","atm")
        PutCopybook("10.20.112.55","fnsonlq","fnsqa","atm")
    if 'src' in os.listdir(r'C:\good\cobol\update'):
        PutSrc("10.20.117.17","fnsonld5","fnsonld5","src")
        PutSrc("10.20.112.55","fnsonlq","fnsqa","src")
        PutSrc("10.20.143.32","fnsonlp","fnsonlp","src")
#        CompileCob("10.20.117.17","fnsonld5","fnsonld5")
#        CompileCob("10.20.143.32","fnsonlp","fnsonlp")
#        CompileCob("10.20.112.55","fnsonlq","fnsqa")
        GetGnt("10.20.112.55","fnsonlq","fnsqa")
        PutToARegion("exe")
    if 'sql' in os.listdir(r'C:\good\cobol\update'):
        PutSrc("10.20.117.17","fnsonld5","fnsonld5","sql")
        PutSrc("10.20.143.32","fnsonlp","fnsonlp","sql")
        PutSrc("10.20.112.55","fnsonlq","fnsqa","sql")
#        CompileSql("10.20.117.17","fnsonld5","fnsonld5")
#        CompileSql("10.20.143.32","fnsonlpd","fnsonlpd")
#        CompileSql("10.20.112.55","fnsonlqd","fnsqd")
#        Getbnd("10.20.112.55","fnsonlqd","fnsqd","sql")
#        PutSqxToA()
        print "have table please compile later"
    if 'cat' in os.listdir(r'C:\good\cobol\update'):
        PutSrc("10.20.117.17","fnsonld5","fnsonld5","cat")
        PutSrc("10.20.143.32","fnsonlp","fnsonlp","cat")
        PutSrc("10.20.112.55","fnsonlq","fnsqa","cat")
        PutToARegion("cat")
    if 'sqb' in os.listdir(r'C:\good\cobol\update'):
        PutSqb("10.20.117.17","fnsonld5","fnsonld5")
        PutSqb("10.20.143.32","fnsonlp","fnsonlp")
        PutSqb("10.20.112.55","fnsonlq","fnsqa")
#        CompileSqb("10.20.117.17","fnsonld5","fnsonld5")
#        CompileSqb("10.20.143.32","fnsonlpd","fnsonlpd")
#        CompileSqb("10.20.112.55","fnsonlqd","fnsqd")
#        Getbnd("10.20.112.55","fnsonlqd","fnsqd","sql")
#        PutSqxToA()
        print "have sqb please compile and  put the gnt and exe to A region"
    if 'sh' in os.listdir(r'C:\good\cobol\update'):
        PutSrc("10.20.117.17","fnsonld5","fnsonld5","sh")
        PutSrc("10.20.143.32","fnsonlp","fnsonlp","sh")
        PutSrc("10.20.112.55","fnsonlq","fnsqa","sh")
        PutToARegion("sh")
    if 'card' in os.listdir(r'C:\good\cobol\update'):
        PutSrc("10.20.117.17","fnsonld5","fnsonld5","card")
        PutSrc("10.20.143.32","fnsonlp","fnsonlp","card")
        PutSrc("10.20.112.55","fnsonlq","fnsqa","card")
        PutToARegion("card")
def Compile():
    Putfiles()
def JudgeTypeByName(filename,vss):
    if filename.endswith('xml'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/bancslink/xml/Transactions/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\xml'):
            os.makedirs(r'C:\good\cobol\update\xml')
        path.Get("c:\\good\\cobol\\update\\xml\\" + filename)
    elif filename.endswith('htm'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/bancslink/HTML/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\html'):
            os.makedirs(r'C:\good\cobol\update\html')
        path.Get("c:\\good\\cobol\\update\\html\\" + filename)
    elif filename.endswith('COB'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\src'):
            os.makedirs(r'C:\good\cobol\update\src')
        path.Get("c:\\good\\cobol\\update\\src\\" + filename)
    elif filename.endswith('sh'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/sh/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\sh'):
            os.makedirs(r'C:\good\cobol\update\sh')
        path.Get("c:\\good\\cobol\\update\\sh\\" + filename)
    elif filename.endswith('sql'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/sql/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\sql'):
            os.makedirs(r'C:\good\cobol\update\sql')
        path.Get("c:\\good\\cobol\\update\\sql\\" + filename)
    elif filename.endswith('sqb'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/dbdb2/pco/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\sqb'):
            os.makedirs(r'C:\good\cobol\update\sqb')
        path.Get("c:\\good\\cobol\\update\\sqb\\" + filename)
    elif filename.endswith('card'):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/card/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\card'):
            os.makedirs(r'C:\good\cobol\update\card')
        path.Get("c:\\good\\cobol\\update\\card\\" + filename)
    else:
        print filename + "  can not get it from vss,may be you can get it from QA directly"
def JudgeTypeByPath(filename,filepath,vss):
    if filepath.endswith("INV"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRYINV/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\inv'):
            os.makedirs(r'C:\good\cobol\update\inv')
        path.Get("c:\\good\\cobol\\update\\inv\\" + filename)
    elif filepath.endswith("BOR"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRYBOR/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\bor'):
            os.makedirs(r'C:\good\cobol\update\bor')
        path.Get("c:\\good\\cobol\\update\\bor\\" + filename)
    elif filepath.endswith("GEN"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRYGEN/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\gen'):
            os.makedirs(r'C:\good\cobol\update\gen')
        path.Get("c:\\good\\cobol\\update\\gen\\" + filename)
    elif filepath.endswith("MIS"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRYMIS/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\mis'):
            os.makedirs(r'C:\good\cobol\update\mis')
        path.Get("c:\\good\\cobol\\update\\mis\\" + filename)
    elif filepath.endswith("CTA"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRYCTA/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\cta'):
            os.makedirs(r'C:\good\cobol\update\cta')
        path.Get("c:\\good\\cobol\\update\\cta\\" + filename)
    elif filepath.endswith("ATM"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/LIBRYATM/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\atm'):
            os.makedirs(r'C:\good\cobol\update\atm')
        path.Get("c:\\good\\cobol\\update\\atm\\" + filename)
    elif filepath.endswith("cat"):
        path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/cat/" + filename)
        if not os.path.exists(r'C:\good\cobol\update\cat'):
            os.makedirs(r'C:\good\cobol\update\cat')
        path.Get("c:\\good\\cobol\\update\\cat\\" + filename)
    else:
        print filename + "  can not get it from vss,may be you can get it from QA directly"
def StoreSource(filename,filepath):
    vss = win32com.client.Dispatch('SourceSafe') 
    vss.Open(r"\\10.188.208.100\SRCB Document Management\srcsafe.ini","chenchf","1234")
    path = str(filepath)
    name = str(filename)
    name = name.strip()
    if name.count('.'):
        JudgeTypeByName(name,vss)
    else:
        JudgeTypeByPath(name,path,vss)
def AnalysisQAfile():
    app = win32com.client.Dispatch('Excel.Application')
    workbook = app.Workbooks.Open('C:\\QA file.xlsx')
    sheet = workbook.Sheets('ccf1')
    for i in range(sheet.UsedRange.Rows.Count-1,-1,-1):
        row = sheet.UsedRange.Rows[i].Value[0]
        if sheet.UsedRange.Rows[i].Interior.ColorIndex == 6: #6 means yellow
            break
        elif not row[1]:
            pass
        else:
            StoreSource(row[1],row[2])
    app.Quit()
def GetFiles():
    makeWritable(r'C:\good\cobol\update')
    if os.path.exists(r'C:\good\cobol\update'):
        shutil.rmtree(r'C:\good\cobol\update')
    AnalysisQAfile()
def main():
    GetFiles()
    makeWritable(r'C:\good\cobol\update')
    Compile()
#    Quit()
if __name__ == "__main__":
    main()
    print "over REMEBER to send the mail"
    print "please do not close the window make sure update is successful"
    os.system("pause")