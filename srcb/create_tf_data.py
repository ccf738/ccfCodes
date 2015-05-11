__author__ = 'user'
import xml.parsers.expat
import math

sum_three = [0, 1, 2]
for dummy_i in range(25):
    sum_three.append(sum(sum_three[-3:]))
print sum_three[20]