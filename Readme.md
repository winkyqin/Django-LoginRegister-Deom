# 环境
- python==3.7
- django==2.1.7

# 使用
1. 安装依赖
    > pip install -r requirements.txt
2. 配置
    修改setting.py文件，把信息填写成自己的，不然短信发布出去
    ```python
    # 阿里云短信配置
    ACCESS_KEY_ID = "********"  # key
    ACCESS_KEY_SECRET = "********"  # secret
    SIGN_NAME = '********'  # 模板名称
    TEMPLATE_CODE = '********'  # 模板code
   
    ```
 3. python manage.py runserver