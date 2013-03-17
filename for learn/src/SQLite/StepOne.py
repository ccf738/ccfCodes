'''
Created on 2012-8-26

@author: ccf
'''
import sqlite3

db = sqlite3.connect(r'E:/Python 2.7/Scripts/mysite/mysite/db/django.db')
cu = db.cursor()
#cu.execute('create table if not exists catalog(id integer primary key,pid interger,name varchar(10) UNIQUE)')
#cu.execute("insert into catalog values(0,1,'John')")
#cu.execute("insert into catalog values(1,3,'Mary')")
#db.commit()
cu.execute("select * from books_author")
print cu.description
print cu.rowcount
res = cu.fetchall()
for line in res:
    print line
    print '-'*60
cu.close()  
db.close()
