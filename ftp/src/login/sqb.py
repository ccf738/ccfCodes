'''
Created on 2013-2-19

@author: ccf
'''
import telnetlib
import os
import time
def CompileSqb(host,user,password):
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
            print "precompile " + code + " has problem please check"
            continue
        region.write("compile -o dbi " + sqb + "\n")
        result = region.read_until("compile: succesful compile",3)
        if result.count("compile: succesful compile"):
            pass
        else:
            print "compile -o dbi " + code + " has problem please check"
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
            print "bind " + code + " has problem please check"
            continue
        print code + " compile successfully"
    region.close()
        
if __name__ == "__main__":
    CompileSqb("10.20.143.32","fnsonlpd","fnsonlpd")