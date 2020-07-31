from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


# Create your models here.
class UserManager(BaseUserManager):
    '''
    _create_user:私有方法，用来创建用户
    create_user：创建普通用户
    create_superuser：创建超级管理员
    '''

    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请输入手机号码')
        if not username:
            raise ValueError('请输入用户名')
        if not password:
            raise ValueError('请输入密码')

        user = self.model(telephone=telephone, username=username, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )

    uid = ShortUUIDField(primary_key=True)
    openid = models.CharField('OPENID', max_length=128, null=True, blank=True, unique=True)
    username = models.CharField(max_length=100, verbose_name='用户名', unique=True,null=True, blank=True)
    telephone = models.CharField(max_length=11, verbose_name='手机号', unique=True,null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True, verbose_name='昵称')
    real_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='真实姓名')
    mark = models.CharField(max_length=128, null=True, blank=True, verbose_name='用户备注')
    birthday = models.DateField("出生年月", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, choices=GENDER_CHOICES, default="male")
    avatar = models.ImageField('用户头像', upload_to='users/', null=True, blank=True)
    country = models.CharField(verbose_name='国家', null=True, blank=True, max_length=128)
    province = models.CharField(verbose_name='省份', null=True, blank=True, max_length=128)
    city = models.CharField(verbose_name='城市', null=True, blank=True, max_length=128)
    address = models.CharField(verbose_name='详细地址', null=True, blank=True, max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  # 使用用户名登录

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
