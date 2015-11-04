# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from models import Product,ProductSeller,PurchaseLog,User,Rank,Notify,Alert
import requests,json,re,time
import pay,base64


def oauth(request):
    appId = pay.app_id
    sercet = pay.app_secret
    code = request.GET.get('code')
    state = request.GET.get('state')
    html_src = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (appId,sercet,code),verify=False).content
    print html_src
    j = json.loads(html_src)
    html_src_ui = requests.get('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (j['access_token'],j['openid']),verify=False).content
    print html_src_ui
    ui = json.loads(html_src_ui)
    user = User.objects.get_or_create(open_id = j['openid'])[0]
    user.open_id = j['openid']
    user.avatar = ui['headimgurl']
    user.nickname = base64.b64encode(ui['nickname'].encode('utf-8'))
    user.save()
    request.session['open_id'] = user.open_id
    return HttpResponseRedirect(state)


def index(request):
    user = User.objects.get(open_id = request.session.get('open_id'))
    product = Product.objects.filter(is_alive=True,is_current=True).order_by('-id')[0]
    ps_list = ProductSeller.objects.filter(product = product).order_by('-saleroom')[:50]
    in_the_rank = False
    ps = None
    if len(ps_list) and ProductSeller.objects.filter(product = product,seller = user):
        ps = ProductSeller.objects.filter(product = product,seller = user)[0]
        last = ps_list[len(ps_list)-1]
        in_the_rank =  ps.saleroom >= last.saleroom
    return render_to_response('index.html',{
        'product':product,
        'ps_list':ps_list,
        'in_the_rank':in_the_rank,
        'self':ps,
    })

def detail(request):
    user = User.objects.get(open_id = request.session.get('open_id'))
    product = Product.objects.filter(is_alive=True,is_current=True).order_by('-id')[0]
    ps = None
    if ProductSeller.objects.filter(product = product,seller = user):
        ps = ProductSeller.objects.filter(product = product,seller = user)[0]
    return render_to_response('detail.html',{
        'product':product,
        'self':ps,
    })

def join(request,product_id):
    user = User.objects.get(open_id = request.session.get('open_id'))
    if request.POST:
        product = Product.objects.get(id = product_id)
        ps_list = ProductSeller.objects.filter(seller=user,product=product)
        if not ps_list:
            user.nickname = request.POST.get('nickname')
            user.tel = request.POST.get('tel')
            user.desc = request.POST.get('desc')
            user.save()
            ps = ProductSeller()
            ps.product = product
            ps.seller = user
            ps.save()
        else:
            ps = ps_list[0]
        return HttpResponseRedirect('/share/%s/0/' % ps.id)
    return render_to_response('join.html',{
        'product_id':product_id,
        'user':user,
    })

def share(request,ps_id,pl_id):
    ps = ProductSeller.objects.get(id = ps_id)
    count = 1
    if int(pl_id):
        pl = PurchaseLog.objects.get(id = pl_id)
        count = pl.count
    if request.POST:
        count = int(request.POST.get('count'))
        buyer = User.objects.get(open_id = request.session.get('open_id'))
        if int(pl_id):
            pl = PurchaseLog.objects.get(id = pl_id)
            pl.count = count
            pl.save()
        else:
            pl = PurchaseLog()
            pl.ps = ps
            pl.buyer = buyer
            pl.count = count
            pl.order_num = int(time.time()*1000)
            pl.save()
        # rank = Rank.objects.get_or_create(ps_id = ps_id,buyer = buyer)[0]
        # rank.count += count
        # rank.total += count*ps.product.price
        # rank.save()
        # ps.saleroom += count*ps.product.price
        # ps.save()
        return HttpResponseRedirect('/order/?pl_id=%s' % pl.id)
    return render_to_response('share.html',{
        'ps':ps,
        'count':count,
        'pl_id':pl_id,
    })

def order(request):
    pl = PurchaseLog.objects.get(id = request.GET.get('pl_id'))
    timestamp = pay.get_timestamp()
    app_id = pay.app_id
    noncestr = pay.get_noncestr()
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    package = pay.get_package(out_trade_no=str(pl.order_num),total= '%.0f' % (pl.count*pl.ps.product.price*100),content='%s[%s件]' % (pl.ps.product.name.encode('utf-8'),pl.count),spbill_create_ip=ip)
    sign = pay.getSign(package=package,timestamp=timestamp,noncestr = noncestr)
    return render_to_response('order.html',{
        'pl_id':pl.id,
        'user':pl.buyer,
        'ps':pl.ps,
        'count':pl.count,
        'total':int(pl.count)*pl.ps.product.price,
        'app_id':app_id,
        'noncestr':noncestr,
        'timestamp':timestamp,
        'package':package,
        'sign':sign,
    })

def seller(request,open_id):
    seller = User.objects.get(open_id = open_id)
    ps_list = ProductSeller.objects.filter(seller = seller).order_by('-id')
    ps = ps_list[0]
    ranks = Rank.objects.filter(ps = ps).order_by('-count')
    return render_to_response('seller.html',{
        'seller':seller,
        'ps':ps,
        'ranks':ranks,
    })

def buyer(request,pl_id):
    pl = PurchaseLog.objects.get(id = pl_id)
    user = pl.buyer
    if request.POST:
        user.name = request.POST.get('name')
        user.tel = request.POST.get('tel')
        user.add = request.POST.get('add')
        user.save()
        return HttpResponseRedirect('/')
    return render_to_response('buyer.html',{
        'pl':pl,
        'user':user,
    })


def pay_ok(request):
    params = request.GET
    try:
        if pay.pay_ok_sign_check(params) and params['trade_state'] == u'0':
            order_num = params['out_trade_no']
            notify = Notify.objects.get_or_create(order_num = order_num)[0]
            notify.get_content = str(params)
            notify.post_content = str(request.body)
            notify.save()
            pl = PurchaseLog.objects.filter(order_num = order_num)[0]
            pl.has_paid = True
            pl.save()
            rank = Rank.objects.get_or_create(ps_id = pl.ps_id,buyer = pl.buyer)[0]
            rank.count += pl.count
            rank.total += pl.count*pl.ps.product.price
            rank.save()
            ps = pl.ps
            ps.saleroom += pl.count*ps.product.price
            ps.save()
            return HttpResponse('success')
        else:
            return HttpResponse('fail')
    except Exception,e:
        return HttpResponse(str(e))


def alert(request):
    a = Alert()
    a.alert = request.body
    a.save()
    return HttpResponse('success')