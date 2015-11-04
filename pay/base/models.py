# coding=utf-8
from django.db import models
from django.utils.translation import gettext_lazy as _
import base64

# Create your models here.
class Product(models.Model):
    name = models.CharField(_('商品名称'),max_length=100,)
    desc = models.CharField(_('商品介绍'),max_length=3000,)
    pic = models.FileField(_('商品图片'),upload_to='img/product',)
    price = models.FloatField(_('商品价格'))
    is_alive = models.BooleanField(_('是否可用'),default=True)
    is_current = models.BooleanField(_('当前显示'),default=True)

    def __str__(self):
        return u'%s' % self.name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'product'
        verbose_name = '商品'
        verbose_name_plural = '商品'


class User(models.Model):
    open_id = models.CharField(_('OPENID'),max_length=255,primary_key=True)
    nickname = models.CharField(_('昵称'),max_length=500,)
    name = models.CharField(_('姓名'),max_length=100,)
    avatar = models.CharField(_('头像'),max_length=500,)
    tel = models.CharField(_('电话'),max_length=20,null=True,blank=True)
    add = models.CharField(_('地址'),max_length=500,null=True,blank=True)
    desc = models.CharField(_('备注'),max_length=3000,null=True,blank=True)

    def get_nickname(self):
        return base64.b64decode(self.nickname)
    def __str__(self):
        return u'%s' % self.name
    def __unicode__(self):
        return u'%s' % self.name


    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ProductSeller(models.Model):
    product = models.ForeignKey(Product,verbose_name=_('货品'),related_name='ps_product')
    seller = models.ForeignKey(User,verbose_name=_('卖家'),related_name='ps_seller')
    saleroom = models.FloatField(_('销售额'),default=0.0)
    create_time = models.DateTimeField(_('生成时间'),auto_now_add=True)

    def __str__(self):
        return u'%s - %s' % (self.product.name,self.seller)
    def __unicode__(self):
        return u'%s - %s' % (self.product.name,self.seller)

    class Meta:
        db_table = 'product_seller'
        verbose_name = '商品卖家记录'
        verbose_name_plural = '商品卖家记录'


class Rank(models.Model):
    buyer = models.ForeignKey(User,verbose_name=_('买家'),related_name='rank_buyer')
    ps = models.ForeignKey(ProductSeller,verbose_name=_('商品卖家'),related_name='rank_ps')
    count = models.IntegerField(_('数量'),default=0)
    total = models.FloatField(_('总价'),default=0.0)

    def __str__(self):
        return u'%s' % self.id
    def __unicode__(self):
        return u'%s' % self.id

    class Meta:
        db_table = 'rank'
        verbose_name = '商品卖家记录'
        verbose_name_plural = '商品卖家记录'



class PurchaseLog(models.Model):
    ps = models.ForeignKey(ProductSeller,verbose_name=_('商品卖家'),related_name='log_ps')
    buyer = models.ForeignKey(User,verbose_name=_('买家'),related_name='log_buyer')
    count = models.IntegerField(_('数量'),default=0)
    has_paid = models.BooleanField(_('是否支付'),default=False)
    order_num = models.CharField(_('订单'),max_length=32,db_index=True)
    create_time = models.DateTimeField(_('创建时间'),auto_now_add=True)


    def __str__(self):
        return u'%s' % self.id
    def __unicode__(self):
        return u'%s' % self.id

    class Meta:
        db_table = 'log'
        verbose_name = '购买记录'
        verbose_name_plural = '购买记录'


class Notify(models.Model):
    order_num = models.CharField(_('订单'),max_length=32,primary_key=True)
    get_content = models.CharField(_('GET消息体'),max_length=10000,default='')
    post_content = models.CharField(_('POST消息体'),max_length=5000,default='')
    create_time = models.DateTimeField(_('创建时间'),auto_now_add=True)


    def __str__(self):
        return u'%s' % self.order_num
    def __unicode__(self):
        return u'%s' % self.order_num

    class Meta:
        db_table = 'notify'
        verbose_name = '通知'
        verbose_name_plural = '通知'

class Alert(models.Model):
    alert = models.CharField(_('GET消息体'),max_length=10000,default='')
    create_time = models.DateTimeField(_('创建时间'),auto_now_add=True)

    def __str__(self):
        return u'%s' % self.id
    def __unicode__(self):
        return u'%s' % self.id

    class Meta:
        db_table = 'alert'
        verbose_name = '告警'
        verbose_name_plural = '告警'




