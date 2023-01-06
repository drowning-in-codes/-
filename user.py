import sys
import requests


class User:
    def __init__(self):
        self.access_token = None
        self.__appId = input('请输入您的appid:')
        self.__appSecret = input('请输入您的appsecret:')
        self.logintime = 3
        self.login()

    def login(self):
        while self.logintime:
            try:
                res = requests.get(
                    f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.__appId}&secret={self.__appSecret}", )
                if res.status_code == 200:
                    self.access_token = res.json()['access_token']
                else:
                    print('输入错误!请尝试再次输入,还剩' + self.logintime + '次机会')
            except Exception as e:
                print('错误', res.json(), e)
            self.logintime = self.logintime - 1

    def quit(self):
        print('退出')
        sys.exit(0)
