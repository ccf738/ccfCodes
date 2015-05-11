__author__ = 'qctest'

orig_onrf = open(r'D:\111\ONRF.TXT','r')
out_onrf = open(r'D:\111\OUT_ONRF.TXT','w')
orig_invm = open(r'D:\111\INMS5.TXT','r')
real_open_date = {}
for line in orig_invm.readlines():
    if line[10:12] != "29" and line[10:12] != "20":
        continue
    line = line[:-1]
    acct_no = line[:20]
    open_date = line[182:190]
    real_open_date[acct_no] = open_date
for line in orig_onrf.readlines():
    line = line[:-1]
    if line[10:12] != "29" and line[10:12] != "20":
        out_onrf.write(line + "\n")
        continue
    acct_no = line[:20]
    other_1 = line[20:86]
    other_2 = line[94:]
    try:
        open_date = real_open_date.get(acct_no)
    except:
        print acct_no
        continue
    try:
        out_onrf.write(acct_no+other_1+open_date+other_2+"\n")
    except:
        print acct_no, other_1,open_date, other_2
orig_invm.close()
orig_onrf.close()
out_onrf.close()