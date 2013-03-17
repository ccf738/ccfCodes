'''
Created on 2013-2-20

@author: ccf
'''
import telnetlib
import os
import time
def CompileSql(host,user,password):
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
            region.write("db2 \"drop table " + tableName + "\"\n")
            time.sleep(1)
        else:
            if result.count("The name of the object to be created is identical to the existing"):
                region.write("db2 \"delete from " + tableName + "_bkp\"\n")
                time.sleep(1)
                region.write("db2 \"insert into " + tableName + "_bkp select * from " + tableName + "\"\n")
                region.write("db2 \"drop table " + tableName + "\"\n")
                time.sleep(1)
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
        print tableName + " compiled successfully in" +  host.rjust(20)
    region.close()
        
if __name__ == "__main__":
    CompileSql("10.20.117.17","fnsonld5","fnsonld5")