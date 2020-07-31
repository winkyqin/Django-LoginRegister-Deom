from django.shortcuts import render
from django.http import HttpResponse
import random, re
from io import BytesIO
from django.core.cache import cache
from django.views.generic.base import View
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, SmsCaptchaLoginForm
from utils import restful
from utils.captcha.captcha import Captcha
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password

User = get_user_model()


# Create your views here.

def index(request):
    """首页"""
    return render(request, 'index.html')


class RegisterView(View):
    """注册视图"""

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password1')
            # 调用Model中的create_user方法创建用户
            User.objects.create_user(username=username, telephone=telephone, password=password)
            return restful.ok()

        else:
            return restful.params_error(form.get_errors())


class LoginView(View):
    """登录视图"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            # 使用自带的authenticate方法，验证用户名和密码，然后返回user
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                if remember:
                    # 设置session 保存的时间为默认15天
                    request.session.set_expiry(None)
                else:
                    # 如果没有remember  浏览器退出session就失效
                    request.session.set_expiry(0)

                return restful.ok()
            else:
                return restful.params_error(message="手机号或者密码错误！")

        else:
            return restful.params_error(message=form.get_errors())


class ForgetPasswordView(View):
    """忘记密码/重置密码视图"""

    def get(self, request):
        return render(request, 'forget.html')

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            telephone = form.cleaned_data.get('telephone')
            user = User.objects.filter(telephone=telephone).first()  # 找到对应的用户
            user.password = make_password(password=password)  # 修改密码
            user.save()  # 保存
            return restful.ok()

        else:
            return restful.params_error(form.get_errors())


class SmsCaptchaLogin(View):
    '''短信登录视图'''

    def get(self, request):
        return render(request, 'sms_login.html')

    def post(self, request):
        form = SmsCaptchaLoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            remember = form.cleaned_data.get('remember')
            user = User.objects.get(telephone=telephone)  # 由于在表单中已经对短信验证码验证过了，这里直接返回用户
            print(user)
            if user:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)

                return restful.ok()
            else:
                return restful.params_error(message='用户不存在')

        else:
            return restful.params_error(message=form.get_errors())


# 创建短信验证码
def get_code(n=4, alpha=True):
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


# 短信验证码
def sms_captcha(request):
    telephone = str(request.GET.get('telephone'))
    t = re.compile(r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$')
    s = re.search(t, telephone)
    if s:
        print('格式正确')
        code = get_code(4, False)
        # 把telephone、code作为键和值传入cache中，并设置过期时间为5min
        cache.set(telephone, code, 5 * 60)

        # result = aliyunsms.send_sms(telephone, code)
        print('发送的验证码：', code)
        print('判断缓存中是否有:', cache.has_key(telephone))
        print('获取Redis验证码:', cache.get(telephone))
        # print(result)
        return restful.ok()
    else:
        return restful.params_error('手机号码格式错误')


# 图形验证码
def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    cache.set(text.lower(), text.lower(), 5 * 60)

    return response
