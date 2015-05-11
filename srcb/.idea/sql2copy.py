__author__ = 'user'
import re
import ntpath
import os
def create_copy(file_path):
    length_pattern = re.compile(' \([^)]*\) ')
    sql_file = open(file_path)
    head,tail = ntpath.split(file_path)
    table_name = tail.upper()[0:tail.find('.')]
    copy = open(r'd:\vssflile\\' + table_name + 'MAST','wb')
    #copy.write(' '*7 + '01 ' + table_name + '-RECORD.\n')
    for line in sql_file.readlines():
        if not('CHAR' in line or 'NUMBER' in line):
            continue
        for i in range(1,len(line)):
            if line[i] == ' ':
                variable = ' '*11 + '03 ' + table_name + '-' + line[1:i].upper().replace('_','-') + ' PIC '
                variable_length =  re.findall(length_pattern,line[1:])[0].replace('(','').replace(')','').strip()
                if 'CHAR' in line:
                    variable += 'X(' + str(variable_length) + ').\n'
                else:
                    comma_index = variable_length.find(',')
                    decimal_lenght = int(variable_length[comma_index+1:]) if comma_index>0 else 0
                    comma_index = len(variable_length) if comma_index < 0 else comma_index
                    integer_length = int(variable_length[0:comma_index]) - decimal_lenght
                    variable += '9(' + str(integer_length) + ')V9(' + str(decimal_lenght) + ') COMP-3.\n'
                copy.write(variable)
                break
    sql_file.close()
    copy.close()
if __name__ == '__main__':
    create_copy(r'D:\vssflile\aach.sql')
    #if os.path.isdir(r'D:\vssflile\aach.sql'):
    #    for sql_file in os.listdir(path):
    #        if sql_file.endswith('.sql'):
    #            create_copy(sql_file)