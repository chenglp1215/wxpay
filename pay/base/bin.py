# coding=utf-8
import sys,os,base64,datetime
sys.path.append('"/Users/XingZY/Desktop/wxpay"')

os.environ['DJANGO_SETTINGS_MODULE'] = 'wxpay.settings'
from pay.base.models import User

for user in User.objects.all():
    print user.nickname
    user.nickname = base64.b64encode(user.nickname.encode('utf-8'))
    user.save()
    print user.nickname

print '%s completed' % datetime.datetime.now()
