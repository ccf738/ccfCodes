'''
Created on 2013-2-22

@author: ccf
'''
def LastLine(FilePath):
    """this method read the file from the
    last line to fist line one by one"""
    for line in reversed(open(FilePath,'r').readlines()):
        print line

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
if __name__ == "__main__":
    dos2unix(r'C:\123.txt')
    LastLine(r'C:\123.txt')