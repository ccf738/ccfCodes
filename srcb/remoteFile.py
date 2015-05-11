# -*- coding:utf-8 -*-
import excel
from datetime import datetime, date, time
import math
__author__ = 'user'
a = 5

#if __name__ == '__main__':
#    print "asd"
#    print a
def hello(fn):
    def wrapper():
        print "hello, %s" % fn.__name__
        fn()
        print "goodby, %s" % fn.__name__
    return wrapper

@hello
def foo():
    print "i am foo"


def gen_replaced_vchr():
    """生成凭证号替换的清单"""
    with_dup = open(r'd:\t_vchr.txt', 'r')
    replaced_list = open(r'd:\replaced_list.txt', 'w')
    for line in with_dup.readlines():
        line = line[:-1]
        record = line.split("|")
        if record[2] != record[3]:
            record[4] = record[0][2:10]
            replaced_list.write("|".join(record) + "\n")
    with_dup.close()
    replaced_list.close()


def sieve_prime(num):
    if num < 1:
        return 0
    if num == 2:
        return 1
    prime_ind_list = [1 for _ in range(0, num+1)]
    for i in range(2, int(math.sqrt(num)) + 1):
        if prime_ind_list[i] == 1:
            for j in range(i, num+1):
                if i*j > num:
                    break
                prime_ind_list[i*j] = 0
    cat = [i for i in range(2, num+1) if prime_ind_list[i] == 1]
    print len(cat)


if __name__ == '__main__':
    aaa = '4639040011'
    print aaa, aaa[:-1], aaa[:-2], aaa[:-3]