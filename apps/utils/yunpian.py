
import requests

class YunPian(object):


    def send_sms(self, code, mobile):
        print("send sms{code}".format(code=code))