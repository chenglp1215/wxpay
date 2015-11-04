import hashlib,random,string,time
from urllib import quote

app_id = 'wx1f41941b270be240'
app_secret = '6feda656830d308c16b10176e81524f7'
pay_sign_key = 'EGIry6Q1RrhVno9GVVJRo0OkUCJp8Dvu91meegub76v17RylL5mnziWaixQsEQVGiPTBBx4uHWGCJGgVVqoN4U0P9Y0ksgAYCFojYEsOYF1yIdOpjN07qj7fml0al1gB'
partner_id = '1221349901'
partner_key = 'a0913527a437377e1f708e229f9e7dd2'

def get_noncestr():
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return string.join(random.sample(list(s), 32)).replace(' ','')

def get_timestamp():
    return '%s' % int(time.time())

def get_package(out_trade_no,total,content,spbill_create_ip):
    stringTemplate = "bank_type=%s&body=%s&fee_type=%s&input_charset=%s&notify_url=%s&out_trade_no=%s&partner=%s&spbill_create_ip=%s&total_fee=%s&key=%s"
    stringSignTemp = stringTemplate % ('WX',content,'1','UTF-8','http://e.tapindata.com/pay_ok/',out_trade_no,partner_id,spbill_create_ip,total,partner_key)
    signValue = hashlib.md5(stringSignTemp).hexdigest().upper()
    stringTemplate2 = "bank_type=%s&body=%s&fee_type=%s&input_charset=%s&notify_url=%s&out_trade_no=%s&partner=%s&spbill_create_ip=%s&total_fee=%s&sign=%s"
    return stringTemplate2 % (quote('WX'),quote(content),quote('1'),quote('UTF-8'),quote('http://e.tapindata.com/pay_ok/'),quote(out_trade_no),quote('1221349901'),quote(spbill_create_ip),quote(total),signValue)

def getSign(package,timestamp,noncestr):
    stringTemplate = 'appid=%s&appkey=%s&noncestr=%s&package=%s&timestamp=%s'
    s = stringTemplate % (app_id,pay_sign_key,noncestr,package,timestamp)
    return hashlib.sha1(s).hexdigest()

def pay_ok_sign_check(d):
    lst = d.keys()
    lst.sort()
    s = ''
    for key in lst:
        if key == 'sign':
            continue
        s += '%s=%s&' % (key,d[key])
    s += 'key=%s' % partner_key
    check_sign = hashlib.md5(s).hexdigest().upper()
    return d['sign'] == check_sign