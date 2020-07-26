from django.shortcuts import render,redirect,HttpResponse,reverse
from django.http import JsonResponse
from django.views import View
from app1.form import Userform
from app1.models import *
from django.contrib import auth
from OnlineMall import settings
import redis
import datetime
import time
import random
import json

REDIS_CONN = redis.Redis(decode_responses=True)

def shouye(request):
    return redirect("/index/0")

def index(request,good_type):

    login_user_id = request.session.get("_auth_user_id")
    login_user = request.user
    pre_login = request.session.get("pre_login")
    if good_type=="0":
        goods=Shangpin.objects.all()
    else:
        goods=Shangpin.objects.filter(catagory=good_type)

    shopping_carts = []
    sum_price = 0
    # items_num = REDIS_CONN.mget(*REDIS_CONN.keys("shopping_cart_%s_*"%request.user.id))
    # ['2', '2', '4', '6']

    items = REDIS_CONN.keys("shopping_cart_%s_*" % request.user.id)
    # ['shopping_cart_4_5', 'shopping_cart_4_6', 'shopping_cart_4_4', 'shopping_cart_4_3']

    for item in items:
        item_id = item.split("_")[-1]
        item_tobuy = Shangpin.objects.filter(id=item_id)[0]
        item_num = REDIS_CONN.get(item)
        shopping_carts.append({
            "item": item_tobuy,
            "num": item_num
        })
        sum_price += float(item_tobuy.price) * float(item_num)
    # print(sum_price)
    # print(shopping_carts)
    return render(request,"index.html",locals())

def gooddetails(request,id):
    # good=Shangpin.objects.filter(id=id).first()
    good=Shangpin.objects.get(id=id)
    return render(request,"gooddetails.html",locals())

class Login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        user = request.POST.get("user")
        psd = request.POST.get("psd")
        res_dict={"user":None,"error_msg":"",}
        user_login = auth.authenticate(username=user,password=psd)
        if user_login:
            pre_login_time = Userinfo.objects.filter(username=user).values_list("last_login").first()[0]
            request.session["pre_login"] = str(pre_login_time)
            auth.login(request, user_login)
            res_dict["user"]=user
        else:
            res_dict["error_msg"]="用户名或密码错误"
        return JsonResponse(res_dict)

class Reg(View):
    def get(self, request):
        reg_form = Userform()
        return render(request, 'reg.html',{"reg_form":reg_form})

    def post(self, request):
        res_dict={"User":None,"error_msg":""}
        # print(request.POST)
        reg_form=Userform(request.POST)

        if reg_form.is_valid():
            res_dict["user"] = reg_form.cleaned_data.get("user")
            user = reg_form.cleaned_data.get("user")
            pwd = reg_form.cleaned_data.get("pwd")
            address = reg_form.cleaned_data.get("address")
            gender = reg_form.cleaned_data.get("gender")
            tel = reg_form.cleaned_data.get("tel")
            Userinfo.objects.create_user(username=user, password=pwd, address=address,gender=gender,tel=tel)
            res_dict["user"] = user
        else:
            res_dict["error_msg"] = reg_form.errors
        return JsonResponse(res_dict)

def logout(request):

 # 退出登陆要不要清空购物车呢？
    items = REDIS_CONN.keys(settings.SHOPPING_CART_KEY % (request.user.id, "*"))
    for item in items:
        REDIS_CONN.delete(item)

    auth.logout(request)
    # 退出清空购物车,有这个必要吗
    return redirect("/login/")

class Edit_user(View):
    def get(self,request):
        login_user_tel = request.user.tel
        login_user_address = request.user.address
        return render(request,"edit_user.html",locals())

    def post(self,request):
        tel=request.POST.get("tel")
        address=request.POST.get("address")
        Userinfo.objects.filter(id=request.user.id).update(tel=tel,address=address)
        return redirect("/index/0/")

def add2cart(request,good_id):
    user_id = request.user.id
    shopping_cart_key = settings.SHOPPING_CART_KEY % (user_id,good_id)
    REDIS_CONN.incr(shopping_cart_key,1)

    return redirect("/index/0/")

def sub2cart(request,good_id):
    user_id = request.user.id
    shopping_cart_key = settings.SHOPPING_CART_KEY % (user_id,good_id)
    REDIS_CONN.incr(shopping_cart_key,-1)
    # print(type(REDIS_CONN.get(shopping_cart_key)))
    if REDIS_CONN.get(shopping_cart_key) == "0":
        REDIS_CONN.delete(shopping_cart_key)

    return redirect("/index/0/")

def add2order(request):
    items = REDIS_CONN.keys(settings.SHOPPING_CART_KEY%(request.user.id,"*"))
    sum_price = 0
    good_list=[]
    detail_str = ''
    for item in items:
        item_id = item.split("_")[-1]
        item_tobuy = Shangpin.objects.filter(id=item_id)[0]
        item_num = REDIS_CONN.get(item)
        good_list.append(item_tobuy)
        sum_price += float(item_tobuy.price) * float(item_num)
        detail_str += "%s×%s," %(item_tobuy.title,item_num)

        REDIS_CONN.delete(item)

    if sum_price == 0:
        return HttpResponse("未购买任何商品，再去逛逛吧")

    date_now = (str(datetime.datetime.now()).split("."))[0]
    random_num = str(time.time()).split(".")[0][-6:]
    for i in range(1,5):
        random_num += str(random.randint(0,9))
    order = Order.objects.create(order_num=random_num,date=date_now,user=request.user,sum_price=sum_price,details=detail_str)
    order.goods.set(good_list)

    return redirect("/showorder/")


def showorder(request):
    order_list = Order.objects.filter(status="1",user=request.user)
    order_list_done = Order.objects.filter(status="2",user=request.user)
    return render(request, "order.html", locals())


def deleteorder(request,id):
    Order.objects.filter(id=id).delete()
    return redirect("/showorder/")


class Pay(View):
    def get(self,request,id):
        ordertooay = Order.objects.get(id=id)
        return render(request,"pay.html",locals())

    def post(self,request,id):
        res_dict={"code":None}
        Order.objects.filter(id=id).update(status="2"),
        res_dict["code"] = "200"
        return JsonResponse(res_dict)
