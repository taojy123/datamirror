#coding:utf-8

import cookielib
import urllib2
import urllib
import re
import json
import os

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
                     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                     ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                     ('Connection', 'keep-alive'),
                     ('Accept-encoding', 'identity')]

def get_page(url, data=None):
    resp = opener.open(url, data)
    page = resp.read()
    return page


txtMinX = 115.04883
txtMaxX = 117.77344
txtMinY = 39.3003
txtMaxY = 40.9799

txtMinX = raw_input("lon_min:")
txtMaxX = raw_input("lon_max:")
txtMinY = raw_input("lat_min:")
txtMaxY = raw_input("lat_max:")

mode = raw_input("ASTGTM-1 / ASTSLP-2:")



login_page_url = "http://datamirror.csdb.cn/login.htm"
login_page = get_page(login_page_url)

lt_key = re.findall(r'name="lt" value="(.*?)"', login_page)[0]
print lt_key

formData = urllib.urlencode({"username": "yz_zhao0501@163.com",
                             "password": "zyz19880516",
                             "lt": lt_key,
                             "_eventId": "submit"})
login_url = "http://auth.csdb.cn/login?service=http%3A%2F%2Fwww.gscloud.cn%2Flogin.jsp%3Ffrom%3Dhttp%253A%252F%252Fwww.gscloud.cn%252F"
page = get_page(login_url, formData)
if "<script type='text/javascript'>top.window.location.reload();window.close();</script>" in page:
    print "Login Success."
else:
    print "Login Failure."
    raw_input("Press Enter to exit")
    exit()


formData = urllib.urlencode({"mode": "zb",
                             "txtMinX": txtMinX,
                             "txtMaxX": txtMaxX,
                             "txtMinY": txtMinY,
                             "txtMaxY": txtMaxY,
                             "grid": "",
                             "Submit1": "提交",
                             "maxRows": "80",
                             "gdem_list_tr_": "true",
                             "gdem_list_p_": "1",
                             "gdem_list_mr_": "80"
                            })
search_url = "http://datamirror.csdb.cn/list.dem?type=gdem&opType=search"
page = get_page(search_url, formData)
ids = re.findall(r"ASTGTM_(.*?)\r", page)
ids = ids[::2]
print ids
print "Total %d files will download." % (len(ids))


ASTGTM_url = "http://datamirror.csdb.cn/gdemDownload.dem?id=N30E119X&fileType=gdem_utm&type=gdem_utm"
ASTSLP_url = "http://datamirror.csdb.cn/gdemDownload.dem?id=N30E119X&fileType=slp_utm&dataType=slp_utm"



i = 0
for id in ids:
    
    if mode == "1":
        i = i + 1
        ASTGTM_url = "http://datamirror.csdb.cn/gdemDownload.dem?id=%s&fileType=gdem_utm&type=gdem_utm" % id
        File_name = "ASTGTM_%s.zip" % id
        print "(%d/%d)Begin download %s , please waiting a moment..." % (i, len(ids)*2, File_name)
        page = get_page(ASTGTM_url)
        open(File_name, "wb").write(page)
        print "Download %s finish." % File_name
    elif mode == "2":
        i = i + 1
        ASTSLP_url = "http://datamirror.csdb.cn/gdemDownload.dem?id=%s&fileType=slp_utm&dataType=slp_utm" % id
        File_name = "ASTSLP_%s.zip" % id
        print "(%d/%d)Begin download %s , please waiting a moment..." % (i, len(ids)*2, File_name)
        page = get_page(ASTSLP_url)
        open(File_name, "wb").write(page)
        print "Download %s finish." % File_name

print "Total Finish!"

raw_input("Press Enter to exit")



