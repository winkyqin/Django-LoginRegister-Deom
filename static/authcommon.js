function Auth() {
    var self = this;
    self.smsCaptcha = $('#sms-captcha-btn');
}

Auth.prototype.run = function () {
    var self = this
    self.listenSmsCaptchaEvent()
    self.listenImgCaptchaEvent();
    self.listenSignupEvent();
    self.listenSigninEvent();
    self.listenForgetPasswordEvent();
    self.listenSmsCaptchaLoginEvent();
}


Auth.prototype.smsSuccessEvent = function () {
    var self = this;
    layer.msg('短信验证码发送成功')
    self.smsCaptcha.addClass('disabled');
    var count = 60;
    self.smsCaptcha.unbind('click');
    var timer = setInterval(function () {
        self.smsCaptcha.val(count + 's');
        count -= 1;
        if (count <= 0) {
            clearInterval(timer);
            self.smsCaptcha.removeClass('disabled');
            self.smsCaptcha.val('发送验证码');
            self.listenSmsCaptchaEvent();
        }
    }, 1000);
};

Auth.prototype.listenSmsCaptchaEvent = function () {
    var self = this;
    var smsCaptcha = $(".sms-captcha-btn");
    var telephoneInput = $('.log-con .input-group input[name="telephone"]')
    smsCaptcha.click(function () {
        var telephone = telephoneInput.val()
        if (!telephone) {
            layer.msg('请输入手机号码')
            return
        }
        webajax.get({
            'url': '/sms_captcha/',
            'data': {
                telephone: telephone
            },
            'success': function (res) {
                if (res.code == '200') {
                    self.smsSuccessEvent();
                } else {
                    layer.msg(res.message)
                }
            },
            'fail': function (error) {
                layer.msg('网络错误')
            }
        })
    })

}

Auth.prototype.listenImgCaptchaEvent = function () {
    var imgCaptcha = $('.img-captcha');
    imgCaptcha.click(function () {
        imgCaptcha.attr("src", "/img_captcha/" + "?random=" + Math.random())
    });
};


Auth.prototype.listenSignupEvent = function () {
    var signupGroup = $(".register")
    var submitBtn = signupGroup.find('.submit_btn')
    submitBtn.click(function (event) {
        event.preventDefault();
        var usernameInput = signupGroup.find('input[name="username"]')
        var telephoneInput = signupGroup.find('input[name="telephone"]')
        var password1Input = signupGroup.find('input[name="password1"]')
        var password2Input = signupGroup.find('input[name="password2"]')
        var smsCaptchaInput = signupGroup.find('input[name="sms_captcha"]')
        var imgCaptchaInput = signupGroup.find('input[name="img_captcha"]')

        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var img_captcha = imgCaptchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var sms_captcha = smsCaptchaInput.val();

        webajax.post({
            url: '/register/',
            data: {
                'username': username,
                'telephone': telephone,
                'password1': password1,
                'password2': password2,
                'sms_captcha': sms_captcha,
                'img_captcha': img_captcha,
            },
            'success': function (res) {
                if (res.code == '200') {
                    telephoneInput.val('')
                    usernameInput.val('')
                    imgCaptchaInput.val('')
                    password1Input.val('')
                    password2Input.val('')
                    smsCaptchaInput.val('')
                    layer.msg('注册成功')
                }
            }
        })

    })
}


Auth.prototype.listenSigninEvent = function () {
    var self = this
    var siginGroup = $('.login-box')
    var usernameInput = siginGroup.find('input[name="username"]')
    var passwordInput = siginGroup.find('input[name="password"]')
    var rememberInput = siginGroup.find('input[name="remember"]')
    var imgCaptchaInput = siginGroup.find('input[name="img_captcha"]')

    var submitBtn = siginGroup.find('.submit_btn')
    submitBtn.click(function (event) {
        console.log('123')
        event.preventDefault();
        var username = usernameInput.val()
        var password = passwordInput.val()
        var remember = rememberInput.prop("checked");
        var imgCaptcha = imgCaptchaInput.val()

        webajax.post({
            'url': '/login/',
            'data': {
                'username': username,
                'password': password,
                'remember': remember ? 1 : 0,
                'img_captcha': imgCaptcha
            },
            'success': function (res) {
                if (res.code == '200') {
                    usernameInput.val('')
                    passwordInput.val('')
                    imgCaptchaInput.val('')
                    layer.msg('登陆成功')
                    window.location.href = "/"
                }
            },

        })
    })
}

Auth.prototype.listenForgetPasswordEvent = function () {
    var self = this
    var forgetGroup = $('.forget')
    var telephoneInput = forgetGroup.find('input[name="telephone"]')
    var password1Input = forgetGroup.find('input[name="password1"]')
    var password2Input = forgetGroup.find('input[name="password2"]')
    var smsCaptchaInput = forgetGroup.find('input[name="sms_captcha"]')

    var submitBtn = forgetGroup.find('.submit_btn')
    submitBtn.click(function () {
        console.log('123')
        var telephone = telephoneInput.val()
        var password1 = password1Input.val()
        var password2 = password2Input.val()
        var sms_captcha = smsCaptchaInput.val()

        webajax.post({
            'url': '/forget/',
            'data': {
                'telephone': telephone,
                'password1': password1,
                'password2': password2,
                'sms_captcha': sms_captcha,
            },
            'success': function (res) {
                console.log(res)
            }
        })
    })
}


Auth.prototype.listenSmsCaptchaLoginEvent = function () {
    var smsLoginGroup = $('.sms-login')
    var telephoneInput = smsLoginGroup.find('input[name="telephone"]')
    var sms_captchaInput = smsLoginGroup.find('input[name="sms_captcha"]')
    var rememberInput = smsLoginGroup.find('input[name="remember"]')

    var submitBtn = smsLoginGroup.find('.submit_btn')
    submitBtn.click(function () {
        console.log('123')
        var telephone = telephoneInput.val()
        var sms_captcha = sms_captchaInput.val()
        var remember = rememberInput.val()
        webajax.post({
            'url': '/sms_login/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'remember': remember ? 1 : 0,

            },
            'success': function (res) {
                console.log(res)
            }
        })
    })

}

$(function () {
    var auth = new Auth();
    auth.run();
});