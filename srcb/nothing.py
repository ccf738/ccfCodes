# -*- coding:utf-8 -*-

__author__ = 'user'
import excel
import os
import shutil
from ftplib import FTP
import sqlite3
import urllib2
import urllib
import sys
import re
import math
import random

import telnetlib
import timeit
from decimal import *
import xml.parsers.expat

excel_dir = unicode(r"C:\Documents and Settings\user\桌面\update\\", "utf-8")
database_file = unicode(r'\\10.20.34.200\共享目录\开发文档\bancsUpdate.db', "utf-8")
local_base_dir = r'c:\good\cobol\update\\'


class Overload():
    def __init__(self, a):
        pass

    def __init__(self, a, b):
        pass
def get_test_doc(ir_no, des):
    for test_file in os.listdir(unicode(r'\\10.20.34.200\共享目录\开发文档\生产问题单元测试报告')):
        if test_file.count(ir_no[-5:]) >= 1:
            shutil.copy(unicode(r'\\10.20.34.200\共享目录\开发文档\生产问题单元测试报告\\')+test_file, des+test_file)


def test_re():
    test_string = 'asd fdsa fff'
    p = re.compile('\\w+\\b')
    m = re.search('(?<=abc)[^ ]*\\b', test_string)
    print p.findall(test_string)


def myaaa(x):
    val = int(x)
    return -5*math.pow(val, 5) + 69*math.pow(val, 2) - 47

def future_value(present_value, annual_rate, periods_per_year, years):
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years
    return present_value*math.pow((1+rate_per_period), periods)

def cal_area(sides, side_length):
    return (1.0/4)*sides*math.pow(side_length, 2)/math.tan((math.pi/sides))

def project_to_distance(point_x, point_y, distance):
    dist_to_origin = math.sqrt(point_x**2 + point_y**2)
    scale = distance / dist_to_origin
    print point_x*scale, point_y*scale


def compile_cob(host, user, password):
    region = telnetlib.Telnet(host)
    region.read_until("login:", 3)
    region.write(user + "\n")
    region.read_until("Password:", 3)
    region.write(password + "\n")
    region.write("compilecob IN0800.COB" + "\n")
    result = region.read_until("Terminal output also present in")
    print result
    if result.count("error(s) in compilation:"):
        print "not SUCCESSFUL".ljust(20) + "IN0800".center(10) + host.rjust(20)
    region.close()


def resources_vs_time(upgrade_cost_increment, num_upgrades):
    result = []
    time_at_purchase = 0
    total_cost = 1
    rate = 1
    total_resources_generated = 0
    for _ in range(num_upgrades):
        time_at_purchase += total_cost / rate
        total_resources_generated += total_cost
        total_cost += upgrade_cost_increment
        rate += 1
        result.append([time_at_purchase, total_resources_generated])
    return result


def gen_test(num):
    current_num = 0
    while current_num < num:
        yield current_num
        current_num += 1


class Over():
    def __init__(self, date):
        self.data = date

    def __add__(self, other):
        return self.data + other

    def __mul__(self, other):
        print self.data * other


def bin_to_dec(binary_number):
    bin_str = str(binary_number)
    if bin_str is None:
        return 0
    if bin_str == "1":
        return 1
    if bin_str == "0":
        return 0
    return math.pow(2, len(bin_str) - 1) * int(bin_str[0]) + bin_to_dec(bin_str[1:])


class BinarySearchTree:
    def __init__(self, value, parent, left_child, right_child):
        self._value = value
        self._parent = parent
        self._left_child = left_child
        self._right_child = right_child

def my_gen(values):
    for value in values:
        yield value + 1



if __name__ == '__main__':
    for i in my_gen([a for a in range(5)]):
        print i