'''
Created on 2012-7-4

@author: ccf
'''
import win32com.client
from ftplib import FTP
import os
import shutil
users = {'d1':'fnsonld1','d2':'fnsonld2','d3':'fnsonld3','d4':'fnsonld4','d5':'fnsonld5','d6':'fnsonld6'}
other = []
atm = []
cta = []
sqb = []
bnd = []
exe = []
cobol = []
mis = []
inv = []
bor = []
gen = []
shell = []
sql = []
cat = []
card = []
value = ''
path = ''

def DeleteFiles():
    if os.path.exists(r'C:\good\cobol\work\update'):
        shutil.rmtree(r'C:\good\cobol\work\update')
        
    

def GetSources(ip = '10.20.112.55',user = 'fnsonlq',password = 'srcb123'):
    DeleteFiles()
    os.makedirs(r'C:\good\cobol\work\update')
    ftp = FTP(ip)
    ftp.login(user, password)
    file = open(r'C:\Users\ccf\Desktop\list','w')
    if cobol:
        os.makedirs(r'C:\good\cobol\work\update\cobol')
        os.chdir(r'C:\good\cobol\work\update\cobol')
        ftp.cwd('/fns/q/r/src')
        for codes in cobol:
            file.write(codes + '\n')
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    file.close()
    if sql:
        os.makedirs(r'C:\good\cobol\work\update\sql')
        os.chdir(r'C:\good\cobol\work\update\sql')
        ftp.cwd('/fns/q/r/sql')
        for codes in sql:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if sqb:
        os.makedirs(r'C:\good\cobol\work\update\sqb')
        os.chdir(r'C:\good\cobol\work\update\sqb')
        ftp.cwd('/fns/q/r/dbdb2/pco')
        for codes in sqb:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if shell:
        os.makedirs(r'C:\good\cobol\work\update\shell')
        os.chdir(r'C:\good\cobol\work\update\shell')
        ftp.cwd('/fns/q/r/sh')
        for codes in shell:
            print codes
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if exe:
        os.makedirs(r'C:\good\cobol\work\update\exe')
        os.chdir(r'C:\good\cobol\work\update\exe')
        ftp.cwd('/fns/q/r/exe')
        for codes in shell:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if card:
        os.makedirs(r'C:\good\cobol\work\update\card')
        os.chdir(r'C:\good\cobol\work\update\card')
        ftp.cwd('/fns/q/r/card')
        for codes in card:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if bnd:
        os.makedirs(r'C:\good\cobol\work\update\bnd')
        os.chdir(r'C:\good\cobol\work\update\bnd')
        ftp.cwd('/fns/q/r/dbdb2/bnd')
        for codes in bnd:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if mis:
        os.makedirs(r'C:\good\cobol\work\update\mis')
        os.chdir(r'C:\good\cobol\work\update\mis')
        ftp.cwd('/fns/q/r/src/LIBRYMIS')
        for codes in mis:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if inv:
        os.makedirs(r'C:\good\cobol\work\update\inv')
        os.chdir(r'C:\good\cobol\work\update\inv')
        ftp.cwd('/fns/q/r/src/LIBRYINV')
        for codes in inv:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if bor:
        os.makedirs(r'C:\good\cobol\work\update\bor')
        os.chdir(r'C:\good\cobol\work\update\bor')
        ftp.cwd('/fns/q/r/src/LIBRYBOR')
        for codes in bor:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if gen:
        os.makedirs(r'C:\good\cobol\work\update\gen')
        os.chdir(r'C:\good\cobol\work\update\gen')
        ftp.cwd('/fns/q/r/src/LIBRYGEN')
        for codes in gen:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if cta:
        os.makedirs(r'C:\good\cobol\work\update\cta')
        os.chdir(r'C:\good\cobol\work\update\cta')
        ftp.cwd('/fns/q/r/src/LIBRYCTA')
        for codes in cta:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if atm:
        os.makedirs(r'C:\good\cobol\work\update\atm')
        os.chdir(r'C:\good\cobol\work\update\atm')
        ftp.cwd('/fns/q/r/src/LIBRYATM')
        for codes in atm:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    if cat:
        os.makedirs(r'C:\good\cobol\work\update\cat')
        os.chdir(r'C:\good\cobol\work\update\cat')
        ftp.cwd('/fns/q/r/cat')
        for codes in cat:
            ftp.retrbinary('RETR ' + codes, open(codes, 'wb').write)
    ftp.quit()
            
def GetEndRow(sheet):
    for i in range(sheet.UsedRange.Rows.Count-1,-1,-1):
        if sheet.UsedRange.Rows[i].Interior.ColorIndex == 6:
            return i + 1
        
def GetStartRow(sheet):
    for i in range(sheet.UsedRange.Rows.Count-1,-1,-1):
        if sheet.UsedRange.Rows[i].Interior.ColorIndex == 3:
            return i + 1
        
def JudgeTypeByName(FileName):
    FileName = str(FileName)
    if FileName.endswith('COB'):
        if FileName not in cobol:
            cobol.append(FileName)
    elif FileName.endswith('sh'):
        if FileName not in shell:
            shell.append(FileName)
    elif FileName.endswith('sql'):
        if FileName not in sql:
            sql.append(FileName)
    elif FileName.endswith('card'):
        if FileName not in card:
            card.append(FileName)
    elif FileName.endswith('sqb'):
        if FileName not in sqb:
            sqb.append(FileName)
    elif FileName.endswith('exe'):
        if FileName not in exe:
            exe.append(FileName)
    elif FileName.endswith('bnd'):
        if FileName not in bnd:
            bnd.append(FileName)

def JudgeTypeByPath(FileName,path):
    FileName = str(FileName)
    path = str(path)
    if path.startswith('LIBRY'):
        FileName = FileName.upper()
        path = path.upper()
    if path.endswith('MIS'):
        if FileName not in mis:
            mis.append(FileName)
    elif path.endswith('INV'):
        if FileName not in inv:
            inv.append(FileName)
    elif path.endswith('BOR'):
        if FileName not in bor:
            bor.append(FileName)
    elif path.endswith('GEN'):
        if FileName not in gen:
            gen.append(FileName)
    elif path.endswith('CTA'):
        if FileName not in cta:
            cta.append(FileName)
    elif path.endswith('ATM'):
        if FileName not in atm:
            atm.append(FileName)
    elif path.endswith('cat'):
        if FileName not in cat:
            cat.append(FileName)
    else:
        other.append(FileName)
    
    
        
def StoreSources(StartRow,EndRow,sheet):
    for i in range(StartRow,EndRow):
        row = sheet.UsedRange.Rows[i].Value[0]
        if row[1]:
            value = row[1]
            value = value.strip()
            path = row[2]
            if value.endswith('xml') or value.endswith('htm'):
                continue
            elif value.endswith('COB') or value.endswith('sh') or value.endswith('sql') or value.endswith('card') or value.endswith('sqb') or value.endswith('bnd') or value.endswith('exe') :
                JudgeTypeByName(value)
            else:
                JudgeTypeByPath(value,path)

def PutSources(ip):
    region = FTP('10.20.117.17')
    region.login(users[ip], users[ip])
    os.chdir(r'C:\Users\ccf\Desktop')
    if cobol:
        region.cwd('/fns/' + ip + '/r/src')
        region.storbinary('STOR ' + 'list', open('list', 'rb'))
        os.chdir(r'C:\good\cobol\work\update\cobol')
        for codes in cobol:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if sql:
        os.chdir(r'C:\good\cobol\work\update\sql')
        region.cwd('/fns/' + ip + '/r/sql')
        for codes in sql:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if sqb:
        os.chdir(r'C:\good\cobol\work\update\sqb')
        region.cwd('/fns/' + ip + '/r/dbdb2/pco')
        for codes in sqb:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if shell:
        os.chdir(r'C:\good\cobol\work\update\shell')
        region.cwd('/fns/' + ip + '/r/sh')
        for codes in shell:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if exe:
        os.chdir(r'C:\good\cobol\work\update\exe')
        region.cwd('/fns/' + ip + '/r/exe')
        for codes in shell:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if card:
        os.chdir(r'C:\good\cobol\work\update\card')
        region.cwd('/fns/' + ip + '/r/card')
        for codes in card:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if bnd:
        os.chdir(r'C:\good\cobol\work\update\bnd')
        region.cwd('/fns/' + ip + '/r/dbdb2/bnd')
        for codes in bnd:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if mis:
        os.chdir(r'C:\good\cobol\work\update\mis')
        region.cwd('/fns/' + ip + '/r/src/LIBRYMIS')
        for codes in mis:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if inv:
        os.chdir(r'C:\good\cobol\work\update\inv')
        region.cwd('/fns/' + ip + '/r/src/LIBRYINV')
        for codes in inv:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if bor:
        os.chdir(r'C:\good\cobol\work\update\bor')
        region.cwd('/fns/' + ip + '/r/src/LIBRYBOR')
        for codes in bor:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if gen:
        os.chdir(r'C:\good\cobol\work\update\gen')
        region.cwd('/fns/' + ip + '/r/src/LIBRYGEN')
        for codes in gen:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if cta:
        os.chdir(r'C:\good\cobol\work\update\cta')
        region.cwd('/fns/' + ip + '/r/src/LIBRYCTA')
        for codes in cta:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    if atm:
        os.chdir(r'C:\good\cobol\work\update\atm')
        region.cwd('/fns/' + ip + '/r/src/LIBRYATM')
        for codes in atm:
            region.storbinary('STOR ' + codes, open(codes, 'rb'))
    region.quit()
    
                
def UpdateRegion(*ips):
    for region in ips:
        PutSources(region)
    

def main():
    app = win32com.client.Dispatch('Excel.Application')
    workbook = app.Workbooks.Open('C:\\Users\\ccf\\Desktop\\QA file.xlsx')
    sheet = workbook.Sheets('ccf1')
    StoreSources(GetStartRow(sheet),GetEndRow(sheet),sheet)
    workbook.Close()
    app.Quit()
    GetSources()
    #UpdateRegion('d2')
    
if __name__ == '__main__':
    main()
    if other:
        for item in other:
            print item
    else:
        print 'OK'
    
    