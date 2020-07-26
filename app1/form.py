from django import forms
from django.forms import widgets
from app1.models import Userinfo
from django.core.exceptions import ValidationError


class Userform(forms.Form):
    user = forms.CharField(label="账号")
    pwd = forms.CharField(min_length=6,label="密码",widget=widgets.PasswordInput())
    re_pwd = forms.CharField(min_length=6,label="确认密码",widget=widgets.PasswordInput())
    gender=forms.ChoiceField(choices=((1,"男"),(2,"女")),label="性别")
    address = forms.CharField(max_length=50,label="地址")
    tel = forms.CharField(max_length=20,label="电话")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

    def clean_user(self):
        val = self.cleaned_data.get("user")
        user = Userinfo.objects.filter(username=val).first()
        if user:
            raise ValidationError("用户名已存在")
        else:
            # ----------对值进行操作，返回被操作后的值-------------------
            return val



    def clean_pwd(self):
        val = self.cleaned_data.get("pwd")
        if val.isdigit():
            raise ValidationError("密码不能是纯数字")
        else:
            return val

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd and re_pwd and pwd == re_pwd:
            return self.cleaned_data
        else:
            self.add_error("re_pwd", ValidationError("两次密码不一致"))


