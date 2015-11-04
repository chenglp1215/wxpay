# coding=utf-8
from django.http import HttpResponseRedirect


class RequestMiddleWare(object):
    def process_view(self, request, view, args, kwargs):
        if request.path.startswith('/oauth/'):
            return None
        if request.path.startswith('/admin/'):
            return None
        if request.path.startswith('/share/'):
            return None
        if request.path.startswith('/alert/'):
            return None
        if request.path.startswith('/pay_ok/'):
            return None
        if not request.session.get('open_id'):
            return HttpResponseRedirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1f41941b270be240&redirect_uri=http://e.tapindata.com/oauth/&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect' % request.path)
        else:
            return None